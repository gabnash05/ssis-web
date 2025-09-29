import { ref } from 'vue'
import { getCurrentUser } from '../api/auth'

export const isAuthenticated = ref(false)
export const currentUser = ref<any>(null)

export async function checkAuth() {
    try {
        const res = await getCurrentUser()
        currentUser.value = res.data
        isAuthenticated.value = true
    } catch {
        currentUser.value = null
        isAuthenticated.value = false
    }
}
