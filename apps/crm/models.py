from django.db import models
from apps.authentication.models import ExtendUser as User
from apps.base.models import base

class Customer(base):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    def __str__(self):
        return self.name

class Contact(base):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    def __str__(self):
        return self.name

class Opportunity(base):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='opportunities')  
    def __str__(self):
        return self.name

class Task(base):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    def __str__(self):
        return self.title

class Product(base):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class Sale(base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    products = models.ManyToManyField(Product, related_name='sales')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    def __str__(self):
        return f"Sale for {self.customer} on {self.sale_date}"

class Meeting(base):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='meetings')
    participants = models.ManyToManyField(User, related_name='meetings_attended')
    def __str__(self):
        return self.title

class Lead(base):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    description = models.TextField()
    def __str__(self):
        return self.name

""" 
class Campaign(base):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    leads = models.ManyToManyField(Lead, related_name='campaigns')
    def __str__(self):
        return self.name
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

    """ 
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