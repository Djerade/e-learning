from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, Lesson, Enrollment

def home(request):
    courses = Course.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'courses/home.html', {'courses': courses})

def course_list(request):
    courses = Course.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'courses/home.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    modules = course.modules.all().order_by('order')
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled
    })

@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    if created:
        messages.success(request, f'Vous êtes maintenant inscrit au cours {course.title}')
    else:
        messages.info(request, f'Vous êtes déjà inscrit à ce cours')
    return redirect('courses:course_detail', course_id=course.id)

@login_required
def complete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    enrollment.completed = True
    enrollment.save()
    messages.success(request, f'Félicitations ! Vous avez terminé le cours {course.title}')
    return redirect('courses:course_detail', course_id=course.id)

def module_detail(request, course_id, module_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    module = get_object_or_404(Module, id=module_id, course=course)
    lessons = module.lessons.all().order_by('order')
    return render(request, 'courses/module_detail.html', {
        'course': course,
        'module': module,
        'lessons': lessons
    })

def lesson_detail(request, course_id, module_id, lesson_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'module': module,
        'lesson': lesson
    })
