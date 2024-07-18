import request from "@/utils/request";

const DICT_BASE_URL = "/api/v1/dict";

/**
 * 字典
 */
export interface CacheOptions {
  /**
   * 字典ID
   */
  id?: number;
}

class OptionsAPI {
  static cacheOptions: { [name: string]: { [key: string]: OptionType[] } } = {};
  static lastCacheTime: { [name: string]: number } = {};
  static callback_cache: { [name: string]: Array<any> } = {};

  static doCallback(name: string, data?: OptionType[], error?: any) {
    OptionsAPI.callback_cache[name]?.forEach((value) => {
      if (data) {
        value[0](data);
      } else if (error) {
        value[1](error);
      }
    });
    OptionsAPI.callback_cache[name] = [];
  }

  /**
   * 获取字典的数据项
   *
   * @param typeCode 字典编码
   * @returns 字典数据项
   */
  static getOptions(
    name: string,
    key: string,
    callback: () => Promise<OptionType[]>
  ) {
    return new Promise<OptionType[]>((resolve, reject) => {
      if (!OptionsAPI.cacheOptions[name]) {
        OptionsAPI.cacheOptions[name] = {};
      }
      if (OptionsAPI.cacheOptions[name][key]) {
        return resolve(OptionsAPI.cacheOptions[name][key]);
      }
      var now = new Date().getTime();
      // 5秒内不在发起请求
      if (now - (OptionsAPI.lastCacheTime[name] || 0) < 5000) {
        if (!OptionsAPI.callback_cache[name]) {
          OptionsAPI.callback_cache[name] = [];
        }
        OptionsAPI.callback_cache[name].push([resolve, reject]);
        return;
      }
      OptionsAPI.lastCacheTime[name] = now;
      callback()
        .then((data) => {
          OptionsAPI.cacheOptions[name][key] = data;
          resolve(data);
          OptionsAPI.doCallback(name, data, undefined);
        })
        .catch((error) => {
          reject(error);
          OptionsAPI.doCallback(name, undefined, error);
        });
    });
  }
}

export default OptionsAPI;
