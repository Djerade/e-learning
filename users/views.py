from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from courses.models import Enrollment
from certificates.models import Certificate

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
            return redirect('users:profile')
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
