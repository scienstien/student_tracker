from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from student_tracker.models import ClassSchedule, Subject, User
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates test records with older dates'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create a test professor
            professor = User.objects.create_user(
                username='old_professor',
                password='testpass123',
                user_type='professor'
            )

            # Create old subjects (7 months ago)
            old_date = timezone.now() - timedelta(days=30 * 7)
            subject1 = Subject.objects.create(
                name='Old Mathematics',
                professor=professor,
                created_at=old_date
            )
            subject2 = Subject.objects.create(
                name='Old Physics',
                professor=professor,
                created_at=old_date
            )

            # Create old schedules
            for subject in [subject1, subject2]:
                for weekday in range(2):  # Create schedules for Monday and Tuesday
                    ClassSchedule.objects.create(
                        subject=subject,
                        weekday=weekday,
                        start_time='09:00',
                        end_time='10:30',
                        is_regular=True,
                        created_at=old_date
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully created old test records (7 months old)'
                )
            ) 