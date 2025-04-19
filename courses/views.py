from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, Lesson, Enrollment
from .forms import CourseForm

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

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Le cours a été créé avec succès.')
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'courses/course_create.html', {'form': form})

@login_required
def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le cours a été mis à jour avec succès.')
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_update.html', {'form': form})

@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Le cours a été supprimé avec succès.')
        return redirect('courses:course_list')
    return render(request, 'courses/course_delete.html', {'course': course})
