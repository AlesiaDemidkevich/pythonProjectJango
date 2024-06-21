from django.db import models


class Mebel(models.Model):
    link = models.TextField('Ссылка на товар')
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    description = models.TextField('Описание товара')
    parse_datetime = models.DateTimeField('Дата объявления', auto_now_add=True)

    def get_absolute_url(self):
        return self.link

    def __str__(self):
        return f'{self.price} | {self.description}'

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'
        ordering = ['parse_datetime', 'price']