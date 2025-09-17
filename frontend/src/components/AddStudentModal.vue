<script setup lang="ts">
import { watch } from 'vue'
import RecordFormModal from './RecordFormModal.vue'
import { useAddStudentForm } from '../composables/useAddStudentForm'

// Props & Emits
const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit', student: any): void
}>()

const {
    newStudent,
    errors,
    college_code,
    colleges,
    programs,
    filteredPrograms,
    handleSubmit,
    handleIdInput,
    resetForm,
    fetchInitialData,
} = useAddStudentForm(emit)

// Reset form & fetch data when modal opens
watch(
    () => props.modelValue,
    async (isOpen) => {
        if (isOpen) {
            resetForm()
            await fetchInitialData()
        }
    }
)
</script>

<template>
    <RecordFormModal
        :model-value="modelValue"
        title="Add New Student"
        @update:modelValue="$emit('update:modelValue', $event)"
        @submit="handleSubmit"
        @cancel="resetForm"
    >
        <p class="text-sm text-white/60 mb-4">
            Fill out the student's information below.
        </p>

        <div class="flex flex-col gap-4">
            <!-- ID Number -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    ID Number
                    <span v-if="errors.id_number" class="text-red-400 ml-2">
                        {{ errors.id_number }}
                    </span>
                </label>
                <input
                    :value="newStudent.id_number"
                    @input="handleIdInput"
                    placeholder="YYYY-NNNN"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- First Name -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    First Name
                    <span v-if="errors.first_name" class="text-red-400 ml-2">{{ errors.first_name }}</span>
                </label>
                <input
                    v-model="newStudent.first_name"
                    placeholder="John"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- Last Name -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Last Name
                    <span v-if="errors.last_name" class="text-red-400 ml-2">{{ errors.last_name }}</span>
                </label>
                <input
                    v-model="newStudent.last_name"
                    placeholder="Doe"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- Year Level -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Year Level
                    <span v-if="errors.year_level" class="text-red-400 ml-2">{{ errors.year_level }}</span>
                </label>
                <select
                    v-model="newStudent.year_level"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                >
                    <option :value="1">1st Year</option>
                    <option :value="2">2nd Year</option>
                    <option :value="3">3rd Year</option>
                    <option :value="4">4th Year</option>
                </select>
            </div>

            <!-- Gender -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Gender
                    <span v-if="errors.gender" class="text-red-400 ml-2">{{ errors.gender }}</span>
                </label>
                <select
                    v-model="newStudent.gender"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                >
                    <option value="FEMALE">Female</option>
                    <option value="MALE">Male</option>
                    <option value="OTHER">Other</option>
                </select>
            </div>

            <!-- College Dropdown -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    College
                    <span v-if="errors.college_code" class="text-red-400 ml-2">{{ errors.college_code }}</span>
                </label>
                <select
                    v-model="college_code"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                >
                    <option disabled value="">Select a college</option>
                    <option v-for="college in colleges" :key="college.code" :value="college.code">
                        {{ college.name }}
                    </option>
                </select>
            </div>

            <!-- Program Dropdown -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Program
                    <span v-if="errors.program_code" class="text-red-400 ml-2">{{ errors.program_code }}</span>
                </label>
                <select
                    v-model="newStudent.program_code"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400 disabled:opacity-50"
                    :disabled="filteredPrograms.length === 0"
                >
                    <option disabled value="">Select a program</option>
                    <option
                        v-for="program in filteredPrograms"
                        :key="program.code"
                        :value="program.code"
                    >
                        {{ program.name }}
                    </option>
                </select>
            </div>
        </div>
    </RecordFormModal>
</template>
