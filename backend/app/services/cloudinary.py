import asyncio
import io

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from app.config import settings


if settings.cloudinary_configured:
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )


async def upload_product_image(file: UploadFile, folder: str = "vikings_products") -> str:
    if not settings.cloudinary_configured:
        raise RuntimeError("Cloudinary credentials are not configured.")

    contents = await file.read()
    if not contents:
        raise RuntimeError("Uploaded file is empty.")

    def _upload() -> dict[str, str]:
        return cloudinary.uploader.upload(
            io.BytesIO(contents),
            resource_type="image",
            folder=folder,
            use_filename=True,
            unique_filename=True,
            overwrite=False,
        )

    result = await asyncio.to_thread(_upload)
    secure_url = result.get("secure_url")
    if not secure_url:
        raise RuntimeError("Cloudinary upload did not return a secure URL.")

    return secure_url
