<script setup lang="ts">
import { computed, ref } from 'vue';
import AppLayout from './components/AppLayout.vue';
import StudentsView from './views/StudentsView.vue';
import ProgramsView from './views/ProgramsView.vue';
import CollegesView from './views/CollegesView.vue';
import type { ApplicationPage } from './types';

// =========================
// Page Controls
// =========================
const currentPage = ref<ApplicationPage>('STUDENTS');

function goToPage(page: ApplicationPage) {
    currentPage.value = page;
}

const currentView = computed(() => {
    switch (currentPage.value) {
        case "STUDENTS": return StudentsView
        case "PROGRAMS": return ProgramsView
        case "COLLEGES": return CollegesView
        default: return StudentsView
    }
})
</script>

<template>
    <AppLayout
        :currentPage="currentPage"
        @change-page="goToPage"
    >
        <div class="p-6 w-full h-full overflow-auto">
            <transition name="fade-slide" mode="out-in">
                <component :is="currentView" />
            </transition>
        </div>
    </AppLayout>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: opacity 0.15s ease, transform 0.15s ease;
}

.fade-slide-enter-from {
    opacity: 0;
    transform: translateY(5px);
}

.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-5px);
}
</style>
