<script setup lang="ts">
import { ref, watch, onActivated, computed } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddStudentModal from '../components/AddStudentModal.vue'
import EditStudentModal from '../components/EditStudentModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'

import { createStudent, deleteStudent, updateStudent } from '../api/students'
import { useDataStore } from '../stores/dataStore'

import type { SortOrder, Student } from '../types'


// =========================
// Table Columns
// =========================
const studentColumns = [
    { key: 'photo_url', label: 'Photo', sortable: false },
    { key: 'id_number', label: 'ID Number', sortable: true },
    { key: 'first_name', label: 'First Name', sortable: true },
    { key: 'last_name', label: 'Last Name', sortable: true },
    { key: 'year_level', label: 'Year Level', sortable: true },
    { key: 'gender', label: 'Gender', sortable: true },
    { key: 'program_code', label: 'Program Code', sortable: true },
];

// =========================
// Table + Pagination State
// =========================
const store = useDataStore()
const students = computed(() => store.students)
const sortBy = ref<string>(studentColumns[0].key);
const sortOrder = ref<SortOrder>('ASC');
const searchTerm = ref('');
const searchBy = ref('');
const totalPages = ref(1);
const currentPage = ref(1);
const pageSize = ref(50);

// =========================
// Modal State
// =========================
const showAddModal = ref(false);
const showEditModal = ref(false);
const recordToEdit = ref<Student | null>(null);
const showConfirmDialog = ref(false);
const recordToDelete = ref<Student | null>(null);
const addModalRef = ref<any>(null);
const editModalRef = ref<any>(null);
const isAddingStudent = ref(false);
const isEditingStudent = ref(false);

// =========================
// Fetch Students
// =========================
async function fetchStudents() {
    try {
        await store.fetchStudents({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        })
        if (store.meta.students) {
            totalPages.value = Math.max(1, Math.ceil(store.meta.students.total / store.meta.students.per_page))
        }
    } catch (err) {
        console.error("Failed to fetch students:", err);
    }
}

fetchStudents()

watch([searchTerm, searchBy, sortBy, sortOrder], () => {
    currentPage.value = 1
    fetchStudents()
})

watch([sortBy, sortOrder, searchTerm, searchBy, currentPage, pageSize], fetchStudents)

onActivated(() => {
    fetchStudents()
})

// =========================
// Actions
// =========================
function handleAdd() {
    showAddModal.value = true;
}

function handleEdit(student: Student) {
    recordToEdit.value = student;
    showEditModal.value = true;
}

async function handleDelete(student: Student) {
    recordToDelete.value = student;
    showConfirmDialog.value = true;
}

async function handleStudentSubmit(student: Student) {
    isAddingStudent.value = true; // Start loading
    
    try {
        const { data: createdStudent } = await createStudent(student);

        if (addModalRef.value?.avatarFile) {
            try {
                const uploadInfo = await addModalRef.value.requestAvatarUpload(
                    createdStudent.data.id_number,
                    addModalRef.value.avatarFile
                );

                await addModalRef.value.uploadToSupabase(uploadInfo.upload_url, addModalRef.value.avatarFile);
                await addModalRef.value.finalizeAvatar(createdStudent.data.id_number, uploadInfo.avatar_path);
                
                addModalRef.value.clearWarnings?.();
                
            } catch (avatarError) {
                console.error("Avatar upload failed but student was created:", avatarError);
                if (addModalRef.value?.showAvatarWarning) {
                    addModalRef.value.showAvatarWarning(
                        'Student was created successfully, but avatar upload failed. You can update the avatar later.'
                    );
                }
            }
        }

        store.invalidateAll();
        showAddModal.value = false;

        await store.fetchStudents({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        }, true);

    } catch (err: any) {
        console.error("Error creating student:", err);
        if (addModalRef.value?.handleBackendErrors) {
            addModalRef.value.handleBackendErrors(err);
        }
    } finally {
        isAddingStudent.value = false; // End loading
    }
}

async function handleStudentEdit(student: Student) {
    if (!recordToEdit.value) return;
    isEditingStudent.value = true; // Start loading
    
    try {
        await updateStudent(recordToEdit.value.id_number, student);
        
        if (editModalRef.value?.avatarFile) {
            try {
                const uploadInfo = await editModalRef.value.requestAvatarUpload(
                    recordToEdit.value.id_number,
                    editModalRef.value.avatarFile
                );

                await editModalRef.value.uploadToSupabase(uploadInfo.upload_url, editModalRef.value.avatarFile);
                await editModalRef.value.finalizeAvatar(recordToEdit.value.id_number, uploadInfo.avatar_path);
                
                editModalRef.value.clearWarnings?.();
                
            } catch (avatarError) {
                console.error("Avatar upload failed but student was updated:", avatarError);
                if (editModalRef.value?.showAvatarWarning) {
                    editModalRef.value.showAvatarWarning(
                        'Student information was updated successfully, but avatar upload failed. You can try updating the avatar again later.'
                    );
                }
            }
        }

        store.invalidateAll()
        showEditModal.value = false;
        recordToEdit.value = null;
        
        await store.fetchStudents({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        }, true)
    } catch (err: any) {
        console.error("Error updating student:", err);
        if (editModalRef.value?.handleBackendErrors) {
            editModalRef.value.handleBackendErrors(err);
        }
    } finally {
        isEditingStudent.value = false; // End loading
    }
}

async function handleStudentDelete() {
    if (!recordToDelete.value) return;
    try {
        await deleteStudent(recordToDelete.value.id_number);
        store.invalidateAll();
        await store.fetchStudents({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        }, true)
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
            :loading="store.loading.students"
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
            :loading="isAddingStudent"
            @submit="handleStudentSubmit"
        />

        <!-- Edit Student Modal -->
        <EditStudentModal
            ref="editModalRef"
            v-model="showEditModal"
            :student="recordToEdit"
            :loading="isEditingStudent"
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
