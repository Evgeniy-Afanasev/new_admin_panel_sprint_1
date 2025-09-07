from django.contrib import admin
from .models import Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ('person',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    list_display = ('full_name',)
    search_fields = ('full_name',)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline, GenreFilmWorkInline)
    list_display = ('title', 'type', 'creation_date', 'rating',)
    list_filter = ('type', 'creation_date', 'rating')
    search_fields = ('title', 'description', 'id')
