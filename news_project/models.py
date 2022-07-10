import math

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


class News(BaseModel):
    title: str
    text: str
    created_at: datetime
    author: str
    keywords: Optional[List[str]] = None

    @property
    def all_texts(self):
        return f"{self.title}\n{self.text}"

    @validator('keywords', pre=True)
    def keywords_nan(cls, v):
        if isinstance(v, str):
            return eval(v)
        return None if math.isnan(v) else v
