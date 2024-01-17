from django.core.exceptions import ValidationError
from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    date = models.DateField(verbose_name='Дата выхода продукта на рынок')

    def __str__(self):
        return f'{self.name} (модель - {self.model})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Link(models.Model):
    class LinkStatus(models.TextChoices):
        FACTORY = 'factory', 'Завод'
        RETAIL_NETWORK = 'retail network', 'Розничная сеть'
        ENTREPRENEUR = 'entrepreneur', 'Индивидуальный предприниматель'

    status_link = models.CharField(max_length=30, choices=LinkStatus.choices, verbose_name='звено сети')
    supplier = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Поставщик', **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    level = models.PositiveSmallIntegerField(verbose_name='Уровень звена')

    products = models.ManyToManyField(Product, verbose_name='Продукты', **NULLABLE)

    debt = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Задолженность перед поставщиком',
                               **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f"{self.get_status_link_display()} - {self.name} (уровень - {self.level})"

    def save(self, *args, **kwargs):
        self.level = self.calculate_depth()
        super().save(*args, **kwargs)

    def calculate_depth(self):
        depth = 0
        parent = self.supplier
        while parent:
            depth += 1
            parent = parent.supplier
        return depth

    def clean(self):
        if self.status_link == 'factory' and (self.supplier is not None or self.debt is not None):
            raise ValidationError('У завода не может быть Поставщика / Задолженности перед поставщиком')
        if self.supplier is None and self.status_link != 'factory':
            raise ValidationError('Без поставщика может быть только Завод')
        depth = self.calculate_depth()
        if depth > 2:
            raise ValidationError('Иерархическая структура не может состоять более чем из 3 уровней')
        super().clean()

    class Meta:
        verbose_name = 'Торговое звено'
        verbose_name_plural = 'Торговые звенья'


class Contact(models.Model):
    email = models.EmailField(max_length=100, verbose_name='email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    num_house = models.CharField(max_length=10, verbose_name='Номер дома')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, verbose_name='Торговое звено')

    def __str__(self):
        return f'{self.city} ({self.email})'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
