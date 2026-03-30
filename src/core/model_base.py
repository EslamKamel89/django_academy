from typing import Any, Optional, cast

from cloudinary import CloudinaryResource


class CloudinaryMixin:
    cloudinary_field_name = "image"

    def _get_field(self):
        return getattr(self, self.cloudinary_field_name, None)

    @property
    def image_html(self) -> str:
        if not self._get_field():
            return "<p>There is no image uploaded</p>"
        return cast(CloudinaryResource, self._get_field()).image(width=500)

    def get_image(self, *, as_html: bool = False, width: int = 200) -> Optional[str]:
        field = self._get_field()
        if not field:
            return None
        image = cast(CloudinaryResource, field)
        if as_html:
            return image.image(width=width, crop="scale")
        return image.build_url(width=width)
