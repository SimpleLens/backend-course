import shutil

from fastapi import APIRouter, UploadFile

from api.dependencies import DbDep
from services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
async def upload_image( file: UploadFile):
    await ImagesService().upload_image(file=file)