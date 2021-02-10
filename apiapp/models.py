from django.db import models

# Create your models here.

class Coffee(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(upload_to='coffee_images', blank=True)
    description = models.CharField(max_length=10000, blank=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Coffee, self).save(*args, **kwargs)