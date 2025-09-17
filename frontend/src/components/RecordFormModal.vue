<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{
    modelValue: boolean
    title?: string
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'submit'): void
    (e: 'cancel'): void
}>()

function close() {
    emit('update:modelValue', false)
    emit('cancel')
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
                    class="bg-glass-lg border border-white/10 rounded-2xl shadow-xl w-[32rem] p-6 relative"
                >
                    <!-- Header -->
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-2xl font-semibold text-white">
                            {{ title || 'Add Record' }}
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
                    <div class="space-y-4">
                        <slot />
                    </div>

                    <!-- Footer -->
                    <div class="flex justify-end gap-3 mt-6">
                        <button
                            @click="$emit('submit')"
                            class="px-4 py-2 rounded-xl bg-blue-500 text-white hover:bg-blue-600 transition cursor-pointer"
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
