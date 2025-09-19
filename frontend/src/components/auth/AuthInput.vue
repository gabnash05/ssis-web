<script setup lang="ts">
defineProps<{
    modelValue: string
    label?: string
    type?: string
    placeholder?: string
    error?: string
}>()

defineEmits(['update:modelValue'])
</script>

<template>
    <div class="flex flex-col gap-1">
        <!-- Label + Error -->
        <div class="flex justify-between items-center">
            <label v-if="label" class="text-gray-300 text-sm">{{ label }}</label>
            <span v-if="error" class="text-red-400 text-xs">{{ error }}</span>
        </div>

        <!-- Input -->
        <input
            :type="type"
            :placeholder="placeholder"
            :value="modelValue"
            @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
            class="w-full px-4 py-2 rounded-lg bg-glass border text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="error ? 'border-red-500 focus:ring-red-500' : 'border-white/20'"
        />
    </div>
</template>
