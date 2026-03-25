from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from hub.sync import REPO_TYPES, export_bare_git_revision, revision_from_ref, sync_repo_revision


class Command(BaseCommand):
    help = 'Sync a locally pushed bare Git repository back into DCAI Hub metadata and preview storage.'

    def add_arguments(self, parser):
        parser.add_argument('--repo-type', required=True, choices=sorted(REPO_TYPES.keys()))
        parser.add_argument('--repo-id', required=True)
        parser.add_argument('--git-dir', required=True)
        parser.add_argument('--refname', required=True)

    def handle(self, *args, **options):
        repo_type = options['repo_type']
        repo_id = options['repo_id'].strip()
        git_dir = Path(options['git_dir']).resolve()
        refname = options['refname'].strip()

        revision = revision_from_ref(refname)
        if not revision:
            self.stdout.write(self.style.WARNING(f'Skipping unsupported ref: {refname}'))
            return

        repo = REPO_TYPES[repo_type]['repo_model'].objects.filter(repo_id=repo_id).first()
        if not repo:
            raise CommandError(f'Repository not found: {repo_id}')
        if not git_dir.exists():
            raise CommandError(f'Git directory not found: {git_dir}')

        exported = export_bare_git_revision(git_dir, revision)
        sync_repo_revision(
            repo_type,
            repo,
            revision,
            exported['commitSha'],
            exported['files'],
            provider_name='localgit',
            artifact_uri=str(git_dir),
            provider_binding={
                'provider': 'localgit',
                'repoType': repo_type,
                'cloneUrl': str(git_dir),
                'pushUrl': str(git_dir),
                'localPath': str(git_dir),
                'defaultBranch': getattr(repo, 'default_revision', '') or 'main',
            },
            provider_payload={
                'branch': revision,
                'commitSha': exported['commitSha'],
                'treeUrl': str(git_dir),
                'refname': refname,
                'fileCount': len(exported['files']),
                'source': 'git-push',
            },
        )
        self.stdout.write(self.style.SUCCESS(f'Synchronized {repo_id}@{revision} ({exported["commitSha"][:12]})'))
