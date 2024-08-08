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
      repeat_idx: 0,
      append_log: function (level, msg) {
        this.log_array.push({
          lv: level,
          create: new Date(),
          tid: guid(),
          uid: this.request_uid,
          exid: this.request_exid,
          extra: "",
          msg: msg,
          sys: this.request_sys,
        })
      },
      updateTimer: function () {
        this.repeat_idx += 1;
        if (this.log_array.length == 0) {
          return;
        }
        if (this.log_array.length * 1 < this.repeat_idx && this.repeat_idx < 5) {
          return;
        }
        this.repeat_idx = 0;
        var xhr = new XMLHttpRequest()
        // 2. 调用 open 函数
        xhr.open('POST', this.request_api + "?project=" + this.request_project)
        // 3. 设置 Content-Type 属性（固定写法）
        xhr.setRequestHeader('Content-Type', 'application/json')

        var data = JSON.stringify(this.log_array)
        this.log_array = []
        // 4. 调用 send 函数
        xhr.send(data)
        // 5. 监听事件
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            // console.log(xhr.responseText)
          }
        }
      },
      init: function (api, project, uid, exid, sys) {
        console.log("初始化:", api)
        try {
          let u = new URL(api);
          if (u.protocol != "http:" && u.protocol != "https:") {
            console.error("无效的api", api, u.protocol)
            return false;
          }
        } catch (error) {
          console.error("无效的api", api)
          return false;
        }
        var self = this;
        this.request_project = project || "default"
        this.request_api = api;
        this.request_uid = uid || 0;
        this.request_exid = exid || "";
        this.request_sys = sys || "unknow"
        this.is_init = true;
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
            setHeartTimer();
          }, 1000)
        }
        setHeartTimer()
        console.trace = function () {
          try {
            // 将所有参数转换为字符串并连接它们
            var message = [].slice.call(arguments).map(function (arg) {
              return typeof arg === 'object' ? JSON.stringify(arg) : arg;
            }).join(' ');
            self.append_log(level_trace, message)
          } catch (error) {
            console.error("无效的api", error)
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
            self.append_log(level_info, message)
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
            self.append_log(level_log, message)
          } catch (error) {
            console.error("无效的api", error)
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
            self.append_log(level_warn, message)
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
            self.append_log(level_error, message)
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