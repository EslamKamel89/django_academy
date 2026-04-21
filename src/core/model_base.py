from typing import Any, Optional, cast

from cloudinary import CloudinaryResource
from django.conf import settings
from django.template.loader import get_template
from django.utils.html import format_html


class CloudinaryMixin:
    cloudinary_image_field_name = "image"
    cloudinary_video_field_name = "video"

    def _get_image_field(self):
        return getattr(self, self.cloudinary_image_field_name, None)

    def _get_video_field(self):
        return getattr(self, self.cloudinary_video_field_name, None)

    @property
    def image_html(self) -> str:
        field = self._get_image_field()
        if not field:
            return "<p>There is no image uploaded</p>"
        return cast(CloudinaryResource, field).image(width=500)

    def get_image(self, *, as_html: bool = False, width: int = 200) -> Optional[str]:
        field = self._get_image_field()
        if not field:
            return None
        image = cast(CloudinaryResource, field)
        if as_html:
            return image.image(width=width, crop="scale")
        return image.build_url(width=width)

    def _video_tag(self, video_url: str, *, controls: bool = True):
        return format_html(
            '<video {}> <source src="{}" type="video/mp4"  /> </video>',
            "controls" if controls else "",
            video_url,
        )

    def get_video(
        self,
        *,
        as_html: bool = False,
        width: int = 200,
        sign_url: bool = True,
        fetch_format: str = "auto",
        quality: str = "auto",
        expiration: int = 3600,
        controls: bool = True,
    ) -> Optional[str]:
        field = self._get_video_field()
        if not field:
            return None
        video = cast(CloudinaryResource, field)
        url = video.build_url(
            width=width,
            sign_url=sign_url,
            fetch_format=fetch_format,
            quality=quality,
            expiration=expiration,
        )

        if as_html:
            template = get_template("videos/embed.html")
            html = template.render(
                {
                    "controls": "controls" if controls else "",
                    "video_url": url,
                    "cloud_name": settings.CLOUDINARY_CLOUD_NAME,
                }
            )
            return html
        return url
