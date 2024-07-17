<template>
  <div>{{ selectedValue }}</div>
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
    type: [String, Number],
  },
  value: {
    type: String,
  },
});

const emits = defineEmits(["update:modelValue"]);

const selectedValue = ref<string | number | undefined>();

function handleChange(val?: string | number | undefined) {
  emits("update:modelValue", val);
}

onBeforeMount(() => {
  // 根据字典编码获取字典项
  DictAPI.getOptions(props.code).then((data) => {
    data.forEach((val) => {
      if (val.value == props.value) {
        selectedValue.value = val.label;
      }
    });
  });
});
</script>
