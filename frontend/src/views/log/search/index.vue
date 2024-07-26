<template>
  <div class="app-container">
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryParams" :inline="true">
        <el-form-item label="过滤内容" prop="keywords">
          <el-input
            v-model="queryParams.content"
            placeholder="过滤内容"
            clearable
            @keyup.enter="handleQuery"
          />
        </el-form-item>

        <el-form-item label="创建时间">
          <el-date-picker
            class="!w-[240px]"
            v-model="dateTimeRange"
            type="daterange"
            range-separator="~"
            start-placeholder="开始时间"
            end-placeholder="截止时间"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <el-form-item label="系统">
          <dictionary
            v-model="queryParams.sys"
            code="sys_sys"
            class="!w-[140px]"
          />
        </el-form-item>

        <el-form-item label="读取库">
          <select-options
            v-model="queryParams.read"
            code=""
            rule="logs_read"
            class="!w-[140px]"
          />
        </el-form-item>

        <el-form-item label="日志等级">
          <dictionary
            v-model="queryParams.level"
            code="sys_level"
            class="!w-[140px]"
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
        <el-button v-hasPerm="['sys:menu:add']" type="success" @click="">
          <template #icon><i-ep-plus /></template>
          新增</el-button
        >
      </template>

      <el-table
        v-loading="loading"
        :data="searchTableData"
        highlight-current-row
        row-key="id"
        :expand-row-keys="['1']"
        @row-click="handleRowClick"
        :tree-props="{
          children: 'children',
          hasChildren: 'hasChildren',
        }"
      >
        <el-table-column label="菜单名称" min-width="200">
          <template #default="scope">
            <template
              v-if="scope.row.icon && scope.row.icon.startsWith('el-icon')"
            >
              <el-icon style="vertical-align: -0.15em">
                <component :is="scope.row.icon.replace('el-icon-', '')" />
              </el-icon>
            </template>
            <template v-else-if="scope.row.icon">
              <svg-icon :icon-class="scope.row.icon" />
            </template>
            <template v-else>
              <svg-icon icon-class="menu" />
            </template>
            {{ scope.row.name }}
          </template>
        </el-table-column>

        <el-table-column label="类型" align="center" width="80">
          <template #default="scope">
            <el-tag
              v-if="scope.row.type === MenuTypeEnum.CATALOG"
              type="warning"
              >目录</el-tag
            >
            <el-tag v-if="scope.row.type === MenuTypeEnum.MENU" type="success"
              >菜单</el-tag
            >
            <el-tag v-if="scope.row.type === MenuTypeEnum.BUTTON" type="danger"
              >按钮</el-tag
            >
            <el-tag v-if="scope.row.type === MenuTypeEnum.EXTLINK" type="info"
              >外链</el-tag
            >
          </template>
        </el-table-column>

        <el-table-column
          label="归属对象"
          align="left"
          width="150"
          prop="belong"
        />

        <el-table-column
          label="路由路径"
          align="left"
          width="150"
          prop="path"
        />

        <el-table-column
          label="组件路径"
          align="left"
          width="250"
          prop="component"
        />

        <el-table-column
          label="权限标识"
          align="center"
          width="200"
          prop="perm"
        />

        <el-table-column label="状态" align="center" width="80">
          <template #default="scope">
            <el-tag v-if="scope.row.status === 1" type="success">显示</el-tag>
            <el-tag v-else type="info">隐藏</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="排序" align="center" width="80" prop="sort" />

        <el-table-column fixed="right" align="center" label="操作" width="220">
          <template #default="scope">
            <el-button
              v-if="scope.row.type == 'CATALOG' || scope.row.type == 'MENU'"
              v-hasPerm="['sys:menu:add']"
              type="primary"
              link
              size="small"
              @click.stop=""
            >
              <i-ep-plus />新增
            </el-button>

            <el-button
              v-hasPerm="['sys:menu:edit']"
              type="primary"
              link
              size="small"
              @click.stop=""
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
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Menu",
  inheritAttrs: false,
});

import LogsSearchAPI, {
  LogsSearchPageQuery,
  LogsSearchPageVO,
} from "@/api/logs_search";
import MenuAPI, { MenuQuery, MenuForm, MenuVO } from "@/api/menu";
import { MenuTypeEnum } from "@/enums/MenuTypeEnum";

const queryFormRef = ref(ElForm);
const menuFormRef = ref(ElForm);

const dateTimeRange = ref("");
watch(dateTimeRange, (newVal) => {
  if (newVal) {
    queryParams.startTime = newVal[0];
    queryParams.endTime = newVal[1];
  } else {
    queryParams.startTime = undefined;
    queryParams.endTime = undefined;
  }
});

const loading = ref(false);
const dialog = reactive({
  title: "新增菜单",
  is_show: false,
});

// 查询参数
const queryParams = reactive<LogsSearchPageQuery>({
  pageNum: 1,
  pageSize: 10,
});
// 菜单表格数据
const searchTableData = ref<LogsSearchPageVO[]>([]);

// 初始菜单表单数据
const initialMenuFormData = ref<MenuForm>({
  id: undefined,
  pid: 0,
  status: 1,
  sort: 1,
  type: MenuTypeEnum.MENU, // 默认菜单
  alwaysShow: 0,
  keepAlive: 1,
  params: "",
  belong: "",
});

// 菜单表单数据
const formData = ref({ ...initialMenuFormData.value });

// 表单验证规则
const rules = reactive({
  pid: [{ required: true, message: "请选择顶级菜单", trigger: "blur" }],
  name: [{ required: true, message: "请输入菜单名称", trigger: "blur" }],
  type: [{ required: true, message: "请选择菜单类型", trigger: "blur" }],
  belong: [{ required: true, message: "请选择归属信息", trigger: "blur" }],
  // routeName: [{ required: true, message: "请输入路由名称", trigger: "blur" }],
  path: [{ required: true, message: "请输入路由路径", trigger: "blur" }],
  component: [{ required: true, message: "请输入组件路径", trigger: "blur" }],
  status: [{ required: true, message: "请输入状态", trigger: "blur" }],
});

// 选择表格的行菜单ID
const selectedMenuId = ref<number | undefined>();

// 查询
function handleQuery() {
  loading.value = true;
  LogsSearchAPI.getPage(queryParams)
    .then((data) => {
      searchTableData.value = data.list;
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

// 行点击事件
function handleRowClick(row: MenuVO) {
  // 记录表格选择的菜单ID，新增子菜单作为父菜单ID
  selectedMenuId.value = row.id;
}

// 菜单类型切换
function handleMenuTypeChange() {
  // 如果菜单类型改变
  if (formData.value.type !== initialMenuFormData.value.type) {
    if (formData.value.type === MenuTypeEnum.MENU) {
      // 目录切换到菜单时，清空组件路径
      if (initialMenuFormData.value.type === MenuTypeEnum.CATALOG) {
        formData.value.component = "";
      } else {
        // 其他情况，保留原有的组件路径
        formData.value.path = initialMenuFormData.value.path;
        formData.value.component = initialMenuFormData.value.component;
      }
    }
  }
}

/** 菜单保存提交 */
function submitForm() {
  menuFormRef.value.validate((isValid: boolean) => {
    if (isValid) {
      const menuId = formData.value.id;
      if (menuId) {
        MenuAPI.update(menuId, formData.value).then(() => {
          ElMessage.success("修改成功");
          handleCloseDialog();
          handleQuery();
        });
      } else {
        MenuAPI.add(formData.value).then(() => {
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
      MenuAPI.deleteById(menuId)
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
  formData.value.belong = "";
}

onMounted(() => {
  handleQuery();
});
</script>
