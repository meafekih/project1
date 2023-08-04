# For pruposes of this article I have ommitted a number of stuff in this snippet
# to only the most relevant

import os
from slugify import slugify
from django.db import models

class Company(models.Model):
  name = models.CharField(max_length=100)
  logo = models.ImageField(blank=True)