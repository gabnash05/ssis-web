<script setup lang="ts">
import { ref, watch, onActivated, computed } from 'vue'
import DataTable from '../components/DataTable.vue'
import SearchBar from '../components/SearchBar.vue'
import PaginationControls from '../components/PaginationControls.vue'
import AddUserModal from '../components/AddUserModal.vue'
import EditUserModal from '../components/EditUserModal.vue'
import ConfirmationDialog from '../components/ConfirmDialog.vue'

import { createUser, deleteUser, updateUser } from '../api/users'
import { useDataStore } from '../stores/dataStore'
import { useUserStore } from '../stores/userStore'

import type { SortOrder, User } from '../types'

// =========================
// Table Columns (MATCH User type)
// =========================
const userColumns = [
    { key: 'user_id', label: 'User ID', sortable: true },
    { key: 'username', label: 'Username', sortable: true },
    { key: 'email', label: 'Email', sortable: true },
    { key: 'role', label: 'Role', sortable: true },
]

// =========================
// Table + Pagination State
// =========================
const store = useDataStore()
const users = computed(() => store.users)
const sortBy = ref<string>(userColumns[0].key)
const sortOrder = ref<SortOrder>('ASC')
const searchTerm = ref('')
const searchBy = ref('')
const totalPages = ref(1)
const currentPage = ref(1)
const pageSize = ref(50)

// =========================
// Modal State
// =========================
const showAddModal = ref(false)
const showEditModal = ref(false)
const recordToEdit = ref<User | null>(null)
const showConfirmDialog = ref(false)
const recordToDelete = ref<User | null>(null)
const addModalRef = ref<any>(null)
const editModalRef = ref<any>(null)
const showSelfDeleteWarning = ref(false)

// =========================
// Fetch Users
// =========================
const userStore = useUserStore()
const currentUser = computed(() => userStore.currentUser)

async function fetchUsers() {
    try {
        await store.fetchUsers({
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value,
            sort_order: sortOrder.value,
            q: searchTerm.value,
            search_by: searchBy.value,
        })

        if (store.meta.users) {
            totalPages.value = Math.max(1, Math.ceil(store.meta.users.total / store.meta.users.per_page))
        }
    } catch (err) {
        console.error('Failed to fetch users:', err)
    }
}

// Fetch immediately
fetchUsers()

// Watchers for updates
watch([searchTerm, searchBy, sortBy, sortOrder], () => {
    currentPage.value = 1
    fetchUsers()
})

watch([sortBy, sortOrder, searchTerm, searchBy, currentPage, pageSize], fetchUsers)

onActivated(() => {
    fetchUsers()
})

// =========================
// Actions
// =========================
function handleAdd() {
    showAddModal.value = true
}

function handleEdit(user: User) {
    recordToEdit.value = user
    showEditModal.value = true
}

function handleDelete(user: User) {
    if (user.user_id === currentUser.value?.user_id) {
        showSelfDeleteWarning.value = true
        return
    }

    recordToDelete.value = user
    showConfirmDialog.value = true
}

async function handleUserSubmit(user: User) {
    try {
        await createUser(user)
        store.invalidateAll()
        showAddModal.value = false
        await fetchUsers()
    } catch (err: any) {
        console.error('Error creating user:', err)
        addModalRef.value?.handleBackendErrors?.(err)
    }
}

async function handleUserEdit(user: Partial<User>) {
    if (!recordToEdit.value || typeof recordToEdit.value.user_id !== 'number') return

    try {
        await updateUser(recordToEdit.value.user_id, user)
        store.invalidateAll()
        showEditModal.value = false
        recordToEdit.value = null
        await fetchUsers()
    } catch (err: any) {
        console.error('Error updating user:', err)
        editModalRef.value?.handleBackendErrors?.(err)
    }
}

async function handleUserDelete() {
    if (!recordToDelete.value) return

    try {
        await deleteUser(recordToDelete.value.user_id)
        store.invalidateAll()
        await fetchUsers()
        recordToDelete.value = null
        showConfirmDialog.value = false
    } catch (err) {
        console.error('Error deleting user:', err)
    }
}
</script>

<template>
    <div>
        <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-5">
                <h1 class="text-2xl font-bold text-white">User Management</h1>
                <button
                    @click="handleAdd"
                    class="px-4 py-2 bg-glass border border-white/20 rounded-xl text-white hover:bg-white/20 cursor-pointer transition flex items-center gap-2"
                >
                    <img
                        src="../assets/icons/circle-plus.svg"
                        alt="Add"
                        class="w-4 h-4 filter invert"
                    />
                    <span class="text-sm font-medium">Add User</span>
                </button>
            </div>

            <SearchBar
                v-model="searchTerm"
                v-model:searchBy="searchBy"
                :searchByOptions="userColumns"
            />
        </div>

        <DataTable
            :columns="userColumns"
            :rows="users"
            :sortBy="sortBy"
            :sortOrder="sortOrder"
            :loading="store.loading.users"
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

        <AddUserModal
            ref="addModalRef"
            v-model="showAddModal"
            @submit="handleUserSubmit"
        />

        <EditUserModal
            ref="editModalRef"
            v-model="showEditModal"
            :user="recordToEdit ?? undefined"
            @submit="handleUserEdit"
        />

        <ConfirmationDialog
            v-model="showConfirmDialog"
            title="Delete User"
            :message="`Are you sure you want to delete ${recordToDelete?.username}?`"
            confirm-text="Delete"
            confirm-variant="danger"
            @confirm="handleUserDelete"
        />

        <!-- Self-deletion warning -->
        <ConfirmationDialog
            v-model="showSelfDeleteWarning"
            title="Action Not Allowed"
            message="You cannot delete your own user account."
            confirm-text="OK"
            confirm-variant="primary"
        />
    </div>
</template>
