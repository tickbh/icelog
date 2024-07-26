import request from "@/utils/request";

const LOG_BASE_URL = "/api/v1/logs/search";

class LogsSearchAPI {
  /**
   * 获取日志分页列表
   *
   * @param queryParams 查询参数
   */
  static getPage(queryParams: LogsSearchPageQuery) {
    return request<any, PageResult<LogsSearchPageVO[]>>({
      url: `${LOG_BASE_URL}/page`,
      method: "get",
      params: queryParams,
    });
  }

  static update(id: number, data: LogsSearchForm) {
    return request({
      url: `${LOG_BASE_URL}/${id}`,
      method: "put",
      data: data,
    });
  }

  static add(data: LogsSearchForm) {
    return request({
      url: `${LOG_BASE_URL}/create`,
      method: "post",
      data: data,
    });
  }

  static getFormData(id: number) {
    return request<any, LogsSearchForm>({
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

export default LogsSearchAPI;

export interface LogsSearchForm {
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
export interface LogsSearchPageQuery extends PageQuery {
  /** 搜索关键字 */
  content?: string;
  read?: number;
  /** 搜索关键字 */
  sys?: string;
  level?: number;
  status?: number;
  /** 开始时间 */
  startTime?: string;

  /** 结束时间 */
  endTime?: string;
}

/**
 * 系统日志分页VO
 */
export interface LogsSearchPageVO {
  /** 主键 */
  id: number;
  Search: string;
  name: string;
  status: number;
  sort: number;
}
