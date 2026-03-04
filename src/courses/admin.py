from django.contrib import admin

from .models import Course, PublishStatus


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "access")
    list_filter = ("status", "access")
    search_fields = ("title",)

    @admin.display(boolean=True)
    def is_published(self, obj):
        return obj.status == PublishStatus.PUBLISHED
