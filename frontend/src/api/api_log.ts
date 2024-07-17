import request from "@/utils/request";

const LOG_BASE_URL = "/api/v1/pub/log";

class ApiLogAPI {
  static add_one(data: LogForm) {
    return request({
      url: `${LOG_BASE_URL}`,
      method: "post",
      data: data,
    });
  }

  static add_many(data: LogForm[]) {
    return request({
      url: `${LOG_BASE_URL}/batch`,
      method: "post",
      data: data,
    });
  }
}

export default ApiLogAPI;

export interface LogForm {
  time?: Date;
  log_level: number;
  traceId?: string;
  uid: number;
  content: string;
  exid?: string;
  extra?: string;
}

export interface LogStoreForm {
  create_time?: Date;
  store?: string;
  name?: string;
  connect_url?: string;
  id?: number;
  status?: number;
}

export interface LogStorePageQuery extends PageQuery {
  /** 搜索关键字 */
  keywords?: string;

  /** 用户状态 */
  status?: number;

  /** 开始时间 */
  startTime?: string;

  /** 结束时间 */
  endTime?: string;
}

/** 日志存储分页 */
export interface LogStorePageVO {
  create_time?: Date;
  store?: string;
  name?: string;
  connect_url?: string;
  id?: number;
  status?: number;
}
