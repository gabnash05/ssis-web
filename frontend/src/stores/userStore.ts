import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentUser, updateUser, logout } from '../api/auth'

export const useUserStore = defineStore('user', () => {
    const router = useRouter()
    const currentUser = ref<any | null>(null)
    const showUserModal = ref(false)

    async function fetchCurrentUser() {
        const response = await getCurrentUser()
        currentUser.value = response.data.data
    }

    async function saveUser(updatedData: any) {
        const response = await updateUser(updatedData)
        currentUser.value = response.data.data
    }

    async function logoutUser() {
        try {
            await logout()

            currentUser.value = null
            showUserModal.value = false

            router.push({ name: 'LOGIN' })
        } catch (error) {
            console.error('Logout failed:', error)
        }
    }

    return {
        currentUser,
        showUserModal,
        logoutUser,
        fetchCurrentUser,
        saveUser
    }
})