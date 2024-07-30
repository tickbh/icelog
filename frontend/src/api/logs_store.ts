import request from "@/utils/request";

const LOG_BASE_URL = "/api/v1/logs/store";

class LogsStoreAPI {
  /**
   * 获取日志分页列表
   *
   * @param queryParams 查询参数
   */
  static getPage(queryParams: LogsStorePageQuery) {
    return request<any, PageResult<LogsStorePageVO[]>>({
      url: `${LOG_BASE_URL}/page`,
      method: "get",
      params: queryParams,
    });
  }

  static update(id: number, data: LogsStoreForm) {
    return request({
      url: `${LOG_BASE_URL}/${id}`,
      method: "put",
      data: data,
    });
  }

  static add(data: LogsStoreForm) {
    return request({
      url: `${LOG_BASE_URL}/create`,
      method: "post",
      data: data,
    });
  }

  static getFormData(id: number) {
    return request<any, LogsStoreForm>({
      url: `${LOG_BASE_URL}/form?id=${id}`,
      method: "get",
    });
  }

  static updateConnectUrl(id: number, connect_url: string) {
    return request({
      url: `${LOG_BASE_URL}/url/${id}`,
      method: "patch",
      data: { connect_url: connect_url },
    });
  }

  static deleteByIds(ids: string) {
    return request({
      url: `${LOG_BASE_URL}/${ids}`,
      method: "delete",
    });
  }
}

export default LogsStoreAPI;

export interface LogsStoreForm {
  create_time?: Date;
  store?: string;
  name?: string;
  connect_url?: string;
  table_name?: string;
  table_ext?: string;
  id?: number;
  status?: number;
  sort?: number;
}

/**
 * 日志分页查询对象
 */
export interface LogsStorePageQuery extends PageQuery {
  /** 搜索关键字 */
  keywords?: string;
  status?: number;
}

/**
 * 系统日志分页VO
 */
export interface LogsStorePageVO {
  /** 主键 */
  id: number;
  store: string;
  name: string;
  status: number;
  sort: number;
}
