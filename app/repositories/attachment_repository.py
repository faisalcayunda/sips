from app.models import AttachmentModel

from .base import BaseRepository


class AttachmentRepository(BaseRepository[AttachmentModel]):
    def __init__(self, model):
        super().__init__(model)
