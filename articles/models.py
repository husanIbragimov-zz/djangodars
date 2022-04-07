from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User


class ArticleManager(models.Manager):

    def search(self, query):
        lookup = Q(title__icontains=query) | Q(title__icontains=query)
        obj = Article.objects.filter(lookup)
        return obj


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.tag}'


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='articles', null=True)
    slug = models.SlugField(unique=True, null=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    time = models.DateTimeField(null=True)
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ArticleManager()

    def __str__(self):
        return f'{self.title} - {self.id}'

    # def get_absolute_url(self):
    #         return f'{self.created_at.year}/{self.created_at.month}/{self.created_at.day}/{self.slug}/'

    def get_absolute_url(self):
        return reverse('article_detail_view', kwargs={'slug': self.slug})

    # def save(self, *args, **kwargs):
    # before
    # if self.slug is None:
    #     self.slug = slugify(self.title)
    # super().save(*args, **kwargs)
    # after
    # self.slug = slugify(self.title)
    # super().save()


@receiver(pre_save, sender=Article)
def article_pre_save(sender, instance, *args, **kwargs):
    print(args, kwargs)
    if instance.slug is None:
        instance.slug = slugify(instance.title)
        print('pre-save is working')


def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.title)
        instance.save()
        print('pre-save is working')
        print(args, kwargs)


pre_save.connect(article_pre_save, sender=Article)
post_save.connect(article_post_save, sender=Article)




