import uuid
from typing import Literal, Optional, cast

from cloudinary import CloudinaryResource
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.manager import Manager
from django.utils.text import slugify

from core.model_base import CloudinaryMixin


class AccessRequirement(models.TextChoices):
    ANYONE = ("anyone", "Anyone")
    EMAIL_REQUIRED = ("email_req", "Email Required")


class PublishStatus(models.TextChoices):
    PUBLISHED = ("pub", "Published")
    COMING_SOON = ("soon", "Coming Soon")
    DRAFT = ("draft", "Draft")


def course_directory_path(instance: "Course", filename):
    slug = slugify(instance.title) or "course"
    unique = uuid.uuid4().hex[:8]
    return f"courses/{slug}_{unique}/{filename}"


def get_courses_public_id_prefix(instance: "Course", *args, **kwargs):
    # print(args, kwargs)
    unique = uuid.uuid4().hex[:8]
    slug = slugify(instance.title)
    return f"courses/{slug}-{unique}"


def get_lessons_public_id_prefix(asset_type: Literal["image", "video"] = "image"):
    def _inner(instance: "Lesson", *args, **kwargs):
        unique = uuid.uuid4().hex[:8]
        slug = slugify(instance.title) or "lesson"
        if asset_type == "image":
            return f"lessons/images/{slug}-{unique}"
        else:
            return f"lessons/videos/{slug}-{unique}"

    return _inner


def _generate_public_id(model_cls, base: str) -> str:
    for _ in range(10):  # safety limit
        unique = uuid.uuid4().hex[:8]
        candidate = f"{base}-{unique}"
        if not model_cls.objects.filter(public_id=candidate).exists():
            return candidate
    raise RuntimeError("Failed to generate unique public_id")


# Create your models here.
class Course(CloudinaryMixin, models.Model):
    # adding id is for static typing only and auto complete
    id: int
    title = models.CharField(max_length=255)
    public_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    description = models.TextField(blank=True, null=True)
    image = CloudinaryField(
        "image",
        blank=True,
        null=True,
        public_id_prefix=get_courses_public_id_prefix,
        asset_folder="courses",
        tags=["course", "thumbnail"],
    )
    # image = models.ImageField(
    #     upload_to=course_directory_path,  # type: ignore
    #     blank=True,
    #     null=True,
    # )

    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
        db_index=True,
    )

    access = models.CharField(
        max_length=20,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lessons: Manager["Lesson"]

    def save(self, *args, **kwargs):
        if not self.public_id:
            base = slugify(self.title) if self.title else "course"
            self.public_id = _generate_public_id(Course, base)
        return super().save(*args, **kwargs)

    @property
    def is_published(self) -> bool:
        return self.status == PublishStatus.PUBLISHED

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-created_at"]


class Lesson(CloudinaryMixin, models.Model):
    cloudinary_image_field_name = "thumbnail"
    cloudinary_video_field_name = "video"
    # adding id is for static typing only and auto complete
    id: int
    title = models.CharField(max_length=255)
    public_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField(
        "image",
        blank=True,
        null=True,
        public_id_prefix=get_lessons_public_id_prefix("image"),
        asset_folder="lessons/images",
        tags=["lesson", "thumbnail"],
    )
    video = CloudinaryField(
        "video",
        blank=True,
        null=True,
        resource_type="video",
        public_id_prefix=get_lessons_public_id_prefix("video"),
        asset_folder="lessons/videos",
        tags=["lesson", "video"],
    )
    order = models.IntegerField(default=0)
    course_id: int
    course: "models.ForeignKey[Course]" = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED,
        db_index=True,
    )
    can_preview = models.BooleanField(
        default=False,
        help_text="If user don't have access to the course they could see this lesson",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.public_id:
            base = slugify(self.title) if self.title else "lesson"
            self.public_id = _generate_public_id(Lesson, base)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["order", "-created_at"]
