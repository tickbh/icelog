(function () {
  var original_trace = console.trace;
  var original_log = console.log;
  var original_info = console.info;
  var original_warn = console.warn;
  var original_error = console.error;
  var instance = null;
  function getInstance() {
    var level_trace = 5
    var level_log = 4
    var level_info = 3
    var level_warn = 2
    var level_error = 1
    function guid() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
          v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }

    var log_instance = {
      is_init: false,
      log_array: [],
      request_api: null,
      request_project: "default",
      request_uid: 0,
      request_exid: "",
      request_sys: "unknow",
      heart_time: undefined,
      append_log: function (level, msg) {
        log_array.push({
          lv: level,
          time: new Date(),
          tid: guid(),
          uid: request_uid,
          exid: request_exid,
          extra: "",
          sys: request_sys,
        })
      },
      updateTimer: function () {

      },
      init: function (api, project, uid, exid, sys) {
        request_api = api;
        request_project = project
        request_uid = uid
        request_exid = exid
        request_sys = sys
        if (this.is_init) {
          return;
        }
        console.log("初始化iceslog!!!!!!!")
        this.is_init = true;

        var self = this;
        function setHeartTimer() {
          if (!self.is_init || self.heart_time) {
            return;
          }
          self.heart_time = setTimeout(function () {
            self.heart_time = null
            if (!self.is_init) {
              return;
            }
            self.updateTimer();
          }, 10000)
        }
        setHeartTimer()
        console.trace = function () {
          try {
            // 将所有参数转换为字符串并连接它们
            var message = [].slice.call(arguments).map(function (arg) {
              return typeof arg === 'object' ? JSON.stringify(arg) : arg;
            }).join(' ');
            append_log(level_trace, message)
          } catch (error) {
          }
          // 调用原始的console.log函数输出结果
          original_trace.call(console, ...arguments);
        };

        console.info = function () {
          try {
            // 将所有参数转换为字符串并连接它们
            var message = [].slice.call(arguments).map(function (arg) {
              return typeof arg === 'object' ? JSON.stringify(arg) : arg;
            }).join(' ');
            append_log(level_info, message)
          } catch (error) {
          }
          // 调用原始的console.log函数输出结果
          original_info.call(console, ...arguments);
        };
        console.log = function () {
          try {
            // 将所有参数转换为字符串并连接它们
            var message = [].slice.call(arguments).map(function (arg) {
              return typeof arg === 'object' ? JSON.stringify(arg) : arg;
            }).join(' ');
            append_log(level_log, message)
          } catch (error) {
          }
          // 调用原始的console.log函数输出结果
          original_log.call(console, ...arguments);
        };
        console.warn = function () {
          try {
            // 将所有参数转换为字符串并连接它们
            var message = [].slice.call(arguments).map(function (arg) {
              return typeof arg === 'object' ? JSON.stringify(arg) : arg;
            }).join(' ');
            append_log(level_warn, message)
          } catch (error) {
          }
          // 调用原始的console.log函数输出结果
          original_warn.call(console, ...arguments);
        };
        console.error = function () {
          try {
            // 将所有参数转换为字符串并连接它们
            var message = [].slice.call(arguments).map(function (arg) {
              return typeof arg === 'object' ? JSON.stringify(arg) : arg;
            }).join(' ');
            append_log(level_error, message)
          } catch (error) {
          }
          // 调用原始的console.log函数输出结果
          original_error.apply(console, arguments);
        };
      },
      close: function () {
        this.is_init = false;
        console.trace = original_trace;
        console.log = original_log;
        console.info = original_info;
        console.warn = original_warn;
        console.error = original_error;
        console.log("关闭iceslog!!!!!!!")

        if (self.heart_time) {
          clearTimeout(self.heart_time)
          self.heart_time = null;
        }
      }
    }
    return log_instance
  }

  return {
    instance: function () {
      if (instance === null) {
        instance = getInstance();
      }
      return instance;
    }
  };
})();