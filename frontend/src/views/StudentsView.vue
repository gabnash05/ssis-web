<script setup lang="ts">
import { ref, watch } from 'vue'
import DataTable from '../components/DataTable.vue'
import type { SortOrder, Student } from '../types'

const students = ref<Student[]>([])
const sortBy = ref<string>('id_number')
const sortOrder = ref<SortOrder>('ASC')

function fetchStudents() {
    // Here you'd call your API with sortBy + sortOrder
    // Example: /api/students?sortBy=id_number&order=asc
    students.value = [
        { id_number: '2025-0001', first_name: 'Alice', last_name: 'Reyes', year_level: 1, gender: 'FEMALE', program_code: 'BSCS' },
        { id_number: '2025-0002', first_name: 'Ben', last_name: 'Lopez', year_level: 1, gender: 'MALE', program_code: 'BSIT' }
    ]
}
fetchStudents()

watch([sortBy, sortOrder], fetchStudents)

// Actions
function handleEdit(student: Student) {
    console.log('Open Edit Dialog for', student)
    // Open modal or dialog component here
    // After dialog closes, call fetchStudents() to refresh
}

function handleDelete(student: Student) {
    console.log('Confirm delete for', student)
    // Show confirmation dialog, then call API
    // After delete success, call fetchStudents()
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
        <h1 class="text-2xl font-bold mb-4 text-white">Students</h1>
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
    </div>
</template>
