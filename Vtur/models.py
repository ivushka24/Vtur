from django.db import models
from django.conf import settings




from django.contrib.auth.models import User

class Tour(models.Model):

    TOUR_TYPES = [('i', "Island"), ('g', "Georgia"), ('s', "Swamp"), ('f', "Float")]

    title = models.CharField(max_length=100, blank=False)
    tour_type = models.CharField(blank=False, max_length=1, choices=TOUR_TYPES)
    description = models.TextField(blank=False)
    program = models.TextField(blank=False)
    cost = models.IntegerField(blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    vacant_spot = models.IntegerField()
    image = models.ImageField(upload_to="uploads")


    def __str__(self):
        return f"{self.title} {self.start_date} - {self.end_date}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    person_numbers = models.IntegerField(default=1)
    contact_phone = models.CharField(blank=False, max_length=13)


    def __str__(self):
        return f" order #{self.id}"

