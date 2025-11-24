<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
    modelValue: File | null
}>();

const emit = defineEmits<{
    (e: "update:modelValue", file: File | null): void
}>();

const previewUrl = ref<string | null>(null);

watch(
    () => props.modelValue,
    (file) => {
        if (!file) {
            previewUrl.value = null;
            return;
        }
        previewUrl.value = URL.createObjectURL(file);
    },
    { immediate: true }
);

function handleFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] || null;

    emit("update:modelValue", file);
}
</script>

<template>
    <div class="flex flex-col items-start gap-2">
        <label class="text-xs text-white/70">Student Photo</label>

        <div
            class="w-24 h-24 rounded-lg overflow-hidden bg-neutral-800 border border-white/20 flex items-center justify-center cursor-pointer"
        >
            <label class="w-full h-full cursor-pointer flex items-center justify-center">
                <input
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleFileChange"
                />
                <img
                    v-if="previewUrl"
                    :src="previewUrl"
                    class="w-full h-full object-cover"
                />
                <span v-else class="text-xs text-white/40">Upload</span>
            </label>
        </div>

        <button
            v-if="previewUrl"
            class="text-xs text-red-400 underline"
            @click="emit('update:modelValue', null)"
        >
            Remove
        </button>
    </div>
</template>
