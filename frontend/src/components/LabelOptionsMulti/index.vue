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

function handleChange(val?: string | number | undefined) {
  emits("update:modelValue", val);
}

function get_options(): Promise<OptionType[]> {
  if (props.options == "role") {
    return RoleAPI.getOptions();
  }
  return DictAPI.getOptions(props.code);
}

onBeforeMount(() => {
  // 根据字典编码获取字典项
  get_options().then((data) => {
    var final = "";
    data.forEach((val) => {
      var vals = props.value?.split("|");
      if (vals?.includes(val.value + "")) {
        if (final.length > 0) {
          final += "|";
        }
        final += val.label;
      }
    });
    selectedValue.value = final;
  });
});
</script>
