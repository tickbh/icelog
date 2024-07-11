<template>
  <div class="app-container">
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryParams" :inline="true">
        <el-form-item label="关键字" prop="keywords">
          <el-input
            v-model="queryParams.keywords"
            placeholder="菜单名称"
            clearable
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item label="分组" prop="groups">
          <el-input
            v-model="queryParams.groups"
            placeholder="分组信息"
            clearable
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery"
            ><template #icon><i-ep-search /></template>搜索</el-button
          >
          <el-button @click="handleResetQuery">
            <template #icon><i-ep-refresh /></template>
            重置</el-button
          >
        </el-form-item>
      </el-form>
    </div>

    <el-card shadow="never" class="table-container">
      <template #header>
        <el-button
          v-hasPerm="['sys:menu:add']"
          type="success"
          @click="handleOpenDialog(0)"
        >
          <template #icon><i-ep-plus /></template>
          新增</el-button
        >
      </template>

      <el-table
        v-loading="loading"
        :data="permTableData"
        highlight-current-row
        row-key="id"
        :expand-row-keys="['1']"
      >
        <el-table-column label="权限名称" min-width="200">
          <template #default="scope"> {{ scope.row.name }} </template>
        </el-table-column>

        <el-table-column label="路由" align="left" width="150" prop="route" />

        <el-table-column
          label="代码名称"
          align="left"
          width="150"
          prop="codename"
        />

        <el-table-column
          label="分组权限"
          align="left"
          width="250"
          prop="groups_name"
        />

        <el-table-column label="排序" align="left" width="80" prop="sort" />

        <el-table-column
          label="创建时间"
          align="center"
          width="200"
          prop="create_time"
        />

        <el-table-column fixed="right" align="center" label="操作" width="220">
          <template #default="scope">
            <el-button
              v-hasPerm="['sys:menu:edit']"
              type="primary"
              link
              size="small"
              @click.stop="handleOpenDialog(scope.row.id)"
            >
              <i-ep-edit />编辑
            </el-button>
            <el-button
              v-hasPerm="['sys:menu:delete']"
              type="danger"
              link
              size="small"
              @click.stop="handleDelete(scope.row.id)"
              ><i-ep-delete />
              删除
            </el-button>
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

    <el-drawer
      v-model="dialog.is_show"
      :title="dialog.title"
      @close="handleCloseDialog"
      size="50%"
    >
      <el-form
        ref="menuFormRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <!-- <el-form-item label="归属" prop="belong">
          <el-input v-model="formData.belong" placeholder="请输入归属" />
        </el-form-item> -->

        <el-form-item label="权限名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入归属" />
        </el-form-item>

        <el-form-item label="权限路由" prop="route">
          <el-input v-model="formData.route" placeholder="请输入" />
        </el-form-item>

        <el-form-item label="权限代码" prop="route">
          <el-input v-model="formData.codename" placeholder="请输入" />
        </el-form-item>

        <el-form-item label="权限分组" prop="groups">
          <perm-multi v-model:value="formData.groups" />
        </el-form-item>

        <el-form-item prop="is_show" label="显示状态">
          <el-radio-group v-model="formData.is_show">
            <el-radio :value="true">显示</el-radio>
            <el-radio :value="false">隐藏</el-radio>
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
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="handleCloseDialog">取 消</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Menu",
  inheritAttrs: false,
});

import MenuAPI, { MenuQuery, MenuForm, MenuVO } from "@/api/menu";
import PermAPI, { PermForm, PermQuery, PermVO } from "@/api/perm";
import { MenuTypeEnum } from "@/enums/MenuTypeEnum";

const queryFormRef = ref(ElForm);
const menuFormRef = ref(ElForm);

const total = ref(0);
const loading = ref(false);
const dialog = reactive({
  title: "新增菜单",
  is_show: false,
});

// 查询参数
const queryParams = reactive<PermQuery>({
  pageNum: 1,
  pageSize: 10,
});
// 菜单表格数据
const permTableData = ref<PermVO[]>([]);
// 顶级菜单下拉选项
const permOptions = ref<OptionType[]>([]);

// 初始菜单表单数据
const initialPermFormData = ref<PermForm>({
  id: 0,
  sort: 1,
  route: "",
  codename: "",
  name: "",
  is_show: true,
});

// 菜单表单数据
const formData = ref({ ...initialPermFormData.value });

// 表单验证规则
const rules = reactive({
  route: [{ required: true, message: "请选择路由", trigger: "blur" }],
  codename: [{ required: true, message: "请输入代码", trigger: "blur" }],
  name: [{ required: true, message: "请选择名称", trigger: "blur" }],
});

// 选择表格的行菜单ID
const selectedMenuId = ref<number | undefined>();

// 查询
function handleQuery() {
  loading.value = true;
  PermAPI.getPage(queryParams)
    .then((data) => {
      permTableData.value = data.list;
      total.value = data.total;
    })
    .finally(() => {
      loading.value = false;
    });
}

// 重置查询
function handleResetQuery() {
  queryFormRef.value.resetFields();
  handleQuery();
}

/**
 * 打开表单弹窗
 *
 */
function handleOpenDialog(permId?: number) {
  dialog.is_show = true;
  if (permId) {
    dialog.title = "编辑菜单";
    PermAPI.getFormData(permId).then((data) => {
      console.log("data === ", data);
      initialPermFormData.value = { ...data };
      formData.value = data;
    });
  } else {
    dialog.title = "新增菜单";
  }
}

/** 菜单保存提交 */
function submitForm() {
  menuFormRef.value.validate((isValid: boolean) => {
    if (isValid) {
      const permId = formData.value.id;
      if (permId) {
        PermAPI.update(permId, formData.value).then(() => {
          ElMessage.success("修改成功");
          handleCloseDialog();
          handleQuery();
        });
      } else {
        PermAPI.add(formData.value).then(() => {
          ElMessage.success("新增成功");
          handleCloseDialog();
          handleQuery();
        });
      }
    }
  });
}

// 删除菜单
function handleDelete(menuId: number) {
  if (!menuId) {
    ElMessage.warning("请勾选删除项");
    return false;
  }

  ElMessageBox.confirm("确认删除已选中的数据项?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(
    () => {
      loading.value = true;
      PermAPI.deleteByIds("" + menuId)
        .then(() => {
          ElMessage.success("删除成功");
          handleQuery();
        })
        .finally(() => {
          loading.value = false;
        });
    },
    () => {
      ElMessage.info("已取消删除");
    }
  );
}

// 关闭弹窗
function handleCloseDialog() {
  dialog.is_show = false;
  menuFormRef.value.resetFields();
  menuFormRef.value.clearValidate();
  formData.value.id = 0;
}

onMounted(() => {
  handleQuery();
});
</script>
