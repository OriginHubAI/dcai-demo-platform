from django.db import migrations, models
import django.db.models.deletion


def seed_knowledge_hub(apps, schema_editor):
    KnowledgeRepo = apps.get_model('hub', 'KnowledgeRepo')
    KnowledgeVersion = apps.get_model('hub', 'KnowledgeVersion')
    KnowledgeFile = apps.get_model('hub', 'KnowledgeFile')
    KnowledgeBuild = apps.get_model('hub', 'KnowledgeBuild')

    specs = [
        {
            'repo_id': 'OpenDCAI/math-olympiad-kb',
            'namespace': 'OpenDCAI',
            'slug': 'math-olympiad-kb',
            'author': 'OpenDCAI',
            'name': 'Math Olympiad Knowledge Base',
            'description': 'Knowledge repository built from Olympiad problem statements, solutions, and theorem references.',
            'summary': 'Knowledge repo with retrieval and graph metadata.',
            'visibility': 'public',
            'status': 'ready',
            'source_dataset': 'OpenDCAI/math-olympiad-problems',
            'source_files': ['train.jsonl', 'README.md'],
            'document_count': 15420,
            'file_count': 2,
            'downloads': 3200,
            'likes': 280,
            'tags': ['knowledge-base', 'math', 'rag'],
            'metadata': {'domain': 'mathematics', 'modality': 'text'},
            'card_sections': [
                {'title': 'Overview', 'content': 'A retrieval-oriented knowledge base created from math olympiad sources.'},
                {'title': 'Build Pipeline', 'content': 'Documents are parsed, chunked, embedded, indexed, and linked into a graph.'},
            ],
            'vector_store': {
                'provider': 'faiss',
                'collection': 'math_olympiad_kb',
                'dimension': 1536,
                'vectorCount': 15420,
                'indexType': 'IVF_FLAT',
            },
            'pipeline': {
                'stages': [
                    {'name': 'parse', 'status': 'completed', 'label': 'Document Parsing'},
                    {'name': 'chunk', 'status': 'completed', 'label': 'Text Chunking'},
                    {'name': 'embed', 'status': 'completed', 'label': 'Embedding'},
                    {'name': 'index', 'status': 'completed', 'label': 'Index Building'},
                    {'name': 'graph', 'status': 'completed', 'label': 'Knowledge Graph'},
                ],
                'lastRun': '2026-03-24T00:00:00+00:00',
                'progress': 100,
            },
            'knowledge_graph': {
                'enabled': True,
                'entityCount': 3280,
                'relationCount': 8540,
                'lastUpdated': '2026-03-24T00:00:00+00:00',
            },
            'retrieval': {'topK': 8, 'reranker': 'bge-reranker-base', 'chunkSize': 768},
            'mcp': {'enabled': True, 'endpoint': '/mcp/kb/math-olympiad-kb', 'tools': ['search', 'query', 'traverse']},
            'versions': [
                {
                    'revision': 'main',
                    'commit_sha': 'kbmath001',
                    'manifest': {'sourceDataset': 'OpenDCAI/math-olympiad-problems'},
                    'is_latest': True,
                    'files': [
                        {
                            'path': 'README.md',
                            'file_type': 'markdown',
                            'size_bytes': 512,
                            'size_label': '512B',
                            'preview_text': '# Math Olympiad Knowledge Base\n\nKnowledge card for the repository.',
                            'sha256': 'sha256:kb-math-readme',
                            'sort_order': 0,
                        },
                        {
                            'path': 'chunks/train.jsonl',
                            'file_type': 'jsonl',
                            'size_bytes': 2048,
                            'size_label': '2KB',
                            'row_count': 3,
                            'preview_rows': [
                                {'chunk_id': 'm1', 'text': 'If a+b=c, prove ...', 'doc_id': 'problem-1'},
                                {'chunk_id': 'm2', 'text': 'By Jensen inequality ...', 'doc_id': 'solution-4'},
                                {'chunk_id': 'm3', 'text': 'Consider the invariant ...', 'doc_id': 'problem-9'},
                            ],
                            'sha256': 'sha256:kb-math-chunks',
                            'sort_order': 1,
                        },
                    ],
                },
            ],
            'builds': [
                {
                    'trigger': 'seed',
                    'status': 'completed',
                    'progress': 100,
                    'stages': [
                        {'name': 'parse', 'status': 'completed'},
                        {'name': 'chunk', 'status': 'completed'},
                        {'name': 'embed', 'status': 'completed'},
                        {'name': 'index', 'status': 'completed'},
                        {'name': 'graph', 'status': 'completed'},
                    ],
                },
            ],
        },
        {
            'repo_id': 'OpenDCAI/chemistry-books-kb',
            'namespace': 'OpenDCAI',
            'slug': 'chemistry-books-kb',
            'author': 'OpenDCAI',
            'name': 'Chemistry Books Knowledge Base',
            'description': 'Knowledge repository for chemistry books with vector retrieval and graph extraction metadata.',
            'summary': 'Domain knowledge repo for chemistry retrieval workflows.',
            'visibility': 'public',
            'status': 'processing',
            'source_dataset': 'OpenDCAI/chemistry-books',
            'source_files': ['corpus.jsonl'],
            'document_count': 9800,
            'file_count': 2,
            'downloads': 1800,
            'likes': 140,
            'tags': ['knowledge-base', 'chemistry', 'domain'],
            'metadata': {'domain': 'chemistry', 'modality': 'text'},
            'card_sections': [
                {'title': 'Overview', 'content': 'Chemistry corpus converted into a retrieval-friendly knowledge repository.'},
            ],
            'vector_store': {
                'provider': 'faiss',
                'collection': 'chemistry_books_kb',
                'dimension': 1536,
                'vectorCount': 6200,
                'indexType': 'HNSW',
            },
            'pipeline': {
                'stages': [
                    {'name': 'parse', 'status': 'completed', 'label': 'Document Parsing'},
                    {'name': 'chunk', 'status': 'completed', 'label': 'Text Chunking'},
                    {'name': 'embed', 'status': 'running', 'label': 'Embedding'},
                    {'name': 'index', 'status': 'pending', 'label': 'Index Building'},
                    {'name': 'graph', 'status': 'pending', 'label': 'Knowledge Graph'},
                ],
                'lastRun': '2026-03-24T00:00:00+00:00',
                'progress': 60,
            },
            'knowledge_graph': {
                'enabled': False,
                'entityCount': 0,
                'relationCount': 0,
                'lastUpdated': None,
            },
            'retrieval': {'topK': 6, 'reranker': '', 'chunkSize': 768},
            'mcp': {'enabled': False, 'endpoint': '', 'tools': []},
            'versions': [
                {
                    'revision': 'main',
                    'commit_sha': 'kbchem001',
                    'manifest': {'sourceDataset': 'OpenDCAI/chemistry-books'},
                    'is_latest': True,
                    'files': [
                        {
                            'path': 'README.md',
                            'file_type': 'markdown',
                            'size_bytes': 384,
                            'size_label': '384B',
                            'preview_text': '# Chemistry Books KB\n\nBuild in progress.',
                            'sha256': 'sha256:kb-chem-readme',
                            'sort_order': 0,
                        },
                        {
                            'path': 'chunks/preview.jsonl',
                            'file_type': 'jsonl',
                            'size_bytes': 1024,
                            'size_label': '1KB',
                            'row_count': 2,
                            'preview_rows': [
                                {'chunk_id': 'c1', 'text': 'Covalent bonds involve electron sharing.', 'doc_id': 'chem-1'},
                                {'chunk_id': 'c2', 'text': 'Acid-base titration determines concentration.', 'doc_id': 'chem-2'},
                            ],
                            'sha256': 'sha256:kb-chem-chunks',
                            'sort_order': 1,
                        },
                    ],
                },
            ],
            'builds': [
                {
                    'trigger': 'seed',
                    'status': 'running',
                    'progress': 60,
                    'stages': [
                        {'name': 'parse', 'status': 'completed'},
                        {'name': 'chunk', 'status': 'completed'},
                        {'name': 'embed', 'status': 'running'},
                        {'name': 'index', 'status': 'pending'},
                        {'name': 'graph', 'status': 'pending'},
                    ],
                },
            ],
        },
    ]

    for spec in specs:
        versions = spec.pop('versions')
        builds = spec.pop('builds')
        repo = KnowledgeRepo.objects.create(**spec)
        for version_spec in versions:
            files = version_spec.pop('files')
            version = KnowledgeVersion.objects.create(repo=repo, **version_spec)
            for file_spec in files:
                KnowledgeFile.objects.create(version=version, **file_spec)
        for build_spec in builds:
            KnowledgeBuild.objects.create(repo=repo, **build_spec)


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeRepo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('repo_id', models.CharField(max_length=255, unique=True)),
                ('namespace', models.CharField(max_length=120)),
                ('slug', models.CharField(max_length=120)),
                ('author', models.CharField(max_length=120)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('summary', models.TextField(blank=True, default='')),
                ('visibility', models.CharField(default='public', max_length=32)),
                ('status', models.CharField(default='pending', max_length=32)),
                ('source_dataset', models.CharField(blank=True, default='', max_length=255)),
                ('source_files', models.JSONField(blank=True, default=list)),
                ('document_count', models.PositiveBigIntegerField(default=0)),
                ('file_count', models.PositiveIntegerField(default=0)),
                ('downloads', models.PositiveIntegerField(default=0)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('card_sections', models.JSONField(blank=True, default=list)),
                ('vector_store', models.JSONField(blank=True, default=dict)),
                ('pipeline', models.JSONField(blank=True, default=dict)),
                ('knowledge_graph', models.JSONField(blank=True, default=dict)),
                ('retrieval', models.JSONField(blank=True, default=dict)),
                ('mcp', models.JSONField(blank=True, default=dict)),
                ('hf_compatible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['repo_id'],
            },
        ),
        migrations.CreateModel(
            name='KnowledgeBuild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('trigger', models.CharField(default='manual', max_length=32)),
                ('status', models.CharField(default='queued', max_length=32)),
                ('progress', models.PositiveIntegerField(default=0)),
                ('stages', models.JSONField(blank=True, default=list)),
                ('error_message', models.TextField(blank=True, default='')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='hub.knowledgerepo')),
            ],
            options={
                'ordering': ['-created_at', '-id'],
            },
        ),
        migrations.CreateModel(
            name='KnowledgeVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('revision', models.CharField(max_length=120)),
                ('commit_sha', models.CharField(max_length=64)),
                ('manifest', models.JSONField(blank=True, default=dict)),
                ('is_latest', models.BooleanField(default=False)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='hub.knowledgerepo')),
            ],
            options={
                'ordering': ['-created_at', '-id'],
                'unique_together': {('repo', 'revision')},
            },
        ),
        migrations.CreateModel(
            name='KnowledgeFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('path', models.CharField(max_length=512)),
                ('file_type', models.CharField(max_length=64)),
                ('size_bytes', models.PositiveBigIntegerField(default=0)),
                ('size_label', models.CharField(default='0B', max_length=64)),
                ('row_count', models.PositiveBigIntegerField(blank=True, null=True)),
                ('preview_rows', models.JSONField(blank=True, default=list)),
                ('preview_text', models.TextField(blank=True, default='')),
                ('sha256', models.CharField(blank=True, default='', max_length=128)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='hub.knowledgeversion')),
            ],
            options={
                'ordering': ['sort_order', 'path'],
                'unique_together': {('version', 'path')},
            },
        ),
        migrations.RunPython(seed_knowledge_hub, migrations.RunPython.noop),
    ]
