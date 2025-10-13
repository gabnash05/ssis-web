import { createRouter, createWebHistory } from 'vue-router'
import StudentsView from '../views/StudentsView.vue'
import ProgramsView from '../views/ProgramsView.vue'
import CollegesView from '../views/CollegesView.vue'
import LoginView from '../views/auth/LoginView.vue'
import SignupView from '../views/auth/SignupView.vue'
import UsersView from '../views/UsersView.vue'

import { isAuthenticated, checkAuth } from '../composables/useAuth'
import { useUserStore } from '../stores/userStore'

const routes = [
    { path: '/login', name: 'LOGIN', component: LoginView, meta: { layout: 'auth' } },
    { path: '/signup', name: 'SIGNUP', component: SignupView, meta: { layout: 'auth' } },
    { path: '/', redirect: { name: 'LOGIN' } },

    { path: '/users', name: 'USERS', component: UsersView, meta: { layout: 'app', requiresAuth: true, adminOnly: true } },
    { path: '/students', name: 'STUDENTS', component: StudentsView, meta: { layout: 'app', requiresAuth: true, adminOnly: false } },
    { path: '/programs', name: 'PROGRAMS', component: ProgramsView, meta: { layout: 'app', requiresAuth: true, adminOnly: false } },
    { path: '/colleges', name: 'COLLEGES', component: CollegesView, meta: { layout: 'app', requiresAuth: true, adminOnly: false } }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})

// Navigation guard
router.beforeEach(async (to, _, next) => {
    if (to.meta.requiresAuth) {
        if (!isAuthenticated.value) {
            await checkAuth()
        }
        if (!isAuthenticated.value) {
            return next('/login')
        }

        const userStore = useUserStore()
        
        if (!userStore.currentUser) {
            try {
                await userStore.fetchCurrentUser()
            } catch (error) {
                console.error('Failed to fetch user in router guard:', error)
                return next({ name: 'STUDENTS' })
            }
        }

        if (to.meta.adminOnly && userStore.currentUser?.role !== 'admin') {
            return next({ name: 'STUDENTS' })
        }
    }

    next()
})