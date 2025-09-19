<script setup lang="ts">
defineProps<{
    title: string
    footerText?: string
    footerLink?: string
    footerLinkText?: string
}>()
</script>

<template>
    <div class="w-full max-w-md p-10 rounded-xl bg-glass border border-white/10 shadow-xl">
        <h1 class="text-2xl font-semibold text-white text-center mb-6">
            {{ title }}
        </h1>
        <slot />
        <p v-if="footerText" class="mt-6 text-sm text-center text-gray-300">
            {{ footerText }}
            <router-link
                v-if="footerLink"
                :to="footerLink"
                class="text-blue-400 hover:underline"
            >
                {{ footerLinkText }}
            </router-link>
        </p>
    </div>
</template>
