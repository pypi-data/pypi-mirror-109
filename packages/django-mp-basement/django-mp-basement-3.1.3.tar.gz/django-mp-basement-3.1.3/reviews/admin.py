
from django.contrib import admin

from suit.sortables import SortableTabularInline

from reviews.models import Review, ReviewImage


class ImagesInline(SortableTabularInline):
    fields = ['preview_tag']
    readonly_fields = ['preview_tag']
    model = ReviewImage
    extra = 0
    max_num = 0


class ReviewAdmin(admin.ModelAdmin):

    inlines = [ImagesInline]

    list_filter = ['is_active']

    list_display = [
        'name', 'email', 'date_created', 'user', 'rating', 'is_active']

    list_editable = ['is_active']

    search_fields = ['id', 'name', 'email', 'text']


admin.site.register(Review, ReviewAdmin)
