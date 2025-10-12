<script setup lang="ts">
import { ref } from 'vue'
import AuthFormWrapper from '../../components/auth/AuthFormWrapper.vue'
import AuthInput from '../../components/auth/AuthInput.vue'
import AuthButton from '../../components/auth/AuthButton.vue'

import { login } from '../../api/auth'
import { checkAuth } from '../../composables/useAuth'
import { router } from '../../router'

const email = ref('');
const password = ref('');
const isLoading = ref(false);

// ✅ Store error messages per field
const errors = ref({
    email: '',
    password: ''
});

// General error message for login failures
const generalError = ref('');

async function handleLogin() {
    errors.value.email = '';
    errors.value.password = '';
    generalError.value = '';

    if (!email.value) errors.value.email = 'Email is required';
    if (!password.value) errors.value.password = 'Password is required';

    if (errors.value.email || errors.value.password) return;

    try {
        isLoading.value = true;

        await login(email.value, password.value);
        await checkAuth()
        router.push({ name: "STUDENTS" })
    } catch (err: any) {
        console.error("Login failed:", err);
        
        // Check if it's a backend error with details
        if (err.response?.data?.details) {
            const details = err.response.data.details;
            if (details.email) errors.value.email = details.email;
            if (details.password) errors.value.password = details.password;
        }
        
        generalError.value = err.message || 'Login failed. Please try again.';
    } finally {
        isLoading.value = false;
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

            <!-- General Error Message -->
            <div v-if="generalError" class="p-2 rounded text-red-400 text-sm">
                {{ generalError }}
            </div>

            <AuthButton :loading="isLoading" :disabled="isLoading">
                {{ isLoading ? "Logging in..." : "Login"}}
            </AuthButton>
        </form>
    </AuthFormWrapper>
</template>
