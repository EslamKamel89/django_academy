import cloudinary

# import cloudinary.api
# import cloudinary.uploader
# from cloudinary import CloudinaryImage, CloudinaryVideo
from decouple import config
from django.conf import settings


def cloudinary_init():
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_PUBLIC_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )
