from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from plugins.capm import (get_df, VM)

class capmSchema(BaseModel):
    tags : List[str]
    start : str
    rate : float

router = APIRouter(prefix="/capm",tags=["capm"])

description = '''financial asset tickets: list & start format : YYYY-MM-DD'''
@router.get('/',description=description)
async def capm(data : capmSchema):
    return VM(data.rate,get_df(data.tags,data.start)['dfr'])
