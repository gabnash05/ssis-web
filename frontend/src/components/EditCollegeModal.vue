<script setup lang="ts">
import { watch, ref } from 'vue'
import RecordFormModal from './RecordFormModal.vue'
import ConfirmDialog from './ConfirmDialog.vue'
import { useEditCollegeForm } from '../composables/useEditCollegeForm.ts'
import type { College } from '../types.ts';

// =========================
// Props & Emits
// =========================
const props = defineProps<{
    modelValue: boolean
    college: College | null
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit', college: any): void
}>()

// =========================
// Composable State
// =========================
const {
    editedCollege,
    errors,
    generalError,
    resetForm,
    loadCollege,
    handleSubmit,
    handleBackendErrors,
} = useEditCollegeForm(emit)

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
        emit('submit', { ...editedCollege.value })
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
// Watchers
// =========================
watch(
    () => props.college,
    (newCollege) => {
        if (newCollege) {
            loadCollege(newCollege)  // ⬅️ Populate the form
        } else {
            resetForm()
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
        title="Edit College"
        @update:modelValue="$emit('update:modelValue', $event)"
        @submit="handleValidatedSubmit"
        @cancel="resetForm"
    >
        <p class="text-sm text-white/60 mb-4">
            Edit the college's information below.
        </p>

        <div class="flex flex-col gap-4">
            <!-- College Code -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    College Code
                    <span v-if="errors.college_code" class="text-red-400 ml-2">{{ errors.college_code }}</span>
                </label>
                <input
                    v-model="editedCollege.college_code"
                    placeholder="CCS"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- College Name -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    College Name
                    <span v-if="errors.college_name" class="text-red-400 ml-2">{{ errors.college_name }}</span>
                </label>
                <input
                    v-model="editedCollege.college_name"
                    placeholder="College of Computer Studies"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- General Error Message -->
            <div v-if="generalError" class="p-2 rounded text-red-400 text-sm">
                {{ generalError }}
            </div>
        </div>
    </RecordFormModal>

    <!-- Confirmation Dialog -->
    <ConfirmDialog
        v-model="showConfirm"
        title="Confirm Edit College"
        :message="'Are you sure you want to edit this college?'"
        :confirmText="'Edit'"
        :cancelText="'Cancel'"
        :confirmVariant="'primary'"
        @confirm="confirmSubmit"
        @cancel="cancelSubmit"
    >
    </ConfirmDialog>
</template>
