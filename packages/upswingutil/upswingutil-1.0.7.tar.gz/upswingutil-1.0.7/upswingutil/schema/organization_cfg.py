from typing import Optional
from pydantic import BaseModel

class MultiText(BaseModel):
    defaultText: str = ''
    translatedTexts: Optional[list] = []

# class Languages(BaseModel):
#     description: MultiText = MultiText()
#     translationLanguageCode: str
#     reportDateLanguage: str = ''
#     languageCode = str