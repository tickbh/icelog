
from datetime import timedelta
import json
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import ORJSONResponse
from iceslog import cruds
from iceslog.api.deps import CurrentUser, SessionDep
from iceslog.captcha import img_captcha
from iceslog.core import security
from iceslog.core.config import settings
from iceslog.models import MsgAuthCaptcha, RetMsg, MsgLoginRet, Token
from iceslog.models.menu import Menus
from iceslog.utils import PidTable
router = APIRouter()

def deal_func(data: Menus):
    new_data = {
        "id": data.id,
        "path": data.path,
        "component": data.component,
        "redirect": data.redirect,
        "name": data.name,
        "perm": data.perm,
        "meta": {
            "title": data.name,
            "icon": data.icon,
            "hidden": not data.is_show or len(data.perm or "") > 0,
            "alwaysShow": False,
            "params": data.params,
        }
    }
    return new_data
pid_cls = PidTable(Menus, deal_func=deal_func)

# @router.get("/routes", response_class=ORJSONResponse)
# def get_routers():
#     value = """
#     {"code":"00000","data":[{"path":"/system","component":"Layout","redirect":"/system/user","name":"/system","meta":{"title":"系统管理","icon":"system","hidden":false,"alwaysShow":false,"params":null},"children":[{"path":"user","component":"system/user/index","name":"User","meta":{"title":"用户管理","icon":"user","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"role","component":"system/role/index","name":"Role","meta":{"title":"角色管理","icon":"role","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"menu","component":"system/menu/index","name":"Menu","meta":{"title":"菜单管理","icon":"menu","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"dept","component":"system/dept/index","name":"Dept","meta":{"title":"部门管理","icon":"tree","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"dict","component":"system/dict/index","name":"Dict","meta":{"title":"字典管理","icon":"dict","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"log","component":"system/log/index","name":"Log","meta":{"title":"系统日志","icon":"document","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}}]},{"path":"/api","component":"Layout","name":"/api","meta":{"title":"接口文档","icon":"api","hidden":false,"alwaysShow":true,"params":null},"children":[{"path":"apifox","component":"demo/api/apifox","name":"Apifox","meta":{"title":"Apifox","icon":"api","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}}]},{"path":"/doc","component":"Layout","redirect":"https://juejin.cn/post/7228990409909108793","name":"/doc","meta":{"title":"平台文档","icon":"document","hidden":false,"alwaysShow":false,"params":null},"children":[{"path":"internal-doc","component":"demo/internal-doc","name":"InternalDoc","meta":{"title":"平台文档(内嵌)","icon":"document","hidden":false,"alwaysShow":false,"params":null}},{"path":"https://juejin.cn/post/7228990409909108793","name":"Https://juejin.cn/post/7228990409909108793","meta":{"title":"平台文档(外链)","icon":"link","hidden":false,"alwaysShow":false,"params":null}}]},{"path":"/multi-level","component":"Layout","name":"/multiLevel","meta":{"title":"多级菜单","icon":"cascader","hidden":false,"alwaysShow":true,"params":null},"children":[{"path":"multi-level1","component":"demo/multi-level/level1","name":"MultiLevel1","meta":{"title":"菜单一级","icon":"","hidden":false,"alwaysShow":true,"params":null},"children":[{"path":"multi-level2","component":"demo/multi-level/children/level2","name":"MultiLevel2","meta":{"title":"菜单二级","icon":"","hidden":false,"alwaysShow":false,"params":null},"children":[{"path":"multi-level3-1","component":"demo/multi-level/children/children/level3-1","name":"MultiLevel31","meta":{"title":"菜单三级-1","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"multi-level3-2","component":"demo/multi-level/children/children/level3-2","name":"MultiLevel32","meta":{"title":"菜单三级-2","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}}]}]}]},{"path":"/component","component":"Layout","name":"/component","meta":{"title":"组件封装","icon":"menu","hidden":false,"alwaysShow":false,"params":null},"children":[{"path":"curd","component":"demo/curd/index","name":"Curd","meta":{"title":"增删改查","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"table-select","component":"demo/table-select/index","name":"TableSelect","meta":{"title":"列表选择器","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"wang-editor","component":"demo/wang-editor","name":"WangEditor","meta":{"title":"富文本编辑器","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"upload","component":"demo/upload","name":"Upload","meta":{"title":"图片上传","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"icon-selector","component":"demo/icon-selector","name":"IconSelector","meta":{"title":"图标选择器","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"dict-demo","component":"demo/dict","name":"DictDemo","meta":{"title":"字典组件","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}}]},{"path":"/route-param","component":"Layout","name":"/routeParam","meta":{"title":"路由参数","icon":"el-icon-ElementPlus","hidden":false,"alwaysShow":true,"params":null},"children":[{"path":"route-param-type1","component":"demo/route-param","name":"RouteParamType1","meta":{"title":"参数(type=1)","icon":"el-icon-Star","hidden":false,"keepAlive":true,"alwaysShow":false,"params":{"type":"1"}}},{"path":"route-param-type2","component":"demo/route-param","name":"RouteParamType2","meta":{"title":"参数(type=2)","icon":"el-icon-StarFilled","hidden":false,"keepAlive":true,"alwaysShow":false,"params":{"type":"2"}}}]},{"path":"/function","component":"Layout","name":"/function","meta":{"title":"功能演示","icon":"menu","hidden":false,"alwaysShow":false,"params":null},"children":[{"path":"icon-demo","component":"demo/icons","name":"IconDemo","meta":{"title":"Icons","icon":"el-icon-Notification","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"/function/websocket","component":"demo/websocket","name":"/function/websocket","meta":{"title":"Websocket","icon":"","hidden":false,"keepAlive":true,"alwaysShow":false,"params":null}},{"path":"other/:id","component":"demo/other","name":"Other/:id","meta":{"title":"敬请期待...","icon":"","hidden":false,"alwaysShow":false,"params":null}}]}],"msg":"一切ok"}
#     """
#     ret = json.loads(value)
#     return ORJSONResponse(ret)

@router.get("/routes", response_class=ORJSONResponse)
def get_routes(current_user: CurrentUser):
    menus = pid_cls.get_values(current_user.user_type)
    return ORJSONResponse({"code": "00000", "msg": "ok", "data": menus })
