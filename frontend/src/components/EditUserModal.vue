<script setup lang="ts">
import { ref, watch } from 'vue'
import RecordFormModal from './RecordFormModal.vue'
import ConfirmDialog from './ConfirmDialog.vue'
import type { User } from '../types'

const props = defineProps<{
    modelValue: boolean
    user?: User
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit', user: Partial<User>): void
}>()

const editedUser = ref({
    username: '',
    email: '',
    role: 'user'
})

const errors = ref<Record<string, string>>({})
const generalError = ref('')
const showConfirm = ref(false)
const isSubmitting = ref(false)

function validate(): boolean {
    errors.value = {}
    if (!editedUser.value.username) errors.value.username = 'Username required'
    if (!editedUser.value.email) errors.value.email = 'Email required'
    return Object.keys(errors.value).length === 0
}

function handleValidatedSubmit() {
    if (!validate()) return
    showConfirm.value = true
}

async function confirmSubmit() {
    isSubmitting.value = true
    try {
        emit('submit', { ...editedUser.value })
    } catch (err: any) {
        console.error('Error editing user:', err)
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
    editedUser.value = {
        username: props.user?.username ?? '',
        email: props.user?.email ?? '',
        role: props.user?.role ?? 'user'
    }
    errors.value = {}
    generalError.value = ''
}

function handleBackendErrors(err: any) {
    if (err.response?.data?.errors) {
        errors.value = err.response.data.errors
    } else if (err.response?.data?.message) {
        generalError.value = err.response.data.message
    } else {
        generalError.value = 'An unexpected server error occurred.'
    }
}

defineExpose({ handleBackendErrors })

watch(() => props.modelValue, (isOpen) => {
    if (isOpen) resetForm()
})
</script>

<template>
    <RecordFormModal
        :model-value="modelValue"
        title="Edit User"
        @update:modelValue="$emit('update:modelValue', $event)"
        @submit="handleValidatedSubmit"
        @cancel="resetForm"
    >
        <p class="text-sm text-white/60 mb-4">
            Update the user information below.
        </p>

        <div class="flex flex-col gap-4">
            <!-- Username -->
            <div>
                <label class="block text-xs text-white/70 mb-1">
                    Username
                    <span v-if="errors.username" class="text-red-400 ml-2">{{ errors.username }}</span>
                </label>
                <input
                    v-model="editedUser.username"
                    placeholder="jdoe"
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
                    v-model="editedUser.email"
                    type="email"
                    placeholder="user@example.com"
                    class="w-full p-2 rounded bg-neutral-800 text-sm text-white border border-white/10 focus:border-blue-400"
                />
            </div>

            <!-- Role -->
            <div>
                <label class="block text-xs text-white/70 mb-1">Role</label>
                <select
                    v-model="editedUser.role"
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

    <ConfirmDialog
        v-model="showConfirm"
        title="Confirm Edit"
        message="Are you sure you want to save these changes?"
        confirmText="Save"
        cancelText="Cancel"
        confirmVariant="primary"
        @confirm="confirmSubmit"
        @cancel="cancelSubmit"
    />
</template>
