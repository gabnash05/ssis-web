<script setup lang="ts">
import { ref, watch } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import type { SortOrder, Student } from '../types'

const students = ref<Student[]>([])
const sortBy = ref<string>('id_number')
const sortOrder = ref<SortOrder>('ASC')
const searchTerm = ref('')
const totalPages = ref(10)
const currentPage = ref(1)
const pageSize = ref(50)

async function fetchStudents() {
    // 🔹 Normally call your backend API here with query params
    // Example: /api/students?search=...&sortBy=...&sortOrder=...
    // For now, we simulate:
    console.log(`Fetching students ${searchTerm.value} sorted by ${sortBy.value} ${sortOrder.value} page ${currentPage.value} size ${pageSize.value}`)
    students.value = [
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' },
        
    ]
}

// Fetch on load
fetchStudents()

watch([sortBy, sortOrder, searchTerm, currentPage, pageSize], fetchStudents)

// Actions
async function handleEdit(student: Student) {
    console.log('Open Edit Dialog for', student)
    // 🔹 Open modal or navigate to edit form
    // After saving changes (API PUT/PATCH), refresh table:
    console.log(`Saving changes for ${student.id_number}...`)
    await fetchStudents()
}

async function handleDelete(student: Student) {
    console.log('Confirm delete for', student)
    // 🔹 Call API DELETE /students/:id
    // After deletion succeeds:
    console.log(`Deleting ${student.id_number}...`)
    await fetchStudents()
}

const studentColumns = [
    { key: 'id_number', label: 'ID Number', sortable: true },
    { key: 'first_name', label: 'First Name', sortable: true },
    { key: 'last_name', label: 'Last Name', sortable: true },
    { key: 'year_level', label: 'Year Level', sortable: true},
    { key: 'gender', label: 'Gender', sortable: true},
    { key: 'program_code', label: 'Program Code', sortable: true },
]
</script>

<template>
    <div>
        <div class="flex items-center justify-between mb-4">
            <h1 class="text-2xl font-bold text-white">Students</h1>
            <SearchBar v-model="searchTerm" />
        </div>

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

        <PaginationControls
            :total-pages="totalPages"
            :current-page="currentPage"
            :page-size="pageSize"
            @update:page="currentPage = $event"
            @update:pageSize="pageSize = $event"
        />
    </div>
</template>
