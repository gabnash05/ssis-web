<script setup lang="ts">
defineProps<{ currentPage: string }>()
defineEmits<{ (e: 'changePage', page: string): void }>()
</script>

<template>
    <!-- Background (same as AppLayout) -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
        <div class="absolute w-[500px] h-[500px] bg-[#2e64b0]/40 rounded-full blur-[100px] top-1/4 left-1/4"></div>
        <div class="absolute w-[600px] h-[600px] bg-[#d425c9]/20 rounded-full blur-[120px] top-2/3 right-1/4"></div>
        <div class="absolute w-[450px] h-[450px] bg-[#2cdfdf]/20 rounded-full blur-[90px] bottom-1/4 left-1/2"></div>
    </div>

    <div class="min-h-screen py-7 px-15 flex justify-center items-center">
        <slot />
    </div>
</template>