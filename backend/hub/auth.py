from django.db.models import F
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from openapi.models import OpenAPIKey


def _actor_identifiers(user):
    if not getattr(user, 'is_authenticated', False):
        return set()

    identifiers = {
        (getattr(user, 'username', '') or '').strip(),
        (getattr(user, 'email', '') or '').strip(),
        (getattr(user, 'name', '') or '').strip(),
    }
    email = (getattr(user, 'email', '') or '').strip()
    if email and '@' in email:
        identifiers.add(email.split('@', 1)[0])
    return {value for value in identifiers if value}


def actor_matches_author(user, author):
    if not author:
        return True
    if getattr(user, 'is_superuser', False):
        return True
    return author in _actor_identifiers(user)


def get_request_api_key(request):
    auth = getattr(request, 'auth', None)
    return auth if isinstance(auth, OpenAPIKey) else None


def can_read_repo(request, repo):
    if (getattr(repo, 'visibility', 'public') or 'public') == 'public':
        return True
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', False):
        return False
    api_key = get_request_api_key(request)
    if api_key and api_key.key_type not in {
        OpenAPIKey.KeyType.READ,
        OpenAPIKey.KeyType.WRITE,
        OpenAPIKey.KeyType.ADMIN,
    }:
        return False
    return actor_matches_author(user, getattr(repo, 'author', ''))


def can_write_repo(request, repo=None):
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', False):
        return False
    if getattr(user, 'is_superuser', False):
        return True

    api_key = get_request_api_key(request)
    if api_key and api_key.key_type not in {
        OpenAPIKey.KeyType.WRITE,
        OpenAPIKey.KeyType.ADMIN,
    }:
        return False
    if repo is None:
        return True
    return actor_matches_author(user, getattr(repo, 'author', ''))


def default_author_for_user(user):
    identifiers = list(_actor_identifiers(user))
    username = (getattr(user, 'username', '') or '').strip()
    if username:
        return username
    return identifiers[0] if identifiers else 'anonymous'


class HubOpenAPIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return None
        if len(auth) != 2:
            raise AuthenticationFailed('Invalid authorization header')

        try:
            token = auth[1].decode('utf-8')
        except UnicodeDecodeError as exc:
            raise AuthenticationFailed('Invalid authorization token') from exc

        if not token.startswith('sk-'):
            return None

        api_key = OpenAPIKey.objects.select_related('user').filter(key=token).first()
        if not api_key or not api_key.is_valid():
            raise AuthenticationFailed('Invalid API key')

        OpenAPIKey.objects.filter(pk=api_key.pk).update(
            usage_count=F('usage_count') + 1,
            last_used_at=timezone.now(),
        )
        api_key.refresh_from_db(fields=['usage_count', 'last_used_at'])
        return (api_key.user, api_key)
