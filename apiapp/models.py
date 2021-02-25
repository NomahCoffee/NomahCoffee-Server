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

class StoreHours(models.Model):
    DAYS = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday")
    ]
    
    day = models.CharField(max_length=9, choices=DAYS)
    from_hour = models.TimeField(null=True, blank=True)
    to_hour = models.TimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', 'from_hour')
        # unique_together = ('weekday', 'from_hour', 'to_hour')
        verbose_name = "Day"
        verbose_name_plural = "Store Hours"

    def __str__(self):
        return self.day

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_hour, self.to_hour)

class StoreLocation(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='store_images', blank=True)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Store Locations"