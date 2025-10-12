<script setup lang="ts">
import { ref, watch, onActivated, computed } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddProgramModal from '../components/AddProgramModal.vue'
import EditProgramModal from '../components/EditProgramModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'

import { createProgram, updateProgram, deleteProgram } from '../api/programs'
import { useDataStore } from '../stores/dataStore'

import type { SortOrder, Program } from '../types'

// =========================
// Table Columns
// =========================
const programColumns = [
    { key: 'program_code', label: 'Program Code', sortable: true },
    { key: 'program_name', label: 'Program Name', sortable: true },
    { key: 'college_code', label: 'College Code', sortable: true },
]

// =========================
// Table + Pagination State
// =========================
const store = useDataStore()
const programs = computed(() => store.programs)
const sortBy = ref<string>(programColumns[0].key)
const sortOrder = ref<SortOrder>('ASC')
const searchTerm = ref('')
const searchBy = ref('')
const totalPages = ref(1)
const currentPage = ref(1)
const pageSize = ref(50)

// =========================
// Modal State
// =========================
const showAddModal = ref(false)
const showEditModal = ref(false)
const recordToEdit = ref<Program | null>(null)
const showConfirmDialog = ref(false)
const recordToDelete = ref<Program | null>(null)
const addModalRef = ref<any>(null)
const editModalRef = ref<any>(null)

// =========================
// Fetch Programs
// =========================
async function fetchPrograms() {
    try {
        await store.fetchPrograms({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        })
        if (store.meta.programs) {
            totalPages.value = Math.max(1, Math.ceil(store.meta.programs.total / store.meta.programs.per_page))
        }
    } catch (err) {
        console.error('Failed to fetch programs:', err)
    }
}

fetchPrograms()

watch([searchTerm, searchBy, sortBy, sortOrder], () => {
    currentPage.value = 1
    fetchPrograms()
})

watch([sortBy, sortOrder, searchTerm, searchBy, currentPage, pageSize], fetchPrograms)

onActivated(() => {
    fetchPrograms()
})
// =========================
// Actions
// =========================
function handleAdd() {
    showAddModal.value = true
}

function handleEdit(program: Program) {
    recordToEdit.value = program
    showEditModal.value = true
}

async function handleDelete(program: Program) {
    recordToDelete.value = program
    showConfirmDialog.value = true
}

async function handleProgramSubmit(program: Program) {
    try {
        await createProgram(program)
        store.invalidateAll()
        showAddModal.value = false
        await store.fetchPrograms({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        }, true)
    } catch (err: any) {
        console.error("Error creating program:", err)
        if (addModalRef.value?.handleBackendErrors) {
            addModalRef.value.handleBackendErrors(err)
        }
    }
}

async function handleProgramEdit(program: Program) {
    if (!recordToEdit.value) return
    try {
        await updateProgram(recordToEdit.value.program_code, program)
        store.invalidateAll()
        showEditModal.value = false
        recordToEdit.value = null
        await store.fetchPrograms({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        }, true)
    } catch (err: any) {
        console.error("Error updating program:", err)
        if (editModalRef.value?.handleBackendErrors) {
            editModalRef.value.handleBackendErrors(err)
        }
    }
}

async function handleProgramDelete() {
    if (!recordToDelete.value) return
    try {
        await deleteProgram(recordToDelete.value.program_code)
        store.invalidateAll()
        await store.fetchPrograms({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        }, true)
        recordToDelete.value = null
        showConfirmDialog.value = false
    } catch (err) {
        console.error("Error deleting program:", err)
    }
}
</script>

<template>
    <div>
        <!-- Header Section -->
        <div class="flex items-center justify-between mb-4">
            <!-- Title + Add Button -->
            <div class="flex items-center gap-5">
                <h1 class="text-2xl font-bold text-white">Programs</h1>
                <button
                    @click="handleAdd"
                    class="px-4 py-2 bg-glass border border-white/20 rounded-xl text-white hover:bg-white/20 cursor-pointer transition flex items-center gap-2"
                >
                    <img
                        src="../assets/icons/circle-plus.svg"
                        alt="Add"
                        class="w-4 h-4 filter invert"
                    />
                    <span class="text-sm font-medium">Add Program</span>
                </button>
            </div>

            <SearchBar
                v-model="searchTerm"
                v-model:searchBy="searchBy"
                :searchByOptions="programColumns"
            />
        </div>

        <!-- Table -->
        <DataTable
            :columns="programColumns"
            :rows="programs"
            :sortBy="sortBy"
            :sortOrder="sortOrder"
            :loading="store.loading.programs"
            @update:sortBy="sortBy = $event"
            @update:sortOrder="sortOrder = $event"
            @edit="handleEdit"
            @delete="handleDelete"
        />

        <!-- Pagination -->
        <PaginationControls
            :total-pages="totalPages"
            :current-page="currentPage"
            :page-size="pageSize"
            @update:page="currentPage = $event"
            @update:pageSize="pageSize = $event"
        />

        <!-- Add Program Modal -->
        <AddProgramModal
            ref="addModalRef"
            v-model="showAddModal"
            @submit="handleProgramSubmit"
        />

        <!-- Edit Program Modal -->
        <EditProgramModal
            ref="editModalRef"
            v-model="showEditModal"
            :program="recordToEdit"
            @submit="handleProgramEdit"
        />

        <!-- Confirm Delete Dialog -->
        <ConfirmationDialog
            v-model="showConfirmDialog"
            title="Delete Program"
            :message="`Are you sure you want to delete ${recordToDelete?.program_code} - ${recordToDelete?.program_name}?`"
            confirm-text="Delete"
            confirm-variant="danger"
            @confirm="handleProgramDelete"
        />
    </div>
</template>
