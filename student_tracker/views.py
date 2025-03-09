from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import User, Subject, ClassSchedule, Attendance
from django.http import JsonResponse
from datetime import datetime, timedelta

def is_professor(user):
    return user.user_type == 'professor'

def is_class_rep(user):
    return user.user_type == 'class_rep'

@login_required
def dashboard(request):
    context = {
        'user_type': request.user.user_type
    }
    
    if request.user.user_type == 'professor':
        subject = request.user.teaching_subject
        today_classes = ClassSchedule.objects.filter(
            subject=subject,
            is_cancelled=False
        ).filter(
            Q(is_regular=True, weekday=timezone.now().weekday()) |
            Q(is_regular=False, date=timezone.now().date())
        )
        context.update({
            'subject': subject,
            'today_classes': today_classes
        })
    
    elif request.user.user_type == 'student':
        today_attendance = Attendance.objects.filter(
            student=request.user,
            class_schedule__is_cancelled=False
        ).filter(
            Q(class_schedule__is_regular=True, class_schedule__weekday=timezone.now().weekday()) |
            Q(class_schedule__is_regular=False, class_schedule__date=timezone.now().date())
        )
        context['today_attendance'] = today_attendance
    
    elif request.user.user_type == 'class_rep':
        all_subjects = Subject.objects.all()
        context['subjects'] = all_subjects
    
    return render(request, 'dashboard.html', context)

@login_required
@user_passes_test(is_professor)
def mark_attendance(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    # Check if professor can mark attendance
    if not schedule.can_mark_attendance():
        messages.error(request, "Attendance can only be marked during class time or up to 30 minutes after class ends.")
        return redirect('dashboard')
    
    # Check if professor owns this subject
    if schedule.subject.professor != request.user:
        messages.error(request, "You can only mark attendance for your own subject.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            # Get selected student IDs from the form
            student_ids = request.POST.getlist('students')
            
            # Get all students
            all_students = User.objects.filter(user_type='student')
            
            # Mark attendance for all students
            for student in all_students:
                Attendance.objects.update_or_create(
                    class_schedule=schedule,
                    student=student,
                    defaults={
                        'is_present': str(student.id) in student_ids,
                        'marked_by': request.user
                    }
                )
            
            messages.success(request, "Attendance marked successfully!")
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f"Error marking attendance: {str(e)}")
            return redirect('dashboard')
    
    # For GET request, prepare the attendance form
    students = User.objects.filter(user_type='student').order_by('username')
    existing_attendance = Attendance.objects.filter(
        class_schedule=schedule,
        is_present=True
    )
    existing_attendance_ids = list(existing_attendance.values_list('student_id', flat=True))
    
    context = {
        'schedule': schedule,
        'students': students,
        'existing_attendance_ids': existing_attendance_ids
    }
    return render(request, 'mark_attendance.html', context)

@login_required
@user_passes_test(is_class_rep)
def manage_schedule(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        weekday = request.POST.get('weekday')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        is_regular = request.POST.get('is_regular') == 'true'
        date = request.POST.get('date')
        
        subject = get_object_or_404(Subject, id=subject_id)
        
        schedule = ClassSchedule.objects.create(
            subject=subject,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
            is_regular=is_regular,
            date=date if not is_regular else None,
            created_by=request.user
        )
        
        messages.success(request, "Class schedule created successfully!")
        return redirect('dashboard')
    
    subjects = Subject.objects.all()
    schedules = ClassSchedule.objects.all().order_by('weekday', 'start_time')
    
    context = {
        'subjects': subjects,
        'schedules': schedules
    }
    return render(request, 'manage_schedule.html', context)

@login_required
@user_passes_test(is_class_rep)
def cancel_class(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    schedule.is_cancelled = True
    schedule.save()
    messages.success(request, "Class cancelled successfully!")
    return redirect('dashboard')

@login_required
def view_attendance(request):
    if request.user.user_type == 'student':
        attendance = Attendance.objects.filter(student=request.user)
    elif request.user.user_type == 'professor':
        attendance = Attendance.objects.filter(class_schedule__subject__professor=request.user)
    else:
        attendance = Attendance.objects.all()
    
    context = {
        'attendance': attendance
    }
    return render(request, 'view_attendance.html', context) 