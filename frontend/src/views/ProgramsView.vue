<script setup lang="ts">
import { ref, watch } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddProgramModal from '../components/AddProgramModal.vue'
import EditProgramModal from '../components/EditProgramModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'
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
const programs = ref<Program[]>([])
const sortBy = ref<string>(programColumns[0].key)
const sortOrder = ref<SortOrder>('ASC')
const searchTerm = ref('')
const searchBy = ref(programColumns[0].key)
const totalPages = ref(10)
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

// =========================
// Fetch Programs (Mock)
// =========================
async function fetchPrograms() {
    console.log(
        `Fetching programs ${searchTerm.value} search by ${searchBy.value} sorted by ${sortBy.value} ${sortOrder.value} page ${currentPage.value} size ${pageSize.value}`
    )
    programs.value = [
        {
            program_code: 'BSCS',
            program_name: 'Bachelor of Science in Computer Science',
            college_code: 'CCS',
        },
        {
            program_code: 'BSCE',
            program_name: 'Bachelor of Science in Civil Engineering',
            college_code: 'COE',
        },
    ]
}

fetchPrograms()
watch([sortBy, sortOrder, searchTerm, searchBy, currentPage, pageSize], fetchPrograms)

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
    console.log('Submitting new program:', program)
    // 🔹 API POST call here
    showAddModal.value = false
    await fetchPrograms()
}

async function handleProgramEdit(program: Program) {
    console.log('Updating program:', program)
    // 🔹 API PUT/PATCH call here
    showEditModal.value = false
    recordToEdit.value = null
    await fetchPrograms()
}

async function handleProgramDelete() {
    if (!recordToDelete.value) return
    console.log('Deleting program:', recordToDelete.value)
    // 🔹 API DELETE call here
    await fetchPrograms()
    recordToDelete.value = null
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
        <AddProgramModal
            v-model="showAddModal"
            @submit="handleProgramSubmit"
        />

        <!-- Edit Student Modal -->
        <EditProgramModal
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
