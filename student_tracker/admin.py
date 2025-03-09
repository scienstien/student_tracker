from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subject, ClassSchedule, Attendance
from django.utils import timezone
from datetime import timedelta
import shutil
from django.conf import settings
from django.contrib import messages

def cleanup_old_data(modeladmin, request, queryset):
    # Create backup directory if it doesn't exist
    backup_dir = settings.BASE_DIR / 'backups'
    backup_dir.mkdir(exist_ok=True)

    # Create backup
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f'db_backup_{timestamp}.sqlite3'
    shutil.copy2(settings.DATABASES['default']['NAME'], backup_path)
    
    # Calculate cutoff date (6 months ago)
    cutoff_date = timezone.now() - timedelta(days=30*6)
    
    # Delete old schedules
    old_schedules = ClassSchedule.objects.filter(created_at__lt=cutoff_date)
    schedules_count = old_schedules.count()
    old_schedules.delete()
    
    # Delete old subjects
    old_subjects = Subject.objects.filter(created_at__lt=cutoff_date)
    subjects_count = old_subjects.count()
    old_subjects.delete()
    
    messages.success(
        request, 
        f'Successfully cleaned up {schedules_count} schedules and {subjects_count} subjects older than 6 months. '
        f'Backup created at {backup_path}'
    )

cleanup_old_data.short_description = "Clean up data older than 6 months"

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'user_type', 'email', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type',)}),
    )

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'professor', 'created_at')
    list_filter = ('professor', 'created_at')
    search_fields = ('name', 'professor__username')
    actions = [cleanup_old_data]

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'weekday', 'start_time', 'end_time', 'is_regular', 'is_cancelled', 'created_at')
    list_filter = ('weekday', 'is_regular', 'is_cancelled', 'created_at')
    search_fields = ('subject__name',)
    actions = [cleanup_old_data]

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('class_schedule', 'student', 'is_present', 'marked_by', 'marked_at')
    list_filter = ('is_present', 'marked_at')
    search_fields = ('student__username', 'class_schedule__subject__name')

admin.site.register(User, CustomUserAdmin)
