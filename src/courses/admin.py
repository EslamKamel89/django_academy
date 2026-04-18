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
        ("video_url",),
        ("order", "status"),
        ("can_preview",),
        ("created_at", "updated_at"),
    )
    readonly_fields = [
        "display_thumbnail",
        "video_url",
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
        return obj.get_video(as_html=True, sign_url=True) or "No Video"

    @admin.display(description="Video url")
    def video_url(self, obj: Lesson):
        url = obj.get_video(sign_url=True)
        if not url:
            return "No video"
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            url,
            obj.title,
        )


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

    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/cloudinary-video-player@3.10.0/dist/cld-video-player.min.css",
            )
        }

        js = (
            "https://cdn.jsdelivr.net/npm/cloudinary-video-player@3.10.0/dist/cld-video-player.min.js",
        )
