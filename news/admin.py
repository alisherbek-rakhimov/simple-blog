from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import News, Category


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ['id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    list_filter = ['is_published', 'category']

    fields = ['title', 'category', 'content', 'get_photo', 'photo', 'is_published', 'views', 'created_at', 'updated_at']

    readonly_fields = ['get_photo', 'views', 'created_at', 'updated_at']
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        # else:
        #     return 'photo ne ustanovleno'

    get_photo.short_description = 'Miniatura'

    empty_value_display = "-пусто-"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title']

    empty_value_display = "-пусто-"


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Upravlenie novostyami'
admin.site.site_header = 'Upravlenie novostyami'
