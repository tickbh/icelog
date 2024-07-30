
from typing import Any, Self
from sqlmodel import SQLModel
from typing import Annotated
from fastapi import Body

class RetMsg(SQLModel):
    code: str="00000"
    msg: str="ok"
    
    @staticmethod
    def err_msg(code: str, msg: str):
        return RetMsg(code=code, msg=msg)
    
    
class OptionType(SQLModel):
    value: str | int
    label: str = ""
    
    children: list[Self] = []
    
class PageModel(SQLModel):
    pageNum: Annotated[int, Body(title="Check Default Page Num", ge=1)] = 1
    pageSize: Annotated[int, Body(title="Check Default Page Size", ge=10, le=100)] = 10