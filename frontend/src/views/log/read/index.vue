<!-- 日志读取管理 -->
<template>
  <div class="app-container">
    <el-row :gutter="20">
      <!-- 用户列表 -->
      <el-col :lg="20" :xs="24">
        <div class="search-container">
          <el-form ref="queryFormRef" :model="queryParams" :inline="true">
            <el-form-item label="关键字" prop="keywords">
              <el-input
                v-model="queryParams.keywords"
                placeholder="读取方式/名称"
                clearable
                style="width: 200px"
                @keyup.enter="handleQuery"
              />
            </el-form-item>

            <el-form-item label="状态" prop="status">
              <el-select
                v-model="queryParams.status"
                placeholder="全部"
                clearable
                class="!w-[100px]"
              >
                <el-option label="启用" value="1" />
                <el-option label="禁用" value="0" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="handleQuery"
                ><i-ep-search />搜索</el-button
              >
              <el-button @click="handleResetQuery">
                <i-ep-refresh />
                重置</el-button
              >
            </el-form-item>
          </el-form>
        </div>

        <el-card shadow="never" class="table-container">
          <template #header>
            <div class="flex-x-between">
              <div>
                <el-button
                  v-hasPerm="['sys:user:add']"
                  type="success"
                  @click="handleOpenDialog()"
                  ><i-ep-plus />新增</el-button
                >
                <el-button
                  v-hasPerm="['sys:user:delete']"
                  type="danger"
                  :disabled="removeIds.length === 0"
                  @click="handleDelete()"
                  ><i-ep-delete />删除</el-button
                >
              </div>
            </div>
          </template>

          <el-table
            v-loading="loading"
            :data="pageData"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="50" align="center" />
            <el-table-column
              key="id"
              label="编号"
              align="center"
              prop="id"
              width="100"
            />
            <el-table-column
              key="name"
              label="名字"
              align="center"
              prop="name"
            />

            <el-table-column
              key="connect_url"
              label="连接信息"
              width="200"
              align="center"
              prop="connect_url"
            />

            <el-table-column
              key="table_name"
              label="表名或者Topic"
              width="200"
              align="center"
              prop="table_name"
            />

            <el-table-column
              key="table_ext"
              label="表额外信息"
              width="200"
              align="center"
              prop="table_ext"
            />

            <el-table-column
              label="读取方式"
              width="120"
              align="center"
              prop="store"
            >
              <template #default="scope">
                <label-options code="sys_store" :value="scope.row.store" />
              </template>
            </el-table-column>

            <el-table-column label="状态" align="center" prop="status">
              <template #default="scope">
                <el-tag :type="scope.row.status == 1 ? 'success' : 'info'">{{
                  scope.row.status == 1 ? "启用" : "禁用"
                }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="创建时间"
              align="center"
              prop="create_time"
              width="180"
            />
            <el-table-column label="排序" align="center" prop="sort" />
            <el-table-column label="操作" fixed="right" width="220">
              <template #default="scope">
                <el-button
                  v-hasPerm="['sys:user:password:reset']"
                  type="primary"
                  size="small"
                  link
                  @click="handleResetConnectUrl(scope.row)"
                  ><i-ep-refresh-left />重置连接</el-button
                >
                <el-button
                  v-hasPerm="['sys:user:edit']"
                  type="primary"
                  link
                  size="small"
                  @click="handleOpenDialog(scope.row.id)"
                  ><i-ep-edit />编辑</el-button
                >
                <el-button
                  v-hasPerm="['sys:user:delete']"
                  type="danger"
                  link
                  size="small"
                  @click="handleDelete(scope.row.id)"
                  ><i-ep-delete />删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>

          <pagination
            v-if="total > 0"
            v-model:total="total"
            v-model:page="queryParams.pageNum"
            v-model:limit="queryParams.pageSize"
            @pagination="handleQuery"
          />
        </el-card>
      </el-col>
    </el-row>

    <!-- 用户表单弹窗 -->
    <el-drawer
      v-model="dialog.visible"
      :title="dialog.title"
      append-to-body
      @close="handleCloseDialog"
    >
      <!-- 用户新增/编辑表单 -->
      <el-form
        ref="storeFormRef"
        :model="formData"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入名称" />
        </el-form-item>

        <el-form-item label="读取方式" prop="store">
          <dictionary v-model="formData.store" code="sys_store" />
        </el-form-item>

        <el-form-item label="连接信息" prop="connect_url" v-if="!formData.id">
          <el-input
            v-model="formData.connect_url"
            placeholder="请输入密码, 6位到50位"
            maxlength="50"
          />
        </el-form-item>

        <el-form-item label="表名信息或者Topic" prop="table_name">
          <el-input v-model="formData.table_name" placeholder="请输入表名" />
        </el-form-item>

        <el-form-item label="额外表信息" prop="table_ext">
          <el-input v-model="formData.table_ext" placeholder="请输入表名" />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :label="1">正常</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="排序" prop="sort">
          <el-input-number
            v-model="formData.sort"
            style="width: 100px"
            controls-position="right"
            :min="0"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="handleSubmit">确 定</el-button>
          <el-button @click="handleCloseDialog">取 消</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "User",
  inheritAttrs: false,
});

import UserAPI, { UserForm, UserPageQuery, UserPageVO } from "@/api/user";
import LogsReadAPI, {
  LogsReadForm,
  LogsReadPageVO,
  LogsReadPageQuery,
} from "@/api/logs_read";

const queryFormRef = ref(ElForm);
const storeFormRef = ref(ElForm);

const loading = ref(false);
const removeIds = ref([]);
const total = ref(0);
const pageData = ref<LogsReadPageVO[]>();
/** 角色下拉选项 */
const roleOptions = ref<OptionType[]>();
/** 用户查询参数  */
const queryParams = reactive<LogsReadPageQuery>({
  pageNum: 1,
  pageSize: 10,
});

/**  用户弹窗对象  */
const dialog = reactive({
  visible: false,
  title: "",
});

/** 导入弹窗显示状态 */
const importDialogVisible = ref(false);

// 用户表单数据
const formData = reactive<LogsReadForm>({
  status: 1,
});

/** 用户表单校验规则  */
const rules = reactive({
  name: [{ required: true, message: "名称不能为空", trigger: "blur" }],
  connect_url: [
    { required: true, message: "连接信息不能为空", trigger: "blur" },
  ],
  store: [{ required: true, message: "读取方式不能为空", trigger: "blur" }],
});

/** 查询 */
function handleQuery() {
  loading.value = true;
  LogsReadAPI.getPage(queryParams)
    .then((data) => {
      console.log("handleQuery", data);
      pageData.value = data.list;
      total.value = data.total;
    })
    .finally(() => {
      loading.value = false;
    });
}

/** 重置查询 */
function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryParams.pageNum = 1;
  handleQuery();
}

/** 行复选框选中记录选中ID集合 */
function handleSelectionChange(selection: any) {
  removeIds.value = selection.map((item: any) => item.id);
}

function check_url_right(url: string): boolean {
  try {
    let u = new URL(url);
    if (u.protocol.length == 0) {
      return false;
    }
    return true;
  } catch (error) {
    return false;
  }
  return false;
}

/** 重置密码 */
function handleResetConnectUrl(row: { [key: string]: any }) {
  ElMessageBox.prompt(
    "请输入「" + row.name + "」的新连接, 原链接信息为: " + row.connect_url + "",
    "重置链接",
    {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      beforeClose: (a, i, done) => {
        if (a == "confirm") {
          if (!i.inputValue || i.inputValue.length < 6) {
            // 检查密码是否为空或少于6位
            ElMessage.warning("链接至少需要6位字符，请重新输入");
            return false;
          }
          if (!check_url_right(i.inputValue)) {
            ElMessage.warning("非合法的url对象, 请重新输入");
            return false;
          }
          done();
        } else {
          done();
        }
      },
    }
  )
    .then(({ value }) => {
      console.log("ok!!");
      LogsReadAPI.updateConnectUrl(row.id, value).then(() => {
        ElMessage.success("链接重置成功，新链接是：" + value);
      });
    })
    .catch((e) => {});
}

/**
 * 打开弹窗
 *
 * @param id 用户ID
 */
async function handleOpenDialog(id?: number) {
  dialog.visible = true;
  // 加载角色下拉数据源
  roleOptions.value = [];

  if (id) {
    dialog.title = "修改用户";
    LogsReadAPI.getFormData(id).then((data) => {
      Object.assign(formData, { ...data });
    });
  } else {
    dialog.title = "新增用户";
  }
}

/** 关闭弹窗 */
function handleCloseDialog() {
  dialog.visible = false;
  storeFormRef.value.resetFields();
  storeFormRef.value.clearValidate();

  formData.id = undefined;
  formData.status = 1;
}

/** 表单提交 */
const handleSubmit = useThrottleFn(() => {
  storeFormRef.value.validate((valid: any) => {
    if (valid) {
      if (formData.connect_url && !check_url_right(formData.connect_url)) {
        ElMessage.warning("非合法的url对象, 请重新输入");
        return false;
      }
      const userId = formData.id;
      loading.value = true;
      if (userId) {
        LogsReadAPI.update(userId, formData)
          .then(() => {
            ElMessage.success("修改用户成功");
            handleCloseDialog();
            handleResetQuery();
          })
          .finally(() => (loading.value = false));
      } else {
        LogsReadAPI.add(formData)
          .then(() => {
            ElMessage.success("新增用户成功");
            handleCloseDialog();
            handleResetQuery();
          })
          .finally(() => (loading.value = false));
      }
    }
  });
}, 3000);

/** 删除用户 */
function handleDelete(id?: number) {
  const userIds = [id || removeIds.value].join(",");
  if (!userIds) {
    ElMessage.warning("请勾选删除项");
    return;
  }

  ElMessageBox.confirm("确认删除用户?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(
    function () {
      loading.value = true;
      LogsReadAPI.deleteByIds(userIds)
        .then(() => {
          ElMessage.success("删除成功");
          handleResetQuery();
        })
        .finally(() => (loading.value = false));
    },
    function () {
      ElMessage.info("已取消删除");
    }
  );
}
/** 打开导入弹窗 */
function handleOpenImportDialog() {
  importDialogVisible.value = true;
}

onMounted(() => {
  handleQuery();
});
</script>
