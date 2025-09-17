<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{
    modelValue: boolean
    title?: string
    message?: string
    confirmText?: string
    cancelText?: string
    confirmVariant?: 'primary' | 'danger' | 'success' 
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'confirm'): void
    (e: 'cancel'): void
}>()

function close() {
    emit('update:modelValue', false)
    emit('cancel')
}

function confirm() {
    emit('confirm')
    emit('update:modelValue', false)
}

function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') close()
}

onMounted(() => window.addEventListener('keydown', handleKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', handleKeydown))
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
                    class="bg-glass-lg border border-white/10 rounded-2xl shadow-xl w-[28rem] p-6 relative"
                >
                    <!-- Header -->
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold text-white">
                            {{ title || 'Confirm Action' }}
                        </h2>
                        <button
                            @click="close"
                            class="p-1 rounded-md hover:bg-white/10 transition cursor-pointer"
                            aria-label="Close"
                        >
                            <img src="../assets/icons/cross.svg" class="w-5 h-5 filter invert" />
                        </button>
                    </div>

                    <!-- Body -->
                    <div class="text-white/80 text-sm mb-6">
                        {{ message || 'Are you sure you want to continue?' }}
                    </div>

                    <!-- Footer -->
                    <div class="flex justify-end gap-3">
                        <button
                            @click="close"
                            class="px-4 py-2 rounded-xl bg-neutral-700 text-white hover:bg-neutral-600 transition cursor-pointer"
                        >
                            {{ cancelText || 'Cancel' }}
                        </button>
                        <button
                            @click="confirm"
                            class="px-4 py-2 rounded-xl text-white transition cursor-pointer"
                            :class="{
                                'bg-blue-500 hover:bg-blue-600': confirmVariant === 'primary' || !confirmVariant,
                                'bg-red-500 hover:bg-red-600': confirmVariant === 'danger',
                                'bg-green-500 hover:bg-green-600': confirmVariant === 'success'
                            }"
                        >
                            {{ confirmText || 'Confirm' }}
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
    transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
