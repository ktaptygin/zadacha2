from django.db import models

# Create your models here.

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    people = models.PositiveSmallIntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'booking'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'contact'

class DeliciousCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'delicious_categories'

class Delicious(models.Model):
    category = models.ForeignKey(
        DeliciousCategory,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    on_main = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'delicious'

class Event(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'events'

class Speciality(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'specialities'

class StaticSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'static'