<script setup lang="ts">
import { computed, ref, watch } from 'vue'

const props = defineProps<{
    totalPages: number
    currentPage: number
    pageSize: number
    pageSizeOptions?: number[]
}>()

const emit = defineEmits<{
    (e: 'update:page', page: number): void
    (e: 'update:pageSize', size: number): void
}>()

function changePage(newPage: number) {
    if (newPage < 1 || newPage > props.totalPages) return
    emit('update:page', newPage)
}

const pagesToShow = computed(() => {
    const pages: number[] = []
    const start = Math.max(1, props.currentPage - 2)
    const end = Math.min(props.totalPages, props.currentPage + 2)

    for (let i = start; i <= end; i++) {
        pages.push(i)
    }
    return pages
})

// Go to page input state
const gotoPage = ref(props.currentPage)
watch(() => props.currentPage, (newVal) => gotoPage.value = newVal)

function submitGotoPage() {
    const pageNumber = Number(gotoPage.value)
    if (!Number.isNaN(pageNumber)) changePage(pageNumber)
}
</script>

<template>
    <div class="flex flex-col sm:flex-row items-center justify-between gap-4 mt-4 text-white">
        <!-- Show X per page -->
        <div class="flex items-center gap-2">
            <label for="page-size" class="text-sm opacity-80">Show</label>
            <select
                id="page-size"
                :value="pageSize"
                @change="emit('update:pageSize', parseInt(($event.target as HTMLSelectElement).value))"
                class="bg-glass text-white px-3 py-1 rounded-md border border-white/20 text-sm focus:outline-none"
            >
                <option
                    v-for="size in (pageSizeOptions || [5, 10, 20, 50])"
                    :key="size"
                    :value="size"
                    class="bg-neutral-900/50 text-white"
                >
                    {{ size }}
                </option>
            </select>
            <span class="text-sm opacity-80">per page</span>
        </div>

        <!-- Pagination Controls -->
        <div class="flex flex-wrap items-center gap-1">
            <!-- Prev Button -->
            <button
                @click="changePage(props.currentPage - 1)"
                :disabled="props.currentPage === 1"
                class="cursor-pointer hover:scale-110 px-3 py-1 rounded text-sm bg-glass border border-white/10 hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed transition duration-200"
            >
                Prev
            </button>

            <!-- Nearby Pages -->
            <template v-for="page in pagesToShow" :key="page">
                <button
                    @click="changePage(page)"
                    class="px-3 py-1 text-sm rounded border transition duration-100 cursor-pointer hover:scale-110"
                    :class="[
                        page === props.currentPage
                            ? 'bg-blue-500/20 text-white border-white/40'
                            : 'bg-glass border-white/10 hover:bg-white/10'
                    ]"
                >
                    {{ page }}
                </button>
            </template>

            <!-- Next Button -->
            <button
                @click="changePage(props.currentPage + 1)"
                :disabled="props.currentPage === props.totalPages"
                class="cursor-pointer hover:scale-110 px-3 py-1 text-sm rounded bg-glass border border-white/10 hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed transition duration-200"
            >
                Next
            </button>

            <!-- Go to page input -->
            <div class="flex items-center gap-2 ml-2">
                <span class="text-sm opacity-80">Go to</span>
                <input
                    type="number"
                    v-model="gotoPage"
                    @keydown.enter="submitGotoPage"
                    @blur="submitGotoPage"
                    class="w-14 text-center bg-white/20 border border-white/10 rounded text-sm text-white outline-none focus:ring-1 focus:ring-white/50 transition-colors duration-200"
                    :min="1"
                    :max="props.totalPages"
                />
            </div>
        </div>
    </div>
</template>

