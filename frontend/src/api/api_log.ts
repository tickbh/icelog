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

/**
 * 字典
 */
export interface LogForm {
  time?: Date;
  log_level: number;
  traceId?: string;
  uid: number;
  content: string;
  exid?: string;
  extra?: string;
}
