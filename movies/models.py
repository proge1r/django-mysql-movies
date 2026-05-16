from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    release_date = models.DateField(verbose_name="Release Date")
    description = models.TextField(verbose_name="Description", blank=True)
    image = models.ImageField(upload_to='movies/', blank=True, null=True, verbose_name="Poster")
    
    rating = models.IntegerField(
        verbose_name="Rating",
        validators=[
            MinValueValidator(1, message="Rating cannot be less than 1."),
            MaxValueValidator(5, message="Rating cannot be greater than 5.")
        ]
    )

    def __str__(self):
        return self.title