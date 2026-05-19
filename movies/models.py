from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='movies/', blank=True, null=True)
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0)
        ]
    )
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    username = models.CharField(max_length=150, editable=False)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.username:
            latest_review = Review.objects.filter(movie=self.movie).order_by('-id').first()
            if latest_review and latest_review.username.startswith('testUser'):
                try:
                    next_id = int(latest_review.username.replace('testUser', '')) + 1
                    self.username = f'testUser{next_id}'
                except ValueError:
                    self.username = 'testUser0'
            else:
                self.username = 'testUser0'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} - {self.movie.title}'