import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField('Создание записи', auto_now_add=True)
    modified = models.DateTimeField('Редактирование записи', auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


# id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
# name TEXT NOT NULL UNIQUE,
# description TEXT,
# created timestamp with time zone,
# modified timestamp with time zone
class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name

# id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
# full_name TEXT NOT NULL,
# created timestamp with time zone,
# modified timestamp with time zone
class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


# id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
# title TEXT NOT NULL,
# description TEXT,
# creation_date DATE,
# rating FLOAT,
# type TEXT not null,
# created timestamp with time zone,
# modified timestamp with time zone
class FilmWork(UUIDMixin, TimeStampedMixin):

    class Type(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=50, choices=Type.choices)
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file_path'), blank=True, null=True, upload_to='movies/')
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, verbose_name=_('film work'))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=_('genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, verbose_name=_('film work'))
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name=_('person'))
    role = models.TextField('role')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person')
        verbose_name_plural = _('persons')