import shutil

from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
async def upload_image(file: UploadFile):
    with open(f"src\static\images\{file.filename}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
