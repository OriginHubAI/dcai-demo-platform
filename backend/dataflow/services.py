from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from django.conf import settings


IGNORE_NAMES = {
    '.git',
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    '.ruff_cache',
    '.DS_Store',
}


PACKAGE_METADATA = {
    'agentic_rag': {
        'title': 'Agentic RAG',
        'description': 'Operators for retrieval-augmented generation and agentic knowledge workflows.',
        'category': 'rag',
        'tags': ['rag', 'agent', 'retrieval'],
    },
    'chemistry': {
        'title': 'Chemistry',
        'description': 'Domain operators for chemistry parsing, evaluation, and data generation.',
        'category': 'science',
        'tags': ['chemistry', 'science', 'domain'],
    },
    'code': {
        'title': 'Code',
        'description': 'Operators for code-centric QA generation, filtering, and evaluation.',
        'category': 'code',
        'tags': ['code', 'qa', 'evaluation'],
    },
    'conversations': {
        'title': 'Conversations',
        'description': 'Operators for conversation datasets and multi-turn data preparation.',
        'category': 'text',
        'tags': ['conversation', 'chat', 'text'],
    },
    'core_speech': {
        'title': 'Core Speech',
        'description': 'Core speech operators for multimodal pipeline construction.',
        'category': 'multimodal',
        'tags': ['speech', 'audio', 'multimodal'],
    },
    'core_text': {
        'title': 'Core Text',
        'description': 'Core text operators used in canonical DataFlow pipelines.',
        'category': 'core',
        'tags': ['core', 'text', 'pipeline'],
    },
    'core_vision': {
        'title': 'Core Vision',
        'description': 'Core vision operators for captioning and image-centric workflows.',
        'category': 'multimodal',
        'tags': ['vision', 'image', 'multimodal'],
    },
    'general_text': {
        'title': 'General Text',
        'description': 'General-purpose text data operators for filtering, evaluation, and generation.',
        'category': 'text',
        'tags': ['text', 'general', 'operators'],
    },
    'knowledge_cleaning': {
        'title': 'Knowledge Cleaning',
        'description': 'Operators for cleaning and structuring knowledge sources for RAG.',
        'category': 'rag',
        'tags': ['knowledge-base', 'rag', 'cleaning'],
    },
    'pdf2vqa': {
        'title': 'PDF2VQA',
        'description': 'Operators that convert document sources into visual question answering data.',
        'category': 'document',
        'tags': ['pdf', 'vqa', 'document'],
    },
    'reasoning': {
        'title': 'Reasoning',
        'description': 'Operators for chain-of-thought, reasoning enrichment, and difficulty grading.',
        'category': 'reasoning',
        'tags': ['reasoning', 'cot', 'evaluation'],
    },
    'text2sql': {
        'title': 'Text2SQL',
        'description': 'Operators for text-to-SQL data generation and evaluation.',
        'category': 'structured-data',
        'tags': ['sql', 'text2sql', 'structured-data'],
    },
    'text_pt': {
        'title': 'Text PT',
        'description': 'Operators for pre-training data creation and processing.',
        'category': 'training',
        'tags': ['pretrain', 'text', 'training'],
    },
    'text_sft': {
        'title': 'Text SFT',
        'description': 'Operators tailored to supervised fine-tuning data pipelines.',
        'category': 'training',
        'tags': ['sft', 'text', 'training'],
    },
}


@dataclass
class PackageRecord:
    id: str
    name: str
    version: str
    description: str
    category: str
    tags: list[str]
    author: str
    license: str
    downloads: int
    likes: int
    repo_path: str
    last_modified: str

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'category': self.category,
            'tags': self.tags,
            'author': self.author,
            'license': self.license,
            'downloads': self.downloads,
            'likes': self.likes,
            'lastModified': self.last_modified,
            'type': 'workspace',
        }


class DataFlowCatalog:
    def __init__(self):
        default_root = Path(__file__).resolve().parents[3] / 'DataFlow' / 'dataflow' / 'operators'
        self.root = Path(getattr(settings, 'DATAFLOW_OPERATORS_ROOT', default_root)).resolve()

    def _package_version(self) -> str:
        return getattr(settings, 'DATAFLOW_WORKSPACE_VERSION', 'workspace')

    def _score(self, package_id: str) -> tuple[int, int]:
        return 10000 + (abs(hash(package_id)) % 50000), 200 + (abs(hash(f'{package_id}:like')) % 2000)

    def _last_modified(self, package_path: Path) -> str:
        latest = max((item.stat().st_mtime for item in package_path.rglob('*')), default=package_path.stat().st_mtime)
        return datetime.utcfromtimestamp(latest).strftime('%Y-%m-%d')

    def list_packages(self) -> list[dict]:
        if not self.root.exists():
            return []

        packages = []
        for package_path in sorted(self.root.iterdir()):
            if not package_path.is_dir() or package_path.name in IGNORE_NAMES:
                continue
            meta = PACKAGE_METADATA.get(package_path.name, {})
            downloads, likes = self._score(package_path.name)
            packages.append(
                PackageRecord(
                    id=package_path.name,
                    name=meta.get('title', package_path.name.replace('_', ' ').title()),
                    version=self._package_version(),
                    description=meta.get('description', f'Workspace package for {package_path.name}.'),
                    category=meta.get('category', 'workspace'),
                    tags=meta.get('tags', [package_path.name]),
                    author='OpenDCAI',
                    license='apache-2.0',
                    downloads=downloads,
                    likes=likes,
                    repo_path=str(package_path),
                    last_modified=self._last_modified(package_path),
                ).to_dict()
            )
        return packages

    def get_package(self, package_id: str) -> dict | None:
        for package in self.list_packages():
            if package['id'] == package_id:
                return package
        return None

    def get_package_repo_path(self, package_id: str) -> str:
        return str(self._package_root(package_id))

    def get_repo_root(self) -> str:
        configured_root = getattr(settings, 'DATAFLOW_REPO_ROOT', '')
        if configured_root:
            return str(Path(configured_root).resolve())
        return str(self.root.parents[1])

    def _package_root(self, package_id: str) -> Path:
        target = (self.root / package_id).resolve()
        if self.root not in target.parents or not target.exists() or not target.is_dir():
            raise FileNotFoundError('Package not found')
        return target

    def _safe_path(self, package_id: str, relative_path: str = '') -> Path:
        root = self._package_root(package_id)
        target = (root / relative_path).resolve()
        if target != root and root not in target.parents:
            raise PermissionError('Requested path escapes package root')
        return target

    def build_tree(self, package_id: str) -> dict:
        root = self._package_root(package_id)

        def walk(path: Path) -> dict:
            node = {
                'name': path.name,
                'path': '' if path == root else str(path.relative_to(root)),
                'type': 'directory' if path.is_dir() else 'file',
            }
            if path.is_dir():
                node['children'] = [
                    walk(child)
                    for child in sorted(path.iterdir(), key=lambda item: (item.is_file(), item.name.lower()))
                    if child.name not in IGNORE_NAMES
                ]
            else:
                node['size'] = path.stat().st_size
            return node

        return walk(root)

    def read_file(self, package_id: str, relative_path: str) -> dict:
        root = self._package_root(package_id)
        target = self._safe_path(package_id, relative_path)
        if not target.exists() or not target.is_file():
            raise FileNotFoundError('File not found')
        return {
            'path': str(target.relative_to(root)),
            'content': target.read_text(encoding='utf-8', errors='replace'),
            'size': target.stat().st_size,
        }

    def run_package_test(self, package_id: str) -> dict:
        repo_path = self.get_package_repo_path(package_id)

        command = ['python', '-m', 'compileall', repo_path]
        result = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        return {
            'package_id': package_id,
            'command': ' '.join(command),
            'success': result.returncode == 0,
            'returncode': result.returncode,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip(),
        }


catalog = DataFlowCatalog()
