<template>
  <el-select
    v-model="selectedValues"
    multiple
    :placeholder="placeholder"
    :disabled="disabled"
    clearable
    @change="handleChange"
  >
    <el-option
      v-for="option in options"
      :key="option.value"
      :label="option.label"
      :value="option.value"
    />
  </el-select>
</template>

<script setup lang="ts">
import DictAPI from "@/api/dict";

const props = defineProps({
  /**
   * 字典编码(eg: 性别-gender)
   */
  code: {
    type: String,
    required: true,
  },
  modelValue: {
    type: String,
  },
  value: {
    type: String,
  },
  placeholder: {
    type: String,
    default: "请选择",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits(["update:modelValue", "update:value"]);

const options: Ref<OptionType[]> = ref([]);

const selectedValues = ref<string[] | number[] | undefined>();

watch([options, () => props.modelValue], ([newOptions, newModelValue]) => {
  if (newOptions.length === 0) {
    // 下拉数据源加载未完成不回显
    return;
  }
  if (newModelValue == undefined) {
    selectedValues.value = undefined;
    return;
  }
  selectedValues.value = newModelValue as any as string[];
});

function handleChange(val?: string[] | number[] | undefined) {
  emits("update:modelValue", val);
  if (val != undefined) {
    emits("update:value", val.join("|"));
  }
}

onBeforeMount(() => {
  // 根据字典编码获取字典项
  DictAPI.getOptions(props.code).then((data) => {
    selectedValues.value = props.value?.split("|");
    options.value = data;
  });
});

onMounted(() => {});
</script>
