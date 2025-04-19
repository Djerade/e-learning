from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from courses.models import Enrollment, Course
from certificates.models import Certificate
from django.urls import reverse
from django.db.models import Count

# Create your views here.

@login_required
def profile(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    certificates = Certificate.objects.filter(student=request.user)
    return render(request, 'users/profile.html', {
        'enrollments': enrollments,
        'certificates': certificates
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès')
            return redirect('users:profile')  # Utilisation correcte du namespace
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    certificates = Certificate.objects.filter(student=request.user)
    return render(request, 'users/dashboard.html', {
        'enrollments': enrollments,
        'certificates': certificates
    })

@login_required
def dashboard_redirect(request):
    if request.user.is_instructor:
        return redirect('users:instructor_dashboard')
    return redirect('users:student_dashboard')

@login_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    certificates = Certificate.objects.filter(student=request.user).select_related('course')
    
    return render(request, 'users/student_dashboard.html', {
        'enrollments': enrollments,
        'certificates': certificates,
    })

@login_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user).annotate(enrollment_count=Count('enrollments'))
    total_students = Enrollment.objects.filter(course__in=courses).values('student').distinct().count()
    popular_courses = courses.order_by('-enrollment_count')[:5]
    
    return render(request, 'users/instructor_dashboard.html', {
        'courses': courses,
        'total_students': total_students,
        'popular_courses': popular_courses,
    })
