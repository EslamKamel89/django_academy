import cloudinary

# import cloudinary.api
# import cloudinary.uploader
# from cloudinary import CloudinaryImage, CloudinaryVideo
from decouple import config

CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_PUBLIC_API_KEY = config("CLOUDINARY_PUBLIC_API_KEY")
CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET")


def cloudinary_init():
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_PUBLIC_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
    )
