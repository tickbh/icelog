
from typing import Any, Self
from sqlmodel import SQLModel

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