from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RepoProviderMixin(models.Model):
    sync_status = models.CharField(max_length=32, default='local')
    provider_bindings = models.JSONField(default=dict, blank=True)
    default_revision = models.CharField(max_length=120, default='main')

    class Meta:
        abstract = True


class VersionProviderMixin(models.Model):
    provider_revision = models.CharField(max_length=255, blank=True, default='')
    provider_commit = models.CharField(max_length=255, blank=True, default='')
    artifact_uri = models.CharField(max_length=1024, blank=True, default='')
    provider_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        abstract = True


class DatasetRepo(TimestampedModel, RepoProviderMixin):
    repo_id = models.CharField(max_length=255, unique=True)
    namespace = models.CharField(max_length=120)
    slug = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    name = models.CharField(max_length=255)
    task = models.CharField(max_length=120)
    domain = models.CharField(max_length=120)
    modality = models.CharField(max_length=120)
    language = models.CharField(max_length=64, default='en')
    license = models.CharField(max_length=120, default='apache-2.0')
    description = models.TextField()
    summary = models.TextField(blank=True, default='')
    visibility = models.CharField(max_length=32, default='public')
    dataset_type = models.CharField(max_length=32, blank=True, default='')
    readonly = models.BooleanField(default=False)
    downloads = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    row_count = models.PositiveBigIntegerField(default=0)
    size_label = models.CharField(max_length=64, default='0B')
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    card_sections = models.JSONField(default=list, blank=True)
    parent_repo_id = models.CharField(max_length=255, blank=True, default='')
    derived_repo_ids = models.JSONField(default=list, blank=True)
    hf_compatible = models.BooleanField(default=True)

    class Meta:
        ordering = ['repo_id']

    def __str__(self):
        return self.repo_id


class DatasetVersion(TimestampedModel, VersionProviderMixin):
    repo = models.ForeignKey(DatasetRepo, related_name='versions', on_delete=models.CASCADE)
    revision = models.CharField(max_length=120)
    commit_sha = models.CharField(max_length=64)
    manifest = models.JSONField(default=dict, blank=True)
    row_count = models.PositiveBigIntegerField(default=0)
    size_label = models.CharField(max_length=64, default='0B')
    is_latest = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at', '-id']
        unique_together = ('repo', 'revision')

    def __str__(self):
        return f'{self.repo.repo_id}@{self.revision}'


class DatasetFile(TimestampedModel):
    version = models.ForeignKey(DatasetVersion, related_name='files', on_delete=models.CASCADE)
    path = models.CharField(max_length=512)
    file_type = models.CharField(max_length=64)
    size_bytes = models.PositiveBigIntegerField(default=0)
    size_label = models.CharField(max_length=64, default='0B')
    split = models.CharField(max_length=64, blank=True, default='')
    row_count = models.PositiveBigIntegerField(null=True, blank=True)
    preview_rows = models.JSONField(default=list, blank=True)
    preview_text = models.TextField(blank=True, default='')
    sha256 = models.CharField(max_length=128, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'path']
        unique_together = ('version', 'path')

    def __str__(self):
        return f'{self.version.repo.repo_id}:{self.path}'


class ModelRepo(TimestampedModel, RepoProviderMixin):
    repo_id = models.CharField(max_length=255, unique=True)
    namespace = models.CharField(max_length=120)
    slug = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    name = models.CharField(max_length=255)
    pipeline_tag = models.CharField(max_length=120)
    library = models.CharField(max_length=120, default='transformers')
    language = models.CharField(max_length=64, default='en')
    license = models.CharField(max_length=120, default='apache-2.0')
    description = models.TextField()
    summary = models.TextField(blank=True, default='')
    visibility = models.CharField(max_length=32, default='public')
    downloads = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    base_model = models.CharField(max_length=255, blank=True, default='')
    dataset = models.CharField(max_length=255, blank=True, default='')
    tags = models.JSONField(default=list, blank=True)
    metrics = models.JSONField(default=list, blank=True)
    card_sections = models.JSONField(default=list, blank=True)
    hf_compatible = models.BooleanField(default=True)

    class Meta:
        ordering = ['repo_id']

    def __str__(self):
        return self.repo_id


class ModelVersion(TimestampedModel, VersionProviderMixin):
    repo = models.ForeignKey(ModelRepo, related_name='versions', on_delete=models.CASCADE)
    revision = models.CharField(max_length=120)
    commit_sha = models.CharField(max_length=64)
    framework = models.CharField(max_length=120, default='transformers')
    params_label = models.CharField(max_length=64, blank=True, default='')
    quantization = models.CharField(max_length=64, blank=True, default='')
    is_latest = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at', '-id']
        unique_together = ('repo', 'revision')

    def __str__(self):
        return f'{self.repo.repo_id}@{self.revision}'


class ModelFile(TimestampedModel):
    version = models.ForeignKey(ModelVersion, related_name='files', on_delete=models.CASCADE)
    path = models.CharField(max_length=512)
    file_type = models.CharField(max_length=64)
    size_bytes = models.PositiveBigIntegerField(default=0)
    size_label = models.CharField(max_length=64, default='0B')
    sha256 = models.CharField(max_length=128, blank=True, default='')
    preview_text = models.TextField(blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'path']
        unique_together = ('version', 'path')

    def __str__(self):
        return f'{self.version.repo.repo_id}:{self.path}'


class KnowledgeRepo(TimestampedModel, RepoProviderMixin):
    repo_id = models.CharField(max_length=255, unique=True)
    namespace = models.CharField(max_length=120)
    slug = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    name = models.CharField(max_length=255)
    description = models.TextField()
    summary = models.TextField(blank=True, default='')
    visibility = models.CharField(max_length=32, default='public')
    status = models.CharField(max_length=32, default='pending')
    source_dataset = models.CharField(max_length=255, blank=True, default='')
    source_files = models.JSONField(default=list, blank=True)
    document_count = models.PositiveBigIntegerField(default=0)
    file_count = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    card_sections = models.JSONField(default=list, blank=True)
    vector_store = models.JSONField(default=dict, blank=True)
    pipeline = models.JSONField(default=dict, blank=True)
    knowledge_graph = models.JSONField(default=dict, blank=True)
    retrieval = models.JSONField(default=dict, blank=True)
    mcp = models.JSONField(default=dict, blank=True)
    hf_compatible = models.BooleanField(default=True)

    class Meta:
        ordering = ['repo_id']

    def __str__(self):
        return self.repo_id


class KnowledgeVersion(TimestampedModel, VersionProviderMixin):
    repo = models.ForeignKey(KnowledgeRepo, related_name='versions', on_delete=models.CASCADE)
    revision = models.CharField(max_length=120)
    commit_sha = models.CharField(max_length=64)
    manifest = models.JSONField(default=dict, blank=True)
    is_latest = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at', '-id']
        unique_together = ('repo', 'revision')

    def __str__(self):
        return f'{self.repo.repo_id}@{self.revision}'


class KnowledgeFile(TimestampedModel):
    version = models.ForeignKey(KnowledgeVersion, related_name='files', on_delete=models.CASCADE)
    path = models.CharField(max_length=512)
    file_type = models.CharField(max_length=64)
    size_bytes = models.PositiveBigIntegerField(default=0)
    size_label = models.CharField(max_length=64, default='0B')
    row_count = models.PositiveBigIntegerField(null=True, blank=True)
    preview_rows = models.JSONField(default=list, blank=True)
    preview_text = models.TextField(blank=True, default='')
    sha256 = models.CharField(max_length=128, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'path']
        unique_together = ('version', 'path')

    def __str__(self):
        return f'{self.version.repo.repo_id}:{self.path}'


class KnowledgeBuild(TimestampedModel):
    repo = models.ForeignKey(KnowledgeRepo, related_name='builds', on_delete=models.CASCADE)
    trigger = models.CharField(max_length=32, default='manual')
    status = models.CharField(max_length=32, default='queued')
    progress = models.PositiveIntegerField(default=0)
    stages = models.JSONField(default=list, blank=True)
    error_message = models.TextField(blank=True, default='')
    provider_job_id = models.CharField(max_length=255, blank=True, default='')
    provider_status = models.CharField(max_length=64, blank=True, default='')
    provider_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'{self.repo.repo_id}:{self.status}'
