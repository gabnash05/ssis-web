<script setup lang="ts">
import { ref } from 'vue'
import AuthFormWrapper from '../../components/auth/AuthFormWrapper.vue'
import AuthInput from '../../components/auth/AuthInput.vue'
import AuthButton from '../../components/auth/AuthButton.vue'

import { login } from '../../api/auth'
import { checkAuth } from '../../composables/useAuth'
import { router } from '../../router'

const email = ref('')
const password = ref('')

// ✅ Store error messages per field
const errors = ref({
    email: '',
    password: ''
})

async function handleLogin() {
    errors.value.email = ''
    errors.value.password = ''

    if (!email.value) errors.value.email = 'Email is required'
    if (!password.value) errors.value.password = 'Password is required'

    if (errors.value.email || errors.value.password) return

    try {
        await login(email.value, password.value);
        await checkAuth()
        router.push({ name: "STUDENTS" })
    } catch (err) {
        console.error("Login failed:", err);
    }
}
</script>

<template>
    <AuthFormWrapper
        title="Login"
        footer-text="Don't have an account?"
        footer-link="/signup"
        footer-link-text="Sign up"
    >
        <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
            <AuthInput
                v-model="email"
                label="Email"
                type="email"
                placeholder="Enter your email"
                :error="errors.email"
            />
            <AuthInput
                v-model="password"
                label="Password"
                type="password"
                placeholder="Enter your password"
                :error="errors.password"
            />
            <AuthButton>Login</AuthButton>
        </form>
    </AuthFormWrapper>
</template>
