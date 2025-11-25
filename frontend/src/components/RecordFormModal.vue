<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'

// =========================
// Props & Emits
// =========================
const props = defineProps<{
    modelValue: boolean
    title?: string
    loading?: boolean
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit'): void
    (e: 'cancel'): void
}>()

// =========================
// Methods
// =========================
function close() {
    if (!props.loading) { // Only allow close if not loading
        emit('update:modelValue', false)
        emit('cancel')
    }
}

function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape' && !props.loading) { // Only close with Escape if not loading
        close()
    }
}

// =========================
// Lifecycle
// =========================
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
                    class="bg-glass-lg border border-white/10 rounded-2xl shadow-xl w-[32rem] p-6 relative"
                    :class="{ 'pointer-events-none': loading }"
                >
                    <!-- Loading Overlay -->
                    <div
                        v-if="loading"
                        class="absolute inset-0 bg-black/50 flex items-center justify-center rounded-2xl z-10"
                    >
                        <div class="flex items-center gap-3 text-white">
                            <div class="w-6 h-6 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                            <span>Saving...</span>
                        </div>
                    </div>

                    <!-- Header -->
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-2xl font-semibold text-white">
                            {{ title || 'Add Record' }}
                        </h2>
                        <button
                            @click="close"
                            :disabled="loading"
                            class="p-1 rounded-md hover:bg-white/10 transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                            aria-label="Close"
                        >
                            <img src="../assets/icons/cross.svg" class="w-5 h-5 filter invert" />
                        </button>
                    </div>

                    <!-- Body -->
                    <div class="space-y-4">
                        <slot />
                    </div>

                    <!-- Footer -->
                    <div class="flex justify-end gap-3 mt-6">
                        <button
                            @click="$emit('submit')"
                            :disabled="loading"
                            class="px-4 py-2 rounded-xl bg-blue-500 text-white hover:bg-blue-600 transition cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Save
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