<script setup lang="ts">
defineProps<{ disabled?: boolean }>()
</script>

<template>
    <button
        type="submit"
        class="w-full px-4 py-2 cursor-pointer rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-50"
        :disabled="disabled"
    >
        <slot />
    </button>
</template>