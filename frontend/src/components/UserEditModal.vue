<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useUserStore } from '../stores/userStore'
import type { User } from '../types'

const props = defineProps<{
    modelValue: boolean
    user: User | null
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
}>()

const userStore = useUserStore()
const formData = ref<User | null>(props.user ? { ...props.user } : null)

// Sync user data when modal opens or user prop changes
watch(
    () => props.user,
    (newVal) => {
        formData.value = newVal ? { ...newVal } : null
    }
)
watch(
    () => props.modelValue,
    (isOpen) => {
        if (isOpen && props.user) formData.value = { ...props.user }
    }
)

// Close when pressing Escape
function close() {
    emit('update:modelValue', false)
}

function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') close()
}

onMounted(() => window.addEventListener('keydown', handleKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', handleKeydown))

// Logout handler
async function handleLogout() {
    await userStore.logoutUser()
    emit('update:modelValue', false)
}
</script>

<template>
    <Teleport to="body">
        <transition name="fade">
            <div
                v-if="modelValue"
                class="fixed inset-0 z-50 flex justify-center items-center backdrop-blur-xl bg-black/40"
            >
                <!-- Modal Container -->
                <div
                    class="bg-neutral-900 border border-white/10 rounded-2xl shadow-xl w-[26rem] p-6 relative text-white"
                >
                    <!-- Close button -->
                    <button
                        @click="close"
                        class="absolute top-3 right-3 text-white/60 hover:text-white cursor-pointer"
                    >
                        ✕
                    </button>

                    <!-- Header -->
                    <div class="flex flex-col items-center text-center mb-6">
                        <img
                            src="../assets/icons/circle-user.svg"
                            class="w-16 h-16 rounded-full bg-white/10 p-3 mb-3 filter invert"
                        />
                        <h2 class="text-lg font-semibold">Account Settings</h2>
                        <p class="text-xs text-white/60">Your Profile Information</p>
                    </div>

                    <!-- User Info -->
                    <div v-if="formData" class="flex flex-col gap-3 text-sm">
                        <div>
                            <label class="block text-xs text-white/60 mb-1">Username</label>
                            <p class="bg-neutral-800 p-2 rounded border border-white/10 text-white/90">
                                {{ formData.username || '—' }}
                            </p>
                        </div>

                        <div>
                            <label class="block text-xs text-white/60 mb-1">Email</label>
                            <p class="bg-neutral-800 p-2 rounded border border-white/10 text-white/90">
                                {{ formData.email || '—' }}
                            </p>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="mt-6 border-t border-white/10 pt-4">
                        <button
                            @click="handleLogout"
                            class="w-full py-2 bg-red-600/50 hover:bg-red-700 text-white text-sm rounded-lg transition cursor-pointer"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </div>
        </transition>
    </Teleport>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
