from django.contrib import admin, messages
from .models import Movie, Director, Actor, DressingRoom, FamilyMember, Pet
from django.db.models import QuerySet

# admin.site.register(Movie, MovieAdmin)
admin.site.register(Director)
admin.site.register(Actor)


# admin.site.register(DressingRoom)


@admin.register(DressingRoom)
class DressingRoomAdmin(admin.ModelAdmin):
    list_display = ['floor', 'number', 'actor']


class RatingFilter(admin.SimpleListFilter):
    title = 'Фильтр по рейтингу'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<40', 'Низкий'),
            ('от 40 до 59', 'Средний'),
            ('от 60 до 79', 'Высокий'),
            ('>=80', 'Высочайший'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        elif self.value() == 'от 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        elif self.value() == 'от 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        elif self.value() == '>=80':
            return queryset.filter(rating__gte=80)
        return queryset


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # fields = ['name', 'rating']
    # exclude = ['slug']
    # readonly_fields = ['year']
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name', 'rating', 'year', 'budget', 'currency', 'rating_status', 'director']
    list_editable = ['rating', 'year', 'budget', 'currency', 'director']
    ordering = ['rating', '-name']
    list_per_page = 10
    actions = ['set_dollars', 'set_euro']
    search_fields = ['name__startswith', 'rating']
    list_filter = ['name', 'currency', RatingFilter]
    filter_horizontal = ['actors']

    @admin.display(ordering='rating', description='Статус!')
    def rating_status(self, mov: Movie):
        if mov.rating < 50:
            return 'Зачем это смотреть?!'
        if mov.rating < 70:
            return 'Разок можно глянуть'
        if mov.rating <= 85:
            return 'Зачёт'
        return 'Топчик'

    @admin.action(description='Установить валюту в доллар')
    def set_dollars(self, request, qs: QuerySet):
        qs.update(currency=Movie.USD)

    @admin.action(description='Установить валюту в евро')
    def set_euro(self, request, qs: QuerySet):
        count_updates = qs.update(currency=Movie.EUR)
        self.message_user(
            request,
            f'Было обновлено {count_updates} записей',
            messages.ERROR
        )


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['family', 'family_choice', 'first_name', 'last_name', 'age', ]
    list_editable = ['family_choice', 'first_name', 'last_name', 'age', ]


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['animal_type', 'name', 'age']
    list_editable = ['name', 'age']
