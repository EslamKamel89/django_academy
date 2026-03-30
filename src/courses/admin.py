from typing import cast

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from .models import Course, Lesson, PublishStatus


class LessonInLine(StackedInline):
    model = Lesson
    extra = 0
    readonly_fields = ["created_at", "updated_at", "public_id"]


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    inlines = [LessonInLine]
    list_display = ("id", "title", "status", "access")
    fields = (
        ("title",),
        ("public_id",),
        ("description",),
        ("image",),
        ("display_image",),
        ("status", "access"),
    )
    readonly_fields = ("display_image", "public_id")
    list_filter = ("status", "access")
    search_fields = ("title",)

    @admin.display(description="Preview")
    def display_image(self, obj: Course):
        return format_html(obj.image_html, "")

    @admin.display(boolean=True)
    def is_published(self, obj):
        return obj.status == PublishStatus.PUBLISHED
