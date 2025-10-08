<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'

defineProps<{
    disabled?: boolean
    loading?: boolean
}>()
</script>

<template>
    <button
        type="submit"
        class="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="disabled || loading"
    >
        <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
        <slot v-else />
    </button>
</template>

<style scoped>
.animate-spin {
    animation: spin 1s linear infinite;
}
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>