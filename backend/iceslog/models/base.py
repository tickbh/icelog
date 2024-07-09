
from typing import Any
from sqlmodel import SQLModel

class RetMsg(SQLModel):
    code_: str="00000"
    msg_: str="ok"
    
    @staticmethod
    def err_msg(code: str, msg: str):
        return RetMsg(code_=code, msg_=msg)
    