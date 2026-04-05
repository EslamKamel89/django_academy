from typing import Any, Optional, cast

from cloudinary import CloudinaryResource


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

    def get_video(self, *, as_html: bool = False, width: int = 200) -> Optional[str]:
        field = self._get_video_field()
        if not field:
            return None
        video = cast(CloudinaryResource, field)
        if as_html:
            return video.video(width=width, controls=True)
        return video.build_url(width=width)
