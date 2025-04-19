from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .models import Certificate

# Create your views here.

@login_required
def certificate_list(request):
    certificates = Certificate.objects.filter(student=request.user)
    return render(request, 'certificates/list.html', {'certificates': certificates})

@login_required
def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id, student=request.user)
    return render(request, 'certificates/detail.html', {'certificate': certificate})

@login_required
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id, student=request.user)
    response = FileResponse(certificate.pdf_file, as_attachment=True)
    return response
