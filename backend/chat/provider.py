import json
from dataclasses import dataclass
from typing import Iterable

import httpx
from django.conf import settings


class ChatProviderError(RuntimeError):
    pass


@dataclass
class ChatCompletionResult:
    model: str
    content: str
    usage: dict


class OpenAICompatibleChatProvider:
    def __init__(self):
        self.base_url = getattr(settings, 'LLM_PROVIDER_BASE_URL', '').strip()
        self.api_key = getattr(settings, 'LLM_PROVIDER_API_KEY', '').strip()
        self.default_model = getattr(settings, 'LLM_DEFAULT_MODEL', 'gpt-4o')
        self.timeout = getattr(settings, 'LLM_REQUEST_TIMEOUT', 120)
        self.available_models = getattr(settings, 'LLM_AVAILABLE_MODELS', [])

    @property
    def configured(self) -> bool:
        return bool(self.base_url and self.api_key)

    def _require_config(self):
        if not self.configured:
            raise ChatProviderError('LLM provider is not configured. Set LLM_PROVIDER_BASE_URL and LLM_PROVIDER_API_KEY.')

    def _api_root(self) -> str:
        base = self.base_url.rstrip('/')
        if base.endswith('/v1'):
            return base
        return f'{base}/v1'

    def _headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def list_models(self) -> list[str]:
        if self.available_models:
            return self.available_models

        if not self.configured:
            return [self.default_model]

        try:
            with httpx.Client(timeout=15) as client:
                response = client.get(f'{self._api_root()}/models', headers=self._headers())
            response.raise_for_status()
        except Exception:
            return [self.default_model]

        payload = response.json()
        models = [item.get('id') for item in payload.get('data', []) if item.get('id')]
        if self.default_model and self.default_model not in models:
            models.insert(0, self.default_model)
        return models or [self.default_model]

    def complete(self, messages: list[dict], model: str | None = None, temperature: float = 0.7) -> ChatCompletionResult:
        self._require_config()
        payload = {
            'model': model or self.default_model,
            'messages': messages,
            'temperature': temperature,
            'stream': False,
        }
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f'{self._api_root()}/chat/completions',
                headers=self._headers(),
                json=payload,
            )
        response.raise_for_status()
        data = response.json()
        content = data['choices'][0]['message']['content']
        return ChatCompletionResult(
            model=data.get('model') or payload['model'],
            content=content,
            usage=data.get('usage') or {},
        )

    def stream(self, messages: list[dict], model: str | None = None, temperature: float = 0.7) -> Iterable[str]:
        self._require_config()
        payload = {
            'model': model or self.default_model,
            'messages': messages,
            'temperature': temperature,
            'stream': True,
        }

        with httpx.Client(timeout=None) as client:
            with client.stream(
                'POST',
                f'{self._api_root()}/chat/completions',
                headers=self._headers(),
                json=payload,
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    if isinstance(line, bytes):
                        line = line.decode('utf-8', errors='ignore')
                    if not line.startswith('data:'):
                        continue
                    data = line[5:].strip()
                    if data == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    choices = chunk.get('choices') or []
                    if not choices:
                        continue
                    delta = choices[0].get('delta', {})
                    content = delta.get('content')
                    if content:
                        yield content
