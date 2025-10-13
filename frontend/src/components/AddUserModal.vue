<script setup lang="ts">
import { ref, watch } from 'vue'
import RecordFormModal from './RecordFormModal.vue'
import ConfirmDialog from './ConfirmDialog.vue'
import type { User } from '../types'

// =========================
// Props & Emits
// =========================
const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit', user: User & { password: string }): void
}>()

// =========================
// Reactive State
// =========================
const newUser = ref({
    username: '',
    email: '',
    role: 'user',
    password: '',
})

const errors = ref<Record<string, string>>({})
const generalError = ref('')
const showConfirm = ref(false)
const isSubmitting = ref(false)

// =========================
// Validation
// =========================
function validate(): boolean {
    errors.value = {}
    if (!newUser.value.username) errors.value.username = 'Username is required'
    if (!newUser.value.email) errors.value.email = 'Email is required'
    if (!newUser.value.password) errors.value.password = 'Password is required'
    return Object.keys(errors.value).length === 0
}

// =========================
// Form Handling
// =========================
function handleValidatedSubmit() {
    if (!validate()) return
    showConfirm.value = true
}

async function confirmSubmit() {
    isSubmitting.value = true
    try {
        emit('submit', { user_id: 0, ...newUser.value })
    } catch (err: any) {
        console.error('Error adding user:', err)
        generalError.value = 'An unexpected error occurred.'
    } finally {
        isSubmitting.value = false
        showConfirm.value = false
    }
}

function cancelSubmit() {
    showConfirm.value = false
}

function resetForm() {
    newUser.value = {
        username: '',
        email: '',
        role: 'user',
        password: '',
    }
    errors.value = {}
    generalError.value = ''
}

// =========================
// Backend Error Handling
// =========================
function handleBackendErrors(err: any) {
    if (err.response?.data?.errors) {
        errors.value = err.response.data.errors
    } else if (err.response?.data?.message) {
        generalError.value = err.response.data.message
    } else {
        generalError.value = 'An unexpected server error occurred.'
    }
}

// Expose to parent
defineExpose({ handleBackendErrors })

// =========================
// Watch for Modal Open
// =========================
watch(() => props.modelValue, (isOpen) => {
    if (isOpen) resetForm()
})
</script>

<template>
    <RecordFormModal
        :model-value="modelValue"
        title="Add New User"
        @update:modelValue="$emit('update:modelValue', $event)"
        @submit="handleValidatedSubmit"
        @cancel="resetForm"
    >
        <p class="text-sm text-white/60 mb-4">
            Fill out the user's information below.
        </p>

        <div class="flex flex-col gap-4">
            <!-- Username -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Username
                    <span v-if="errors.username" class="text-red-400 ml-2">{{ errors.username }}</span>
                </label>
                <input
                    v-model="newUser.username"
                    placeholder="john"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- Email -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Email
                    <span v-if="errors.email" class="text-red-400 ml-2">{{ errors.email }}</span>
                </label>
                <input
                    v-model="newUser.email"
                    type="email"
                    placeholder="user@example.com"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- Password -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Password
                    <span v-if="errors.password" class="text-red-400 ml-2">{{ errors.password }}</span>
                </label>
                <input
                    v-model="newUser.password"
                    type="password"
                    placeholder="••••••"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- Role -->
            <div>
                <label class="block text-xs text-white/70 mb-1">Role</label>
                <select
                    v-model="newUser.role"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                >
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                </select>
            </div>

            <!-- General Error -->
            <div v-if="generalError" class="p-2 rounded text-red-400 text-sm">
                {{ generalError }}
            </div>
        </div>
    </RecordFormModal>

    <!-- Confirmation Dialog -->
    <ConfirmDialog
        v-model="showConfirm"
        title="Confirm Add User"
        message="Are you sure you want to add this user?"
        confirmText="Add"
        cancelText="Cancel"
        confirmVariant="primary"
        @confirm="confirmSubmit"
        @cancel="cancelSubmit"
    />
</template>
