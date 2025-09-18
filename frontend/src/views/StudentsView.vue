<script setup lang="ts">
import { ref, watch } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddStudentModal from '../components/AddStudentModal.vue'
import EditStudentModal from '../components/EditStudentModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'
import type { SortOrder, Student } from '../types'

// =========================
// Table Columns
// =========================
const studentColumns = [
    { key: 'id_number', label: 'ID Number', sortable: true },
    { key: 'first_name', label: 'First Name', sortable: true },
    { key: 'last_name', label: 'Last Name', sortable: true },
    { key: 'year_level', label: 'Year Level', sortable: true },
    { key: 'gender', label: 'Gender', sortable: true },
    { key: 'program_code', label: 'Program Code', sortable: true },
]

// =========================
// Table + Pagination State
// =========================
const students = ref<Student[]>([])
const sortBy = ref<string>(studentColumns[0].key)
const sortOrder = ref<SortOrder>('ASC')
const searchTerm = ref('')
const searchBy = ref(studentColumns[0].key)
const totalPages = ref(10)
const currentPage = ref(1)
const pageSize = ref(50)

// =========================
// Modal State
// =========================
const showAddModal = ref(false)
const showEditModal = ref(false)
const recordToEdit = ref<Student | null>(null)
const showConfirmDialog = ref(false)
const recordToDelete = ref<Student | null>(null)

// =========================
// Fetch Students (Mock)
// =========================
async function fetchStudents() {
    console.log(
        `Fetching students ${searchTerm.value} search by ${searchBy.value} sorted by ${sortBy.value} ${sortOrder.value} page ${currentPage.value} size ${pageSize.value}`
    )
    students.value = [
        {
            id_number: '2025-0001',
            first_name: 'Alice',
            last_name: 'Reyes',
            year_level: 1,
            gender: 'FEMALE',
            program_code: 'BSCS',
        },
        {
            id_number: '2025-0002',
            first_name: 'John',
            last_name: 'Doe',
            year_level: 1,
            gender: 'MALE',
            program_code: 'BSIT',
        },
    ]
}

fetchStudents()
watch([sortBy, sortOrder, searchTerm, searchBy, currentPage, pageSize], fetchStudents)

// =========================
// Actions
// =========================
function handleAdd() {
    showAddModal.value = true
}

function handleEdit(student: Student) {
    recordToEdit.value = student
    showEditModal.value = true
}

async function handleDelete(student: Student) {
    recordToDelete.value = student
    showConfirmDialog.value = true
}

async function handleStudentSubmit(student: Student) {
    console.log('Submitting new student:', student)
    // 🔹 API POST call here
    showAddModal.value = false
    await fetchStudents()
}

async function handleStudentEdit(student: Student) {
    console.log('Updating student:', student)
    // 🔹 API PUT/PATCH call here
    showEditModal.value = false
    recordToEdit.value = null
    await fetchStudents()
}

async function handleStudentDelete() {
    if (!recordToDelete.value) return
    console.log('Deleting student:', recordToDelete.value)
    // 🔹 API DELETE call here
    await fetchStudents()
    recordToDelete.value = null
}
</script>

<template>
    <div>
        <!-- Header Section -->
        <div class="flex items-center justify-between mb-4">
            <!-- Title + Add Button -->
            <div class="flex items-center gap-5">
                <h1 class="text-2xl font-bold text-white">Students</h1>
                <button
                    @click="handleAdd"
                    class="px-4 py-2 bg-glass border border-white/20 rounded-xl text-white hover:bg-white/20 cursor-pointer transition flex items-center gap-2"
                >
                    <img
                        src="../assets/icons/circle-plus.svg"
                        alt="Add"
                        class="w-4 h-4 filter invert"
                    />
                    <span class="text-sm font-medium">Add Student</span>
                </button>
            </div>

            <SearchBar
                v-model="searchTerm"
                v-model:searchBy="searchBy"
                :searchByOptions="studentColumns"
            />
        </div>

        <!-- Table -->
        <DataTable
            :columns="studentColumns"
            :rows="students"
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
        <AddStudentModal
            v-model="showAddModal"
            @submit="handleStudentSubmit"
        />

        <!-- Edit Student Modal -->
        <EditStudentModal
            v-model="showEditModal"
            :student="recordToEdit"
            @submit="handleStudentEdit"
        />

        <!-- Confirm Delete Dialog -->
        <ConfirmationDialog
            v-model="showConfirmDialog"
            title="Delete Student"
            :message="`Are you sure you want to delete ${recordToDelete?.first_name} ${recordToDelete?.last_name}?`"
            confirm-text="Delete"
            confirm-variant="danger"
            @confirm="handleStudentDelete"
        />
    </div>
</template>
