from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, Lesson, Enrollment

def home(request):
    featured_courses = Course.objects.filter(is_published=True)[:3]
    return render(request, 'courses/home.html', {
        'featured_courses': featured_courses
    })

def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, 'courses/list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'courses/detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f'Vous êtes maintenant inscrit au cours {course.title}')
    return redirect('courses:detail', course_id=course_id)

@login_required
def module_detail(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    return render(request, 'courses/module_detail.html', {
        'course': course,
        'module': module,
        'enrollment': enrollment
    })

@login_required
def lesson_detail(request, course_id, module_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    # Mettre à jour la progression
    if not lesson.completed:
        enrollment.progress += 1
        enrollment.save()
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'module': module,
        'lesson': lesson,
        'enrollment': enrollment
    })
