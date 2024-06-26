from model.schemas import PasteSchema
from storage.db.models import Paste


async def create_paste(paste: PasteSchema, session) -> PasteSchema:
    return paste
