<template>
  <div>{{ selectedValue }}</div>
</template>

<script setup lang="ts">
import DictAPI from "@/api/dict";
import RoleAPI from "@/api/role";

const props = defineProps({
  /**
   * 字典编码(eg: 性别-gender)
   */
  code: {
    type: String,
    required: true,
  },
  value: {
    type: String,
    required: true,
  },
  options: {
    type: String,
  },
});

const emits = defineEmits(["update:modelValue"]);

const selectedValue = ref<string | number | undefined>();

watch([props.value, () => props.value], ([newOptions, newModelValue]) => {
  update_value();
});

function get_options(): Promise<OptionType[]> {
  if (props.options == "role") {
    return RoleAPI.getOptions();
  }
  return DictAPI.getOptions(props.code);
}

function update_value() {
  get_options().then((data) => {
    data.forEach((val) => {
      if (val.value == props.value) {
        selectedValue.value = val.label;
      }
    });
  });
}

onBeforeMount(() => {
  update_value();
});
</script>
