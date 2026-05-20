import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from movies.models import Movie, Genre
from datetime import datetime

class Command(BaseCommand):
    help = "Загрузка фильмов из API TMDB"

    def handle(self, *args, **options):
        api_key = os.getenv("TMDB_API_KEY")
        if not api_key:
            self.stdout.write(self.style.ERROR("TMDB_API_KEY не найден в .env"))
            return

        self.stdout.write(self.style.WARNING("Запрашиваем жанры..."))
        genres_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ru-RU"
        try:
            genres_resp = requests.get(genres_url).json()
            tmdb_genres = {g["id"]: g["name"] for g in genres_resp.get("genres", [])}
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка жанров: {e}"))
            return

        for page in range(1, 6):
            self.stdout.write(self.style.WARNING(f"Загрузка страницы {page}..."))
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ru-RU&page={page}"
            
            try:
                response = requests.get(url).json()
                movies_list = response.get("results", [])
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка API: {e}"))
                continue

            for item in movies_list:
                title = item.get("title")
                if not title:
                    continue

                if Movie.objects.filter(title=title).exists():
                    continue

                release_date_str = item.get("release_date")
                if not release_date_str:
                    continue

                try:
                    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue

                genre_objects = []
                for g_id in item.get("genre_ids", []):
                    g_name = tmdb_genres.get(g_id)
                    if g_name:
                        genre, _ = Genre.objects.get_or_create(name=g_name)
                        genre_objects.append(genre)

                movie = Movie(
                    title=title,
                    release_date=release_date,
                    description=item.get("overview", ""),
                    rating=item.get("vote_average", 0.0)
                )

                poster_path = item.get("poster_path")
                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    try:
                        img_resp = requests.get(poster_url, timeout=10)
                        if img_resp.status_code == 200:
                            file_name = f"tmdb_{item['id']}.jpg"
                            movie.image.save(file_name, ContentFile(img_resp.content), save=False)
                    except Exception:
                        pass

                movie.save()
                movie.genres.set(genre_objects)
                self.stdout.write(self.style.SUCCESS(f"Добавлен фильм: {title}"))

        self.stdout.write(self.style.SUCCESS("Готово!"))