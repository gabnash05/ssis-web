<script setup lang="ts">
import { computed, ref } from 'vue';
import AppLayout from './components/AppLayout.vue';
import StudentsView from './views/StudentsView.vue';
import type { ApplicationPage } from './types';

const currentPage = ref<ApplicationPage>('STUDENTS');

function goToPage(page: ApplicationPage) {
    currentPage.value = page;
}

const currentView = computed(() => {
    switch (currentPage.value) {
        case "STUDENTS": return StudentsView
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
            <component :is="currentView" />
        </div>
    </AppLayout>
</template>
