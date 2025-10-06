<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
    modelValue: string
    label?: string
    type?: string
    placeholder?: string
    error?: string
}>()

const emit = defineEmits(['update:modelValue'])

const showPassword = ref(false)

// Dynamically switch input type
const inputType = computed(() => {
    if (props.type === 'password') {
        return showPassword.value ? 'text' : 'password'
    }
    return props.type || 'text'
})
</script>

<template>
    <div class="flex flex-col gap-1">
        <!-- Label + Error -->
        <div class="flex justify-between items-center">
            <label v-if="label" class="text-gray-300 text-sm">{{ label }}</label>
            <span v-if="error" class="text-red-400 text-xs">{{ error }}</span>
        </div>

        <!-- Input Wrapper -->
        <div class="relative">
            <input
                :type="inputType"
                :placeholder="placeholder"
                :value="modelValue"
                @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
                class="w-full px-4 py-2 rounded-lg bg-glass border text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10"
                :class="error ? 'border-red-500 focus:ring-red-500' : 'border-white/20'"
            />

            <!-- Eye Toggle -->
           <button
                v-if="props.type === 'password'"
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-3 flex items-center cursor-pointer opacity-70 hover:opacity-100 transition"
                tabindex="-1"
            >
                <img
                    v-if="!showPassword"
                    src="/src/assets/icons/visibility.svg"
                    alt="Show password"
                    class="w-4 h-4"
                />
                <img
                    v-else
                    src="/src/assets/icons/visibility-off.svg"
                    alt="Hide password"
                    class="w-4 h-4"
                />
            </button>
        </div>
    </div>
</template>
