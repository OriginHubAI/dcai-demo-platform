"""
Custom Admin Views
"""
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """Get dashboard statistics"""
    from datetime import timedelta
    from django.utils import timezone
    
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    
    # User stats
    total_users = User.objects.count()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    new_users_7d = User.objects.filter(date_joined__date__gte=last_7_days).count()
    new_users_30d = User.objects.filter(date_joined__date__gte=last_30_days).count()
    
    # Active users (users who logged in recently)
    recent_login = timezone.now() - timedelta(days=7)
    active_users_7d = User.objects.filter(last_login__gte=recent_login).count()
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'users': {
                'total': total_users,
                'new_today': new_users_today,
                'new_7d': new_users_7d,
                'new_30d': new_users_30d,
                'active_7d': active_users_7d,
            }
        }
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def system_health(request):
    """Get system health status"""
    from django.db import connection
    from django.core.cache import cache
    
    # Database check
    db_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        db_ok = False
    
    # Cache check
    cache_ok = True
    try:
        cache.set('health_check', 'ok', 10)
        cache_ok = cache.get('health_check') == 'ok'
    except Exception:
        cache_ok = False
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'database': 'healthy' if db_ok else 'unhealthy',
            'cache': 'healthy' if cache_ok else 'unhealthy',
            'overall': 'healthy' if (db_ok and cache_ok) else 'degraded'
        }
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list(request):
    """List all users with pagination"""
    from core.pagination import CustomPagination
    
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    search = request.query_params.get('search', '')
    is_active = request.query_params.get('is_active')
    
    users = User.objects.all().order_by('-date_joined')
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(full_name__icontains=search)
        )
    
    if is_active is not None:
        users = users.filter(is_active=is_active.lower() == 'true')
    
    total = users.count()
    start = (page - 1) * page_size
    end = start + page_size
    users = users[start:end]
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': [{
                'id': str(u.id),
                'username': u.username,
                'email': u.email,
                'full_name': u.full_name,
                'is_active': u.is_active,
                'is_staff': u.is_staff,
                'date_joined': u.date_joined.isoformat(),
                'last_login': u.last_login.isoformat() if u.last_login else None,
            } for u in users],
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def user_action(request, user_id):
    """Perform action on user (activate, deactivate, delete)"""
    action = request.data.get('action')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({
            'code': 404,
            'msg': 'User not found',
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)
    
    if action == 'activate':
        user.is_active = True
        user.save(update_fields=['is_active'])
    elif action == 'deactivate':
        user.is_active = False
        user.save(update_fields=['is_active'])
    elif action == 'delete':
        user.delete()
    else:
        return Response({
            'code': 400,
            'msg': 'Invalid action',
            'data': {}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def analytics(request):
    """Get analytics data"""
    from datetime import timedelta
    from django.utils import timezone
    
    days = int(request.query_params.get('days', 30))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    
    # Placeholder for analytics - in production, this would aggregate data
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
            },
            'daily_active_users': [],
            'api_usage': [],
            'storage_usage': {},
        }
    })
