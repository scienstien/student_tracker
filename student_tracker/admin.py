from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subject, ClassSchedule, Attendance

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')
    list_filter = ('user_type',) + UserAdmin.list_filter
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type',)}),
    )

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'professor')
    search_fields = ('name', 'professor__username')

class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'weekday', 'start_time', 'end_time', 'is_regular', 'date', 'is_cancelled')
    list_filter = ('is_regular', 'is_cancelled', 'weekday', 'subject')
    search_fields = ('subject__name',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_schedule', 'is_present', 'marked_by', 'marked_at')
    list_filter = ('is_present', 'marked_at', 'class_schedule__subject')
    search_fields = ('student__username', 'class_schedule__subject__name')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(ClassSchedule, ClassScheduleAdmin)
admin.site.register(Attendance, AttendanceAdmin)
