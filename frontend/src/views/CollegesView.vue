<script setup lang="ts">
import { ref, watch } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddCollegeModal from '../components/AddCollegeModal.vue'
import EditCollegeModal from '../components/EditCollegeModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'
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
// Fetch Programs (Mock)
// =========================
async function fetchColleges() {
    console.log(
        `Fetching colleges ${searchTerm.value} search by ${searchBy.value} sorted by ${sortBy.value} ${sortOrder.value} page ${currentPage.value} size ${pageSize.value}`
    )
    colleges.value = [
        {
            college_code: 'CCS',
            college_name: 'College of Computer Studies',
        },
        {
            college_code: 'COE',
            college_name: 'College of Engineering',
        },
    ]
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
    console.log('Submitting new college:', college)
    // 🔹 API POST call here
    showAddModal.value = false
    await fetchColleges()
}

async function handleCollegeEdit(college: College) {
    console.log('Updating college:', college)
    // 🔹 API PUT/PATCH call here
    showEditModal.value = false
    recordToEdit.value = null
    await fetchColleges()
}

async function handleCollegeDelete() {
    if (!recordToDelete.value) return
    console.log('Deleting college:', recordToDelete.value)
    // 🔹 API DELETE call here
    await fetchColleges()
    recordToDelete.value = null
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
