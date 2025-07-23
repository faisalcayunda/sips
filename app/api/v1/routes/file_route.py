from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from fastapi.responses import StreamingResponse

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.data_types import UUID7Field
from app.core.params import CommonParams
from app.models import UserModel
from app.schemas.base import PaginatedResponse
from app.schemas.file_schema import FileSchema
from app.services import FileService
from app.utils.helpers import iterfile

router = APIRouter()


@router.get(
    "/files",
    response_model=PaginatedResponse[FileSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_files(
    params: CommonParams = Depends(),
    service: FileService = Depends(Factory().get_file_service),
):
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    files, total = await service.find_all(filter, sort, search, group_by, limit, offset)

    return PaginatedResponse(
        items=[FileSchema.model_validate(file) for file in files],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/files/{object_name}", summary="Get file content")
async def get_file_content(object_name: str, service: FileService = Depends(Factory().get_file_service)):
    file_content, object_info = await service.get_file_content(object_name=object_name)

    return StreamingResponse(
        content=iterfile(file_content),
        media_type=object_info["_content_type"],
        headers={"Content-Disposition": f'attachment; filename="{object_info["_metadata"]["x-amz-meta-filename"]}"'},
    )


@router.get("/files/{id}/metadata", response_model=FileSchema)
async def get_file_info(id: str, service: FileService = Depends(Factory().get_file_service)):
    return await service.find_by_id(id)


@router.post("/files", response_model=FileSchema, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: UserModel = Depends(get_current_active_user),
    service: FileService = Depends(Factory().get_file_service),
):
    result = await service.upload_file(file=file, description=description, user_id=current_user.id)
    return result


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Hapus file")
async def delete_file(
    file_id: UUID7Field,
    current_user: UserModel = Depends(get_current_active_user),
    service: FileService = Depends(Factory().get_file_service),
):
    await service.delete_file_with_content(file_id, str(current_user.id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
