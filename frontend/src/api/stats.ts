import request from "@/utils/request";

const STATS_BASE_URL = "/api/v1/stats";

class StatsAPI {
  static getVisitTrend(queryParams: VisitTrendQuery) {
    return request<any, VisitTrendVO>({
      url: `${STATS_BASE_URL}/visit-trend`,
      method: "get",
      params: queryParams,
    });
  }
}

export default StatsAPI;

/**  访问趋势视图对象 */
export interface VisitTrendVO {
  /** 日期列表 */
  dates: string[];
  /** 访问次数 */
  times: number[];
  /** 访客数(UV) */
  uvList: number[];
  /** IP数 */
  ipList: number[];
}

/** 访问趋势查询参数 */
export interface VisitTrendQuery {
  /** 开始日期 */
  startDate: string;
  /** 结束日期 */
  endDate: string;
  /** 按最小分组，0表示按分钟，1表示按10分钟，2表示按30分钟 */
  minStep: number;
}
