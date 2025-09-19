import { createRouter, createWebHistory } from 'vue-router'
import StudentsView from '../views/StudentsView.vue'
import ProgramsView from '../views/ProgramsView.vue'
import CollegesView from '../views/CollegesView.vue'
import LoginView from '../views/auth/LoginView.vue'
import SignupView from '../views/auth/SignupView.vue'

const routes = [
    { path: '/login', name: 'LOGIN', component: LoginView, meta: { layout: 'auth' } },
    { path: '/signup', name: 'SIGNUP', component: SignupView, meta: { layout: 'auth' } },
    {path: '/', redirect: { name: 'LOGIN' } },

    { path: '/students', name: 'STUDENTS', component: StudentsView, meta: { layout: 'app', requiresAuth: true } },
    { path: '/programs', name: 'PROGRAMS', component: ProgramsView, meta: { layout: 'app', requiresAuth: true } },
    { path: '/colleges', name: 'COLLEGES', component: CollegesView, meta: { layout: 'app', requiresAuth: true } }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})

const isAuthenticated = () => {
    return localStorage.getItem('token') !== null
}

// ✅ Navigation Guard
router.beforeEach((to, _, next) => {
    if (to.meta.requiresAuth && !isAuthenticated()) {
        next('/login')
    } else {
        next()
    }
})
