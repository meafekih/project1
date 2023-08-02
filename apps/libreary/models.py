from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    website = models.URLField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    language_choices = (('en', 'English'),('fr', 'French'),('de', 'German'),('es', 'Spanish'),)

    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=2, choices=language_choices, default='en')
    due_date = models.DateField()

    def __str__(self):
        return f"{self.book.title} - {self.language}"
    

