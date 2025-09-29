<script setup lang="ts">
import { ref, watch } from 'vue'

import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddCollegeModal from '../components/AddCollegeModal.vue'
import EditCollegeModal from '../components/EditCollegeModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'

import { listColleges, createCollege, updateCollege, deleteCollege } from '../api/colleges'

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
const colleges = ref<College[]>([])
const sortBy = ref<string>(collegeColumns[0].key)
const sortOrder = ref<SortOrder>('ASC')
const searchTerm = ref('')
const searchBy = ref(collegeColumns[0].key)
const totalPages = ref(10)
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

// =========================
// Fetch Programs
// =========================
async function fetchColleges() {
    try {
        const res = await listColleges({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        })

        colleges.value = res.data
    } catch (err) {
        console.error("Failed to fetch colleges:", err)
    }
}

fetchColleges()
watch([sortBy, sortOrder, searchTerm, searchBy, currentPage, pageSize], fetchColleges)

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
        showAddModal.value = false
        await fetchColleges()
    } catch (err) {
        console.error("Error creating college:", err)
    }
}

async function handleCollegeEdit(college: College) {
    if (!recordToEdit.value) return
    try {
        await updateCollege(recordToEdit.value.college_code, college)
        showEditModal.value = false
        recordToEdit.value = null
        await fetchColleges()
    } catch (err) {
        console.error("Error updating college:", err)
    }
}

async function handleCollegeDelete() {
    if (!recordToDelete.value) return
    try {
        await deleteCollege(recordToDelete.value.college_code)
        await fetchColleges()
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

        <!-- Add Student Modal -->
        <AddCollegeModal
            v-model="showAddModal"
            @submit="handleCollegeSubmit"
        />

        <!-- Edit Student Modal -->
        <EditCollegeModal
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
