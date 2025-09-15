<script setup lang="ts">
import { ref, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'

const searchTerm = ref('')
const isOpen = ref(true)
const debounceTimer = ref<number | null>(null)
const debounceDelay = 300 // ms delay before emitting

const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()

function open() {
    isOpen.value = true
    nextTick(() => {
        const input = document.getElementById('search-input') as HTMLInputElement | null
        input?.focus()
    })
}

function close() {
    if (searchTerm.value.trim() !== '') return searchTerm.value = ''

    isOpen.value = false
    searchTerm.value = ''
    emit('update:modelValue', '')
}

function toggle() {
    isOpen.value ? close() : open()
}

// Debounced watcher
watch(searchTerm, (v) => {
    if (debounceTimer.value) clearTimeout(debounceTimer.value)
    debounceTimer.value = window.setTimeout(() => {
        emit('update:modelValue', v)
    }, debounceDelay)
})

function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape' && isOpen.value) close()
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => {
    window.removeEventListener('keydown', onKeydown)
    if (debounceTimer.value) clearTimeout(debounceTimer.value)
})
</script>

<template>
    <div class="relative flex items-center">
        <div
            class="relative flex items-center py-2 rounded-2xl bg-glass border border-white/20 shadow-lg transition-all duration-300 ease-in-out overflow-hidden"
            :class="isOpen ? 'w-80 px-3 ' : 'w-11 h-10 justify-center px-1'"
        >
            <!-- Left icon (visible only when open) -->
            <div
                class="flex-shrink-0 mr-2 transition-all duration-250 ease-in-out"
                :class="isOpen ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-2 pointer-events-none absolute'"
            >
                <img src="../assets/icons/search.svg" alt="search-left" class="w-5 h-5 filter invert" />
            </div>

            <!-- Search input -->
            <input
                id="search-input"
                v-model="searchTerm"
                type="text"
                placeholder="Search..."
                class="flex-1 bg-transparent outline-none text-white placeholder-gray-300 font-light transition-all duration-300 ease-in-out"
                :class="isOpen ? 'opacity-100 max-w-full' : 'opacity-0 max-w-0 pointer-events-none'"
            />

            <!-- Right button (absolute, so it doesn't shift during animation) -->
            <button
                @click="toggle"
                class="absolute right-2 flex-shrink-0 px-1 cursor-pointer transition-transform duration-300"
                type="button"
                :aria-label="isOpen ? 'Close search' : 'Open search'"
            >
                <transition name="icon-fade" mode="out-in">
                    <img
                        v-if="!isOpen"
                        key="search-closed"
                        src="../assets/icons/search.svg"
                        alt="Search"
                        class="w-5 h-5 filter invert transition-transform duration-300 hover:scale-110"
                    />
                    <img
                        v-else
                        key="search-opened"
                        src="../assets/icons/cross.svg"
                        alt="Close"
                        class="w-5 h-5 filter invert transition-transform duration-300 rotate-0 hover:scale-120 hover:bg-black/20 rounded-md p-1"
                    />
                </transition>
            </button>
        </div>
    </div>
</template>

<style scoped>
/* Fade animation for right icon switch */
.icon-fade-enter-active,
.icon-fade-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}
.icon-fade-enter-from,
.icon-fade-leave-to {
    opacity: 0;
    transform: scale(0.8) rotate(-90deg);
}

/* Blue filter only on hover (when closed) */
button:hover img[alt="Search"] {
    filter: invert(39%) sepia(87%) saturate(2586%) hue-rotate(185deg) brightness(97%) contrast(102%);
    transition: filter 0.15s ease-in-out;
}

/* Ensure smooth transitions for width, padding, and opacity */
.transition-all {
    transition-property: width, max-width, padding, opacity, transform;
}
.duration-250 {
    transition-duration: 250ms;
}
</style>
