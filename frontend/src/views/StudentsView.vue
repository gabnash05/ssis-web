<script setup lang="ts">
import { ref, watch } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddStudentModal from '../components/AddStudentModal.vue'
import EditStudentModal from '../components/EditStudentModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'

import { createStudent, deleteStudent, listStudents, updateStudent } from '../api/students'

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
const totalPages = ref(1)
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
const addModalRef = ref<any>(null)
const editModalRef = ref<any>(null)

// =========================
// Fetch Students
// =========================
async function fetchStudents() {
    try {
        const res = await listStudents({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        });

        students.value = res.data;

        if (res.meta) {
            totalPages.value = Math.max(
                1,
                Math.ceil(res.meta.total / res.meta.per_page)
            );
        }
    } catch (err) {
        console.error("Failed to fetch students:", err);
    }
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
    try {
        await createStudent(student);
        showAddModal.value = false;
        await fetchStudents();
    } catch (err: any) {
        console.error("Error creating student:", err);
        // Pass the error to the modal for display
        if (addModalRef.value?.handleBackendErrors) {
            addModalRef.value.handleBackendErrors(err);
        }
    }
}

async function handleStudentEdit(student: Student) {
    if (!recordToEdit.value) return;
    try {
        await updateStudent(recordToEdit.value.id_number, student);
        showEditModal.value = false;
        recordToEdit.value = null;
        await fetchStudents();
    } catch (err: any) {
        console.error("Error updating student:", err);
        // Pass the error to the modal for display
        if (editModalRef.value?.handleBackendErrors) {
            editModalRef.value.handleBackendErrors(err);
        }
    }
}

async function handleStudentDelete() {
    if (!recordToDelete.value) return;
    try {
        await deleteStudent(recordToDelete.value.id_number);
        await fetchStudents();
        recordToDelete.value = null;
        showConfirmDialog.value = false;
    } catch (err) {
        console.error("Error deleting student:", err);
    }
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
            ref="addModalRef"
            v-model="showAddModal"
            @submit="handleStudentSubmit"
        />

        <!-- Edit Student Modal -->
        <EditStudentModal
            ref="editModalRef"
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
