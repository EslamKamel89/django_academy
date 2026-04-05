from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from .models import Course, Lesson, PublishStatus


class LessonInLine(StackedInline):
    model = Lesson
    extra = 0
    fields = (
        ("title",),
        ("description",),
        ("thumbnail",),
        ("display_thumbnail",),
        ("video",),
        ("display_video",),
        ("order", "status"),
        ("can_preview"),
        ("created_at", "updated_at"),
    )
    readonly_fields = [
        "display_thumbnail",
        "display_video",
        "created_at",
        "updated_at",
        "public_id",
    ]

    @admin.display(description="preview image")
    def display_thumbnail(self, obj: Lesson):
        return format_html(obj.image_html, "")

    @admin.display(description="preview video")
    def display_video(self, obj: Lesson):
        return format_html(obj.get_video(as_html=True) or "", "")


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    inlines = [LessonInLine]
    list_display = ("id", "title", "status", "access")
    list_display_links = ("id", "title")
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
