
from typing import Any
from sqlmodel import SQLModel

class RetMsg(SQLModel):
    code: str="00000"
    msg: str="ok"
    data: Any
    
    @staticmethod
    def err_msg(code: str, msg: str):
        return RetMsg(code=code, msg=msg, data=None)
    
class CommonMessage(SQLModel):
    def build_message(self, code="00000", msg="ok") -> RetMsg:
        return RetMsg(data=self, code=code, msg=msg)