from django.db import models
from users.models import CustomUser
from courses.models import Course

class Certificate(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_number = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='certificates/')
    
    def __str__(self):
        return f"Certificat de {self.student} pour {self.course}"
    
    class Meta:
        unique_together = ['student', 'course']
