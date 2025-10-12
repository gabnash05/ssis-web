<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
</script>

<template>
    <div class="absolute inset-0 z-20">
        <div class="bg-black/50 backdrop-blur-sm flex flex-col items-center justify-center text-white rounded-xl h-full w-full">
            <Loader2 class="w-8 h-8 animate-spin mb-2" />
            <p class="text-sm">Loading...</p>
        </div>
    </div>
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
