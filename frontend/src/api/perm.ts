import request from "@/utils/request";

const PERM_BASE_URL = "/api/v1/perm";

/** 菜单查询参数 */
export interface PermQuery {
  /** 搜索关键字 */
  keywords?: string;
  groups?: number;
  pageNum?: number;
  pageSize?: number;
}

/** 菜单视图对象 */
export interface PermVO {
  /** 菜单ID */
  id?: number;
  /** 菜单名称 */
  name?: string;
  /** 路由 */
  route?: string;
  /** 代码名字 */
  codename?: string;
  /** 是否展示 */
  is_show?: boolean;
  /** 权限分组 */
  groups?: string;
  /** 权限分组名称 */
  groups_name?: string;
  /** 菜单排序(数字越小排名越靠前) */
  sort?: number;
}

/** 菜单表单对象 */
export interface PermForm {
  /** 菜单ID */
  id?: number;
  /** 父类ID */
  pid?: number;
  /** 菜单名称 */
  name?: string;
  /** ICON */
  route?: string;
  /** 归属对象 */
  codename?: string;
  /** 排序 */
  sort?: number;
  /** 权限分组 */
  groups?: string;
  /** 是否显示 */
  is_show?: boolean;

  /** 创建时间 */
  create_time?: string;
}

class PermAPI {
  /**
   * 获取字典分页列表
   *
   * @param queryParams 查询参数
   * @returns 字典分页结果
   */
  static getPage(queryParams: PermQuery) {
    return request<any, PageResult<PermPageVO[]>>({
      url: `${PERM_BASE_URL}/page`,
      method: "get",
      params: queryParams,
    });
  }

  /**
   * 获取菜单树形列表
   *
   * @param queryParams 查询参数
   * @returns 菜单树形列表
   */
  static getList(queryParams: PermAPI) {
    return request<any, PermAPI[]>({
      url: `${PERM_BASE_URL}`,
      method: "get",
      params: queryParams,
    });
  }

  /**
   * 获取字典表单数据
   *
   * @param id 字典ID
   * @returns 字典表单数据
   */
  static getFormData(id: number) {
    return request<any, PermForm>({
      url: `${PERM_BASE_URL}/form/${id}`,
      method: "get",
    });
  }

  /**
   * 新增字典
   *
   * @param data 字典表单数据
   * @returns 请求结果
   */
  static add(data: PermForm) {
    return request({
      url: `${PERM_BASE_URL}`,
      method: "post",
      data: data,
    });
  }

  /**
   * 修改字典
   *
   * @param id 字典ID
   * @param data 字典表单数据
   * @returns 请求结果
   */
  static update(id: number, data: PermForm) {
    return request({
      url: `${PERM_BASE_URL}/${id}`,
      method: "put",
      data: data,
    });
  }

  /**
   * 删除字典
   *
   * @param ids 字典ID，多个以英文逗号(,)分隔
   * @returns 请求结果
   */
  static deleteByIds(ids: string) {
    return request({
      url: `${PERM_BASE_URL}/${ids}`,
      method: "delete",
    });
  }

  /**
   * 获取字典的数据项
   *
   * @param typeCode 字典编码
   * @returns 字典数据项
   */
  static getOptions() {
    return request<any, OptionType[]>({
      url: `${PERM_BASE_URL}/options`,
      method: "get",
    });
  }

  /**
   * 获取字典的数据项
   *
   * @param typeCode 字典编码
   * @returns 字典数据项
   */
  static getGroupOptions() {
    return request<any, OptionType[]>({
      url: `${PERM_BASE_URL}/group/options`,
      method: "get",
    });
  }
}

export default PermAPI;

/**
 * 字典查询参数
 */
export interface DictPageQuery extends PageQuery {
  /**
   * 关键字(字典名称/编码)
   */
  keywords?: string;
}

/**
 * 字典分页对象
 */
export interface PermPageVO {
  /**
   * 字典ID
   */
  id: number;
  /**
   * 字典名称
   */
  name: string;
  /**
   * 字典编码
   */
  code: string;
  /**
   * 字典状态（1-启用，0-禁用）
   */
  status: number;
  /**
   * 字典项列表
   */
  dictItems: DictItem[];
}

/**
 * 字典项
 */
export interface DictItem {
  /**
   * 字典项ID
   */
  id?: number;
  /**
   * 字典项名称
   */
  name?: string;
  /**
   * 字典项值
   */
  value?: string;
  /**
   * 排序
   */
  sort?: number;
  /**
   * 状态（1-启用，0-禁用）
   */
  status?: number;
}

// TypeScript 类型声明

/**
 * 字典
 */
export interface DictForm {
  /**
   * 字典ID
   */
  id?: number;
  /**
   * 字典名称
   */
  name?: string;
  /**
   * 字典编码
   */
  code?: string;
  /**
   * 字典状态（1-启用，0-禁用）
   */
  status?: number;
  /**
   * 备注
   */
  remark?: string;
  /**
   * 字典数据项列表
   */
  dictItems?: DictItem[];
}
