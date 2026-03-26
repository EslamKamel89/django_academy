import uuid
from typing import Optional, cast

from cloudinary import CloudinaryResource
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.manager import Manager
from django.utils.text import slugify


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


# Create your models here.
class Course(models.Model):
    # adding id is for static typing only and auto complete
    id: int
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = CloudinaryField(
        "image",
        blank=True,
        null=True,
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

    @property
    def is_published(self) -> bool:
        return self.status == PublishStatus.PUBLISHED

    @property
    def image_html(self) -> str:
        if not self.image:
            return "<p>There is no image uploaded</p>"
        return cast(CloudinaryResource, self.image).image(width=500)

    def get_image(self, *, as_html: bool = False, width: int = 200) -> Optional[str]:
        if not self.image:
            return None
        image = cast(CloudinaryResource, self.image)
        if as_html:
            return image.image(width=width, crop="scale")
        return image.build_url(width=width)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-created_at"]


class Lesson(models.Model):
    # adding id is for static typing only and auto complete
    id: int
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField(
        "image",
        blank=True,
        null=True,
    )
    video = CloudinaryField(
        "video",
        blank=True,
        null=True,
        resource_type="video",
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

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["order", "-created_at"]
