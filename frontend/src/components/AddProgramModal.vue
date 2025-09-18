<script setup lang="ts">
import { watch, ref } from 'vue'
import RecordFormModal from './RecordFormModal.vue'
import ConfirmDialog from './ConfirmDialog.vue'
import { useAddProgramForm } from '../composables/useAddProgramForm.ts'

// =========================
// Props & Emits
// =========================
const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit', student: any): void
}>()

const {
    newProgram,
    errors,
    colleges,
    handleSubmit,
    resetForm,
    fetchInitialData,
} = useAddProgramForm(emit)

// =========================
// Confirmation Dialog State
// =========================
const showConfirm = ref(false)

function handleValidatedSubmit() {
    const isValid = handleSubmit()
    if (!isValid) return

    showConfirm.value = true
}

function confirmSubmit() {
    emit('submit', { ...newProgram.value })
    emit('update:modelValue', false)
    resetForm()
    showConfirm.value = false
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
        title="Add New Program"
        @update:modelValue="$emit('update:modelValue', $event)"
        @submit="handleValidatedSubmit"
        @cancel="resetForm"
    >
        <p class="text-sm text-white/60 mb-4">
            Fill out the program's information below.
        </p>

        <div class="flex flex-col gap-4">
            <!-- Program Code -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Program Code
                    <span v-if="errors.program_code" class="text-red-400 ml-2">{{ errors.program_code }}</span>
                </label>
                <input
                    v-model="newProgram.program_code"
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
                    v-model="newProgram.program_name"
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
                    v-model="newProgram.college_code"
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
        title="Confirm Add Program"
        :message="'Are you sure you want to add this program?'"
        :confirmText="'Add'"
        :cancelText="'Cancel'"
        :confirmVariant="'primary'"
        @confirm="confirmSubmit"
        @cancel="cancelSubmit"
    >
    </ConfirmDialog>
</template>
