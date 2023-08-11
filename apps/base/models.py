from django.db import models
from apps.authentication.models import ExtendUser as User

class base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class customer_change(models.Model):
    change_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='change', null=True)
    model_changed = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

"""
class all(base):

    AutoField = models.AutoField(primary_key=True)
    TextField = models.TextField()
    IntegerField = models.IntegerField()
    BooleanField = models.BooleanField()
    CharField = models.CharField(max_length=255)
    DateTimeField = models.DateTimeField()
    DateField = models.DateField()
    TimeField = models.TimeField()
    BinaryField = models.BinaryField()
    EmailField = models.EmailField()
    ImageField = models.ImageField()
    FileField = models.FileField()
    SlugField = models.SlugField()

     
    #BigAutoField = models.BigAutoField()
    BigIntegerField = models.BigIntegerField()
    DecimalField = models.DecimalField(decimal_places=2, max_digits=4)
    DurationField = models.DurationField()
    FilePathField = models.FilePathField()
    FloatField = models.FloatField()
    GenericIPAddressField = models.GenericIPAddressField()
    JSONField = models.JSONField()
    PositiveBigIntegerField = models.PositiveBigIntegerField()
    PositiveIntegerField = models.PositiveIntegerField()
    PositiveSmallIntegerField = models.PositiveSmallIntegerField()
    #SmallAutoField = models.SmallAutoField()
    SmallIntegerField = models.SmallIntegerField()
    URLField = models.URLField()
    UUIDField = models.UUIDField() 
"""