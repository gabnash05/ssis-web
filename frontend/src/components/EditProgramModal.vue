<script setup lang="ts">
import { watch, ref } from 'vue'
import RecordFormModal from './RecordFormModal.vue'
import ConfirmDialog from './ConfirmDialog.vue'
import { useEditProgramForm } from '../composables/useEditProgramForm.ts'
import type { Program } from '../types.ts';

// =========================
// Props & Emits
// =========================
const props = defineProps<{
    modelValue: boolean
    program: Program | null
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit', program: any): void
}>()

// =========================
// Composable State
// =========================
const {
    editedProgram,
    errors,
    colleges,
    generalError,
    resetForm,
    fetchInitialData,
    loadProgram,
    handleSubmit,
    handleBackendErrors,
} = useEditProgramForm(emit)

// =========================
// Confirmation Dialog State and Methods
// =========================
const showConfirm = ref(false)
const isSubmitting = ref(false)

function handleValidatedSubmit() {
    const isValid = handleSubmit()
    if (!isValid) return

    showConfirm.value = true
}

async function confirmSubmit() {
    isSubmitting.value = true 
    
    try {
        emit('submit', { ...editedProgram.value })
    } catch (err) {
        console.error("Submission error:", err)
    } finally {
        isSubmitting.value = false
        showConfirm.value = false
    }
}

function cancelSubmit() {
    showConfirm.value = false
}

// =========================
// Watch for Modal Open
// =========================
watch(
    () => props.modelValue,
    async (isOpen) => {
        if (isOpen && props.program) {
            resetForm()
            await fetchInitialData()
            loadProgram(props.program)
        }
    }
)

watch(
    () => props.program,
    (program) => {
        if (props.modelValue && program) {
            loadProgram(program)
        }
    },
    { immediate: true }
)

// Expose the handleBackendErrors function for parent components
defineExpose({
    handleBackendErrors
})
</script>

<template>
    <RecordFormModal
        :model-value="modelValue"
        title="Edit Program"
        @update:modelValue="$emit('update:modelValue', $event)"
        @submit="handleValidatedSubmit"
        @cancel="resetForm"
    >
        <p class="text-sm text-white/60 mb-4">
            Edit the program's information below.
        </p>

        <!-- General Error Message -->
        <div v-if="generalError" class="p-2 rounded text-red-400 text-sm">
            {{ generalError }}
        </div>

        <div class="flex flex-col gap-4">
            <!-- Program Code -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Program Code
                    <span v-if="errors.program_code" class="text-red-400 ml-2">{{ errors.program_code }}</span>
                </label>
                <input
                    v-model="editedProgram.program_code"
                    placeholder="BSCS"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- Program Name -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Program Name
                    <span v-if="errors.program_name" class="text-red-400 ml-2">{{ errors.program_name }}</span>
                </label>
                <input
                    v-model="editedProgram.program_name"
                    placeholder="Bachelor of Science in Computer Science"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- College Dropdown -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    College
                    <span v-if="errors.college_code" class="text-red-400 ml-2">{{ errors.college_code }}</span>
                </label>
                <select
                    v-model="editedProgram.college_code"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                >
                    <option disabled value="" class="text-white/50">Select a college</option>
                    <option v-for="college in colleges" :key="college.code" :value="college.code">
                        {{ college.name }}
                    </option>
                </select>
            </div>
        </div>
    </RecordFormModal>

    <!-- Confirmation Dialog -->
    <ConfirmDialog
        v-model="showConfirm"
        title="Confirm Edit Program"
        :message="'Are you sure you want to edit this program?'"
        :confirmText="'Edit'"
        :cancelText="'Cancel'"
        :confirmVariant="'primary'"
        @confirm="confirmSubmit"
        @cancel="cancelSubmit"
    >
    </ConfirmDialog>
</template>
