<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import AppLayout from './layouts/AppLayout.vue'
import AuthLayout from './layouts/AuthLayout.vue'

const route = useRoute()

const layout = computed(() => {
    return route.meta.layout === 'auth' ? AuthLayout : AppLayout
})

</script>

<template>
    <component 
        :is="layout"
        :current-page="typeof route?.name === 'string' ? route.name : (route?.name?.toString?.() ?? 'LOGIN')"
        @change-page="(page: string) => $router.push({ name: page })"
    >
        <router-view v-slot="{ Component }">
            <transition name="fade-slide" mode="out-in">
                <keep-alive include="StudentsView,ProgramsView,CollegesView,UsersView">
                    <component :is="Component" />
                </keep-alive>
            </transition>
        </router-view>
    </component>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.3s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(10px);
}
.fade-slide-enter-to,
.fade-slide-leave-from {
    opacity: 1;
    transform: translateY(0);
}
</style>