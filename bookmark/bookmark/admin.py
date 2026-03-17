from django.contrib import admin

from bookmark.bookmark import models

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    list_display_links = ['name', 'url']
    list_filter = ['name', 'url']

admin.site.register(models.Bookmark, BookmarkAdmin)