from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import shutil
import os
from django.conf import settings
from student_tracker.models import ClassSchedule, Subject
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Cleans up old semester data and creates a backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--semester',
            type=str,
            help='Specify semester to clean (e.g., "Spring-2024")'
        )
        parser.add_argument(
            '--older-than',
            type=int,
            default=6,
            help='Delete data older than X months (default: 6)'
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup before deletion'
        )

    def handle(self, *args, **options):
        # Create backup directory if it doesn't exist
        backup_dir = settings.BASE_DIR / 'backups'
        backup_dir.mkdir(exist_ok=True)

        # Create backup if requested
        if options['backup']:
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            backup_path = backup_dir / f'db_backup_{timestamp}.sqlite3'
            self.stdout.write(f'Creating backup at {backup_path}')
            shutil.copy2(settings.DATABASES['default']['NAME'], backup_path)

        # Calculate cutoff date
        months = options['older_than']
        cutoff_date = timezone.now() - timedelta(days=30*months)

        # Delete old schedules
        old_schedules = ClassSchedule.objects.filter(created_at__lt=cutoff_date)
        count_schedules = old_schedules.count()
        old_schedules.delete()

        # Delete old subjects
        old_subjects = Subject.objects.filter(created_at__lt=cutoff_date)
        count_subjects = old_subjects.count()
        old_subjects.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cleaned up {count_schedules} schedules and {count_subjects} subjects older than {months} months'
            )
        ) 