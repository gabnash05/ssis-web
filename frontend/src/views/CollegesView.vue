<script setup lang="ts">
defineOptions({ name: 'CollegesView' })
import { ref, watch, onActivated, computed } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddCollegeModal from '../components/AddCollegeModal.vue'
import EditCollegeModal from '../components/EditCollegeModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'

import { createCollege, updateCollege, deleteCollege } from '../api/colleges'
import { useDataStore } from '../stores/dataStore'

import type { SortOrder, College } from '../types'

// =========================
// Table Columns
// =========================
const collegeColumns = [
    { key: 'college_code', label: 'College Code', sortable: true },
    { key: 'college_name', label: 'College Name', sortable: true},
]

// =========================
// Table + Pagination State
// =========================
const store = useDataStore()
const colleges = computed(() => store.colleges)
const sortBy = ref<string>(collegeColumns[0].key)
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
const recordToEdit = ref<College | null>(null)
const showConfirmDialog = ref(false)
const recordToDelete = ref<College | null>(null)
const addModalRef = ref<any>(null)
const editModalRef = ref<any>(null)

// =========================
// Fetch Programs
// =========================
async function fetchColleges() {
    try {
        await store.fetchColleges({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        })
        if (store.meta.colleges) {
            totalPages.value = Math.max(1, Math.ceil(store.meta.colleges.total / store.meta.colleges.per_page))
        }
    } catch (err) {
        console.error("Failed to fetch colleges:", err)
    }
}

fetchColleges()

watch([searchTerm, searchBy, sortBy, sortOrder], () => {
    currentPage.value = 1
    fetchColleges()
})

watch([sortBy, sortOrder, searchTerm, searchBy, currentPage, pageSize], fetchColleges)

onActivated(() => {
    fetchColleges()
})
// =========================
// Actions
// =========================
function handleAdd() {
    showAddModal.value = true
}

function handleEdit(college: College) {
    recordToEdit.value = college
    showEditModal.value = true
}

async function handleDelete(college: College) {
    recordToDelete.value = college
    showConfirmDialog.value = true
}

async function handleCollegeSubmit(college: College) {
    try {
        await createCollege(college)
        store.invalidateAll()
        showAddModal.value = false
        await store.fetchColleges({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        }, true)
    } catch (err: any) {
        console.error("Error creating college:", err)
        if (addModalRef.value?.handleBackendErrors) {
            addModalRef.value.handleBackendErrors(err)
        }
    }
}

async function handleCollegeEdit(college: College) {
    if (!recordToEdit.value) return
    try {
        await updateCollege(recordToEdit.value.college_code, college)
        store.invalidateAll()
        showEditModal.value = false
        recordToEdit.value = null
        await store.fetchColleges({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        }, true)
    } catch (err: any) {
        console.error("Error updating college:", err)
        // Pass the error to the modal for display
        if (editModalRef.value?.handleBackendErrors) {
            editModalRef.value.handleBackendErrors(err)
        }
    }
}

async function handleCollegeDelete() {
    if (!recordToDelete.value) return
    try {
        await deleteCollege(recordToDelete.value.college_code)
        store.invalidateAll()
        await store.fetchColleges({
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
        console.error("Error deleting college:", err)
    }
}
</script>

<template>
    <div>
        <!-- Header Section -->
        <div class="flex items-center justify-between mb-4">
            <!-- Title + Add Button -->
            <div class="flex items-center gap-5">
                <h1 class="text-2xl font-bold text-white">Colleges</h1>
                <button
                    @click="handleAdd"
                    class="px-4 py-2 bg-glass border border-white/20 rounded-xl text-white hover:bg-white/20 cursor-pointer transition flex items-center gap-2"
                >
                    <img
                        src="../assets/icons/circle-plus.svg"
                        alt="Add"
                        class="w-4 h-4 filter invert"
                    />
                    <span class="text-sm font-medium">Add College</span>
                </button>
            </div>

            <SearchBar
                v-model="searchTerm"
                v-model:searchBy="searchBy"
                :searchByOptions="collegeColumns"
            />
        </div>

        <!-- Table -->
        <DataTable
            :columns="collegeColumns"
            :rows="colleges"
            :sortBy="sortBy"
            :sortOrder="sortOrder"
            :loading="store.loading.colleges"
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

        <!-- Add College Modal -->
        <AddCollegeModal
            ref="addModalRef"
            v-model="showAddModal"
            @submit="handleCollegeSubmit"
        />

        <!-- Edit College Modal -->
        <EditCollegeModal
            ref="editModalRef"
            v-model="showEditModal"
            :college="recordToEdit"
            @submit="handleCollegeEdit"
        />

        <!-- Confirm Delete Dialog -->
        <ConfirmationDialog
            v-model="showConfirmDialog"
            title="Delete College"
            :message="`Are you sure you want to delete ${recordToDelete?.college_code} - ${recordToDelete?.college_name}?`"
            confirm-text="Delete"
            confirm-variant="danger"
            @confirm="handleCollegeDelete"
        />
    </div>
</template>
