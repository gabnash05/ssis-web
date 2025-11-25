<script setup lang="ts">
import { watch, ref } from 'vue'
import RecordFormModal from './RecordFormModal.vue'
import ConfirmDialog from './ConfirmDialog.vue'
import StudentAvatarUploader from './StudentAvatarUploader.vue'
import { useEditStudentForm } from '../composables/useEditStudentForm.ts'
import { buildPhotoUrl } from '../utils/photoUrlHelper.ts';
import type { Student } from '../types.ts';

// =========================
// Props & Emits
// =========================
const props = defineProps<{
    modelValue: boolean
    student: Student | null
    loading?: boolean
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit', student: any): void
}>()

// =========================
// Composable State
// =========================
const {
    editedStudent,
    errors,
    college_code,
    colleges,
    filteredPrograms,
    avatarFile,
    generalError,
    handleSubmit,
    handleIdInput,
    resetForm,
    fetchInitialData,
    loadStudent,
    handleBackendErrors,
    requestAvatarUpload,
    uploadToSupabase,
    finalizeAvatar,
    fetchAvatarUrl,
    removeAvatar,
} = useEditStudentForm()

// =========================
// Local State for Existing Avatar
// =========================
const existingAvatarUrl = ref<string>('')
const removeExistingPhoto = ref(false)

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
        const studentData = { ...editedStudent.value }
        
        if (removeExistingPhoto.value) {
            studentData.photo_path = ''
        }
        
        emit('submit', studentData)
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
// Load Student with Avatar
// =========================
async function loadStudentWithAvatar(student: Student) {
    loadStudent(student)
    
    // Load existing avatar if available
    if (student.photo_path) {
        existingAvatarUrl.value = buildPhotoUrl(student.photo_path)
    } else {
        existingAvatarUrl.value = ''
    }
}

// =========================
// Watch for Modal Open
// =========================
watch(
    () => props.modelValue,
    async (isOpen) => {
        if (isOpen && props.student) {
            resetForm()
            await fetchInitialData()
            await loadStudentWithAvatar(props.student)
        }
    }
)

watch(
    () => props.student,
    (student) => {
        if (props.modelValue && student) {
            loadStudentWithAvatar(student)
        }
    },
    { immediate: true }
)

// Expose the handleBackendErrors function for parent components
defineExpose({
    handleBackendErrors,
    requestAvatarUpload,
    uploadToSupabase,
    finalizeAvatar,
    avatarFile,
    fetchAvatarUrl,
    removeAvatar,
})
</script>

<template>
    <RecordFormModal
        :model-value="modelValue"
        title="Edit Student"
        :loading="loading"
        @update:modelValue="$emit('update:modelValue', $event)"
        @submit="handleValidatedSubmit"
        @cancel="resetForm"
    >
        <p class="text-sm text-white/60 mb-4">
            Edit the student's information below.
        </p>

        <div class="max-h-[65vh] overflow-y-auto pr-2 flex flex-col gap-4">
            <!-- Avatar Uploader with existing photo -->
            <StudentAvatarUploader
                v-model="avatarFile"
                :existing-avatar-url="existingAvatarUrl"
                @remove-existing="removeExistingPhoto = true"
            />

            <!-- ID Number -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    ID Number
                    <span v-if="errors.id_number" class="text-red-400 ml-2">
                        {{ errors.id_number }}
                    </span>
                </label>
                <input
                    :value="editedStudent.id_number"
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
                    v-model="editedStudent.first_name"
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
                    v-model="editedStudent.last_name"
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
                    v-model="editedStudent.year_level"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                >
                    <option :value="1">1st Year</option>
                    <option :value="2">2nd Year</option>
                    <option :value="3">3rd Year</option>
                    <option :value="4">4th Year</option>
                    <option :value="5">5th Year</option>
                </select>
            </div>

            <!-- Gender -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Gender
                    <span v-if="errors.gender" class="text-red-400 ml-2">{{ errors.gender }}</span>
                </label>
                <select
                    v-model="editedStudent.gender"
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
                    <option disabled value="" class="text-white/50">Select a college</option>
                    <option v-for="college in colleges" :key="college.code" :value="college.code">
                        {{ college.code }} - {{ college.name }}
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
                    v-model="editedStudent.program_code"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400 disabled:opacity-50"
                    :disabled="filteredPrograms.length === 0"
                >
                    <option disabled value="" class="text-white/50">Select a program</option>
                    <option
                        v-for="program in filteredPrograms"
                        :key="program.code"
                        :value="program.code"
                    >
                        {{ program.code }} - {{ program.name }}
                    </option>
                </select>
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
        title="Confirm Edit Student"
        :message="'Are you sure you want to edit this student?'"
        :confirmText="'Edit'"
        :cancelText="'Cancel'"
        :confirmVariant="'primary'"
        @confirm="confirmSubmit"
        @cancel="cancelSubmit"
    >
    </ConfirmDialog>
</template>