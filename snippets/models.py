from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from enum import Enum

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', default=1, related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField(default='')

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML representation of the code snippet.
        :param args:
        :param kwargs:
        :return:
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)


class Publication(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ('headline',)

    def __str__(self):
        return self.headline

    def reset(self):
        self.headline = 'Default headline'
        self.publications.clear()
        self.save()


class Person(models.Model):
    name = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=30, unique=True)
    favorites = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return f'{self.id}: {self.username}'


class Student(Person):
    enroll_number = models.CharField(max_length=10, blank=True)
    friends = models.ManyToManyField('self')

    def __str__(self):
        return f'{self.id}: {self.username}'


class Employee(models.Model):
    TYPE_CHOICES = (
        (1, 'OWNER'),
        (2, 'STAFF')
    )

    name = models.CharField(max_length=30, blank=True)
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=2)
    staffs = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return f'{self.id}: {self.name}: {self.type}'

    def clean(self):
        """How to validate if adding staff is of type `STAFF`?"""
        pass
