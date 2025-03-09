from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('class_rep', 'Class Representative')
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='subjects')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class ClassSchedule(models.Model):
    WEEKDAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    )
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_regular = models.BooleanField(default=True)  # True for regular classes, False for special classes
    date = models.DateField(null=True, blank=True)  # Only for special classes
    is_cancelled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['weekday', 'start_time']
    
    def __str__(self):
        if self.is_regular:
            return f"{self.subject.name} - {self.get_weekday_display()} {self.start_time}"
        return f"{self.subject.name} - Special Class on {self.date} at {self.start_time}"
    
    def can_mark_attendance(self):
        now = timezone.localtime(timezone.now())  # Convert to local time
        class_date = self.date if not self.is_regular else now.date()
        
        # Create datetime objects in local time
        class_start = timezone.localtime(
            timezone.make_aware(
                timezone.datetime.combine(class_date, self.start_time)
            )
        )
        class_end = timezone.localtime(
            timezone.make_aware(
                timezone.datetime.combine(class_date, self.end_time)
            )
        )
        attendance_end = class_end + timedelta(minutes=30)
        
        # Log the times for debugging
        logger.info(f"Now: {now}")
        logger.info(f"Class start: {class_start}")
        logger.info(f"Class end: {class_end}")
        logger.info(f"Attendance end: {attendance_end}")
        logger.info(f"Can mark: {not self.is_cancelled and class_start <= now <= attendance_end}")
        
        return (
            not self.is_cancelled and
            class_start <= now <= attendance_end
        )

class Attendance(models.Model):
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_attendances')
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['class_schedule', 'student']
    
    def __str__(self):
        return f"{self.student.username} - {self.class_schedule} - {'Present' if self.is_present else 'Absent'}" 