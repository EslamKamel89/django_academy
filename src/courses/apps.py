from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = "courses"

    def ready(self) -> None:
        from helpers import cloudinary_init

        cloudinary_init()
        return super().ready()
