from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'thumbnail', 'price', 'duration', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }