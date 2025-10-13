import { ref } from 'vue'
import { getCurrentUser } from '../api/auth'
import { useUserStore } from '../stores/userStore'

export const isAuthenticated = ref(false)

export async function checkAuth() {
    try {
        const userStore = useUserStore()
        const response = await getCurrentUser()
        
        if (response.data && response.data.data) {
            userStore.currentUser = response.data.data
            isAuthenticated.value = true
            return true
        } else {
            throw new Error('No user data in response')
        }
    } catch (error) {
        isAuthenticated.value = false
        const userStore = useUserStore()
        userStore.currentUser = null
        return false
    }
}