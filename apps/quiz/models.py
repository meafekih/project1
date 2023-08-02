from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=40, default='New Quiz')
    category = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title +'   :   '+ self.category.name


class Question(models.Model):
    SCAL = ((0,'Fundamental'),(1,'Begginner'),(2,'Intermedate'),(3,'Advanced'),(4,'Expert'),)
    TYPE = ((0,'Multi choices'),)
    quiz = models.ForeignKey(Quiz, related_name='question', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=40, verbose_name='Title')
    technique = models.IntegerField(choices=TYPE, default=0, verbose_name='Type of questions')
    difficulty = models.IntegerField(choices=SCAL, default=0, verbose_name='Difficulty')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created')
    is_active = models.BooleanField(default=False, verbose_name='Active status')

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answer', on_delete=models.DO_NOTHING)
    answer_text = models.CharField(max_length=50, verbose_name='Answer Text')
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


