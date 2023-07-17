from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


class Pet(models.Model):
    """Домашние животные"""

    Dog = 'DOG'
    Cat = 'CAT'
    Parrot = 'PAR'
    Snake = 'SNA'
    Fish = 'FIS'

    PET_CHOICES = [
        (Dog, 'Dog'),
        (Cat, 'Cat'),
        (Parrot, 'Parrot'),
        (Snake, 'Snake'),
        (Fish, 'Fish'),
    ]

    name = models.CharField(max_length=20)
    age = models.IntegerField(validators=[MinValueValidator(1)])
    animal_type = models.CharField(max_length=20, choices=PET_CHOICES)

    def __str__(self):
        return f'{self.animal_type} {self.name}'


class Director(models.Model):
    """Режиссёр"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    director_email = models.EmailField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='pet_owner', null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_url(self):
        return reverse('directors-detail', args=[self.id])


class DressingRoom(models.Model):
    """Гримёрка"""

    floor = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return f'{self.floor} {self.number}'


class FamilyMember(models.Model):
    """Член семьи"""

    Father = 'FAT'
    Mother = 'MOT'
    Brother = 'BRO'
    Sister = 'SIS'
    Daughter = 'DAU'
    Son = 'SON'

    FAMILY_CHOICES = [
        (Father, 'Father'),
        (Mother, 'Mother'),
        (Brother, 'Brother'),
        (Sister, 'Sister'),
        (Daughter, 'Daughter'),
        (Son, 'Son'),
    ]

    first_name = models.CharField(max_length=30, default='Unknown')
    last_name = models.CharField(max_length=30, default='Unknown')
    age = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(150)])
    family_choice = models.CharField(max_length=3, choices=FAMILY_CHOICES, null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Actor(models.Model):
    """Актер"""

    MALE = 'M'
    FEMALE = 'F'

    GENDERS = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE)
    dressing = models.OneToOneField(DressingRoom, on_delete=models.SET_NULL, null=True, blank=True)
    family_member = models.OneToOneField(FamilyMember, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='family')

    def __str__(self):
        if self.gender == self.MALE:
            return f'Актёр {self.first_name} {self.last_name}'
        else:
            return f'Актриса {self.first_name} {self.last_name}'

    def get_url(self):
        """Ссылка на страницу актёра"""
        return reverse('actor-detail', args=[self.id])


class Movie(models.Model):
    """Фильм"""

    EUR = 'EUR'
    USD = 'USD'
    RUB = 'RUB'

    CURRENCY_CHOICES = [
        (EUR, 'Euro'),
        (USD, 'Dollar'),
        (RUB, 'Rubles'),
    ]

    name = models.CharField(max_length=40)
    rating = models.IntegerField('Рейтинг', validators=[MinValueValidator(1),
                                             MaxValueValidator(100)])
    year = models.IntegerField('Год выпуска', null=True, blank=True)
    budget = models.IntegerField('Бюджет', default=1_000_000, blank=True,
                                 validators=[MinValueValidator(1)])
    currency = models.CharField('Валюта', max_length=3, choices=CURRENCY_CHOICES, default=RUB)
    slug = models.SlugField(default='', null=False)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True, related_name='movies')
    actors = models.ManyToManyField(Actor)

    def get_url(self):
        """Ссылка на страницу фильма"""
        return reverse('movie-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name} - {self.rating}%'

