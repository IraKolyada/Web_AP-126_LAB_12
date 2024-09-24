from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Spanner, Category

# Register your models here.

class CreatorFilter(admin.SimpleListFilter):
    title = 'Информация про создателя'
    parameter_name = 'status'
    def lookups(self, request, model_admin):
        return [
            ('do', 'Известен создатель'),
            ('dont', 'Не известен создатель'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'do':
            return queryset.filter(creator__isnull=False)
        elif self.value() == 'dont':
            return queryset.filter(creator__isnull=True)

@admin.register(Spanner)
class SpannerAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo','post_photo', 'cat', 'creator', 'tags']
    filter_horizontal = ['tags']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [CreatorFilter, 'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description="Изображение")
    def post_photo(self, spanner: Spanner):
        if spanner.photo:
            return mark_safe(f"<img src='{spanner.photo.url}'width = 50 > ")
        return "Без фото"
    @admin.display(description="Краткое описание", ordering='content')
    def brief_info(self, spanner: Spanner):
        return f"Описание {len(spanner.content)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Spanner.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Spanner.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

#admin.site.register(Spanner,SpannerAdmin)