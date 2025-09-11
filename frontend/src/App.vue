<script setup lang="ts">
import { ref } from 'vue';
import AppLayout from './components/AppLayout.vue';
import type { ApplicationPage } from './types';

const currentPage = ref<ApplicationPage>('STUDENTS');

function goToPage(page: ApplicationPage) {
    currentPage.value = page;
}
</script>

<template>
    <AppLayout
         :currentPage="currentPage"
        @change-page="goToPage"
    >
        <div class="p-6 w-full h-full overflow-auto">
        </div>
    </AppLayout>
</template>
