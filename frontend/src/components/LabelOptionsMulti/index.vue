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
}

onBeforeMount(() => {
  update_value();
});
</script>
