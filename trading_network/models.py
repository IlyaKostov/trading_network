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
        RETAIL_NETWORK = 'retail_network', 'Розничная сеть'
        ENTREPRENEUR = 'entrepreneur', 'Индивидуальный предприниматель'

    status_link = models.CharField(max_length=30, choices=LinkStatus.choices, verbose_name='звено сети')
    supplier = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Поставщик', **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    level = models.PositiveSmallIntegerField(verbose_name='Уровень звена')

    products = models.ManyToManyField(Product, verbose_name='Продукты')

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
