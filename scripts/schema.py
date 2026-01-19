from pydantic import BaseModel, Field
from typing import List

class ExampleSentence(BaseModel):
    no: int = Field(description="example number")
    kanji: str = Field(description="the character from which the sentences are generated")
    sentence: str = Field(description="the example sentence in japanese")
    translation: str = Field(description="example sentence translated to english")

class SentenceList(BaseModel):
    data: List[ExampleSentence] = Field(description="A list of example sentences")