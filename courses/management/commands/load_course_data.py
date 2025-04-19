from django.core.management.base import BaseCommand
from django.core.files import File
from courses.models import Course
from PIL import Image, ImageDraw, ImageFont
import os
import random
from io import BytesIO

class Command(BaseCommand):
    help = 'Load course data and generate thumbnails'

    def handle(self, *args, **options):
        # Couleurs pour les vignettes
        colors = [
            '#3498db',  # Bleu
            '#2ecc71',  # Vert
            '#e74c3c',  # Rouge
            '#f1c40f',  # Jaune
            '#9b59b6',  # Violet
        ]

        # Créer le dossier pour les vignettes s'il n'existe pas
        os.makedirs('media/course_thumbnails', exist_ok=True)

        # Générer des vignettes pour chaque cours
        for course in Course.objects.all():
            # Créer une nouvelle image
            img = Image.new('RGB', (800, 400), color=random.choice(colors))
            draw = ImageDraw.Draw(img)

            # Ajouter le titre du cours
            try:
                font = ImageFont.truetype("Arial", 40)
            except:
                font = ImageFont.load_default()
            
            # Centrer le texte
            text = course.title
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            x = (800 - text_width) / 2
            y = (400 - text_height) / 2

            draw.text((x, y), text, fill='white', font=font)

            # Sauvegarder l'image
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)

            # Sauvegarder l'image dans le modèle
            course.thumbnail.save(
                f'course_{course.id}.jpg',
                File(img_io),
                save=True
            )

            self.stdout.write(self.style.SUCCESS(f'Created thumbnail for course: {course.title}')) 