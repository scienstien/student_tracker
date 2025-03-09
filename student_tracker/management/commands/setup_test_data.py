from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from student_tracker.models import Subject, ClassSchedule
from django.utils import timezone
from datetime import time

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up test data for the student tracking system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin',
                'admin@example.com',
                'admin123',
                user_type='professor'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Create professors with their specific subjects
        professors_data = [
            ('prof_cs', 'Dr. S Saroja', ['CS Class']),
            ('prof_civil', 'Dr. Mashuda Sultana', ['Civil']),
            ('prof_energy', 'Dr. Ruben Sudhakar', ['Energy and Environment']),
            ('prof_thermo', 'Dr. S. Anand', ['Thermodynamic']),
            ('prof_physics', 'Dr. M.C. Santoshkumar', ['Physics']),
            ('prof_math', 'Dr. R. Gowmathi', ['Mathematics']),
        ]

        # Create professors and their subjects
        for username, full_name, subjects in professors_data:
            if not User.objects.filter(username=username).exists():
                professor = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    user_type='professor',
                    first_name=full_name
                )
                self.stdout.write(f'Created professor: {username}')

                # Create subjects for this professor
                for subject_name in subjects:
                    if not Subject.objects.filter(name=subject_name).exists():
                        Subject.objects.create(
                            name=subject_name,
                            professor=professor
                        )
                        self.stdout.write(f'Created subject: {subject_name} for {username}')

        # Create class representative
        if not User.objects.filter(username='class_rep1').exists():
            class_rep = User.objects.create_user(
                username='class_rep1',
                email='class_rep1@example.com',
                password='password123',
                user_type='class_rep',
                first_name='Class Representative',
                last_name='1',
                is_staff=True  # Give staff permissions to manage schedules
            )
            self.stdout.write('Created class representative')
        else:
            class_rep = User.objects.get(username='class_rep1')
            class_rep.user_type = 'class_rep'  # Ensure correct user type
            class_rep.is_staff = True  # Ensure staff permissions
            class_rep.save()
            self.stdout.write('Updated class representative permissions')

        # Create students with roll numbers
        for roll_no in range(112124001, 112124080):
            username = f'student_{roll_no}'
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    user_type='student',
                    first_name=f'Student {roll_no}'
                )
                self.stdout.write(f'Created student: {username}')

        # Create regular class schedules for each subject
        schedule_data = [
            # Computer Science Department
            ('CS Class', 1, time(9, 0), time(10, 30)),  # Tuesday

            # Civil Engineering Department
            ('Civil', 2, time(11, 0), time(12, 30)),  # Wednesday

            # Energy Engineering Department
            ('Energy and Environment', 3, time(14, 0), time(15, 30)),  # Thursday

            # Thermodynamics Department
            ('Thermodynamic', 4, time(14, 0), time(15, 30)),  # Friday

            # Physics Department
            ('Physics', 0, time(9, 0), time(10, 30)),  # Monday

            # Mathematics Department
            ('Mathematics', 0, time(11, 0), time(12, 30)),  # Monday
        ]

        for subject_name, weekday, start_time, end_time in schedule_data:
            try:
                subject = Subject.objects.get(name=subject_name)
                if not ClassSchedule.objects.filter(
                    subject=subject,
                    weekday=weekday,
                    start_time=start_time,
                    end_time=end_time
                ).exists():
                    schedule = ClassSchedule.objects.create(
                        subject=subject,
                        weekday=weekday,
                        start_time=start_time,
                        end_time=end_time,
                        is_regular=True,
                        created_by=class_rep
                    )
                    self.stdout.write(f'Created schedule for {subject_name} on {weekday}')
            except Subject.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Subject {subject_name} not found'))

        self.stdout.write(self.style.SUCCESS('Test data creation completed')) 