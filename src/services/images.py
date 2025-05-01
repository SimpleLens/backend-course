

import shutil
from fastapi import UploadFile
from services.base import BaseService


class ImagesService(BaseService):
    async def upload_image(file: UploadFile):
        with open(f"src\static\images\{file.filename}", "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)