from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Naimenovanie kategorii')

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorii'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse(viewname='category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Naimenovanie')
    content = models.TextField(blank=True, verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data publikatsii')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Obnovleno')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Foto', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Opublikovano')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Kategoriya',
                                 related_name='news')
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse(viewname='view_news', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Novost'
        verbose_name_plural = 'Novosti'
        ordering = ['-created_at']
