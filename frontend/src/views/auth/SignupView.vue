<script setup lang="ts">
import { ref } from 'vue'
import AuthFormWrapper from '../../components/auth/AuthFormWrapper.vue'
import AuthInput from '../../components/auth/AuthInput.vue'
import AuthButton from '../../components/auth/AuthButton.vue'
import { signup } from '../../api/auth'
import { checkAuth } from '../../composables/useAuth'
import { router } from '../../router'

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

// ✅ Store error messages per field
const errors = ref({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
})

async function handleSignup() {
    errors.value = { username: '', email: '', password: '', confirmPassword: '' }

    if (!username.value) errors.value.username = 'Name is required'
    if (!email.value) errors.value.email = 'Email is required'
    if (!password.value) errors.value.password = 'Password is required'
    if (!confirmPassword.value) {
        errors.value.confirmPassword = 'Please confirm password'
    } else if (password.value !== confirmPassword.value) {
        errors.value.confirmPassword = 'Passwords do not match'
    }

    if (Object.values(errors.value).some(e => e)) return

    try {
        await signup(username.value, email.value, password.value);
        await checkAuth()
        router.push({ name: "STUDENTS" })
    } catch (err) {
        console.error("Login failed:", err);
    }
}
</script>

<template>
    <AuthFormWrapper
        title="Sign Up"
        footer-text="Already have an account?"
        footer-link="/login"
        footer-link-text="Login"
    >
        <form @submit.prevent="handleSignup" class="flex flex-col gap-4">
            <AuthInput
                v-model="username"
                label="Username"
                type="text"
                placeholder="Enter your full name"
                :error="errors.username"
            />
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
                placeholder="Enter a password"
                :error="errors.password"
            />
            <AuthInput
                v-model="confirmPassword"
                label="Confirm Password"
                type="password"
                placeholder="Confirm your password"
                :error="errors.confirmPassword"
            />
            <AuthButton>Sign Up</AuthButton>
        </form>
    </AuthFormWrapper>
</template>
