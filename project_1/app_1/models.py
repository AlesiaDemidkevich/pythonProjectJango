from django.db import models


class Mebel(models.Model):
    link = models.TextField('links')
    price = models.DecimalField('price', max_digits=12, decimal_places=2)
    description = models.TextField('description')

    def __str__(self):
        return f'{self.price} | {self.description}'