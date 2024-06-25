import string
import random

from pydantic import BaseModel, Field

from model.base import TimeMixin


MAX_TITLE_LENGTH: int = 50


def default_title() -> str:
    return ''.join(random.choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    ) for _ in range(MAX_TITLE_LENGTH))


class Paste(BaseModel, TimeMixin):
    """
    The main entity of the project.
    """
    title: str = Field(max_length=MAX_TITLE_LENGTH,
                       default_factory=default_title,
                       description="The title of the block.")
    text: str = Field(description="The text of the block.")
    user_id: int = Field(description="The owner id of the paste.")
