import request from "@/utils/request";

const LOG_BASE_URL = "/api/v1/logs/read";

class LogsReadAPI {
  /**
   * 获取日志分页列表
   *
   * @param queryParams 查询参数
   */
  static getPage(queryParams: LogsReadPageQuery) {
    return request<any, PageResult<LogsReadPageVO[]>>({
      url: `${LOG_BASE_URL}/page`,
      method: "get",
      params: queryParams,
    });
  }

  static update(id: number, data: LogsReadForm) {
    return request({
      url: `${LOG_BASE_URL}/${id}`,
      method: "put",
      data: data,
    });
  }

  static add(data: LogsReadForm) {
    return request({
      url: `${LOG_BASE_URL}/create`,
      method: "post",
      data: data,
    });
  }

  static getFormData(id: number) {
    return request<any, LogsReadForm>({
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

export default LogsReadAPI;

export interface LogsReadForm {
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
export interface LogsReadPageQuery extends PageQuery {
  /** 搜索关键字 */
  keywords?: string;
}

/**
 * 系统日志分页VO
 */
export interface LogsReadPageVO {
  /** 主键 */
  id: number;
  Read: string;
  name: string;
  status: number;
  sort: number;
}
