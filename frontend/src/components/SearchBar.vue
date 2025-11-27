<script setup lang="ts">
import { ref, watch, nextTick, onMounted, onBeforeUnmount, computed } from 'vue'

interface searchByOption {
    key: string
    label: string
    sortable?: boolean
}

const props = defineProps<{
    searchByOptions: searchByOption[]
}>()

// Add a "None" option at the start dynamically
const optionsWithNone = computed(() => {
  const excludedKeys = ['photo_url', 'year_level', 'gender'];

  console.log('Original Options:', props.searchByOptions);
  
  // Filter out the excluded options
  const filteredOptions = props.searchByOptions.filter(
    option => !excludedKeys.includes(option.key)
  );
  
  return [
    { key: 'none', label: 'None' },
    ...filteredOptions
  ];
});

const searchTerm = ref('')
const isOpen = ref(true)
const debounceTimer = ref<number | null>(null)
const debounceDelay = 300 // ms delay before emitting

const selectedSearchBy = ref('none')
const isDropdownOpen = ref(false)

const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
    (e: 'update:searchBy', value: string): void
}>()

function open() {
    isOpen.value = true
    nextTick(() => {
        const input = document.getElementById('search-input') as HTMLInputElement | null
        input?.focus()
    })
}

function close() {
    if (searchTerm.value.trim() !== '') return (searchTerm.value = '')

    isOpen.value = false
    searchTerm.value = ''
    emit('update:modelValue', '')
}

function toggle() {
    isOpen.value ? close() : open()
}

watch(searchTerm, (v) => {
    if (debounceTimer.value) clearTimeout(debounceTimer.value)
    debounceTimer.value = window.setTimeout(() => {
        emit('update:modelValue', v)
    }, debounceDelay)
})

function selectSearchBy(optionKey: string) {
    selectedSearchBy.value = optionKey
    emit('update:searchBy', optionKey === 'none' ? '' : optionKey)
    isDropdownOpen.value = false
}

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
    <div class="relative flex items-center gap-2">
        <!-- Search Bar -->
        <div
            class="relative flex items-center py-2 rounded-2xl bg-glass border border-white/20 shadow-lg transition-all duration-300 ease-in-out overflow-hidden"
            :class="isOpen ? 'w-80 px-3' : 'w-11 h-10 justify-center px-1'"
        >
            <div
                class="flex-shrink-0 mr-2 transition-all duration-250 ease-in-out"
                :class="isOpen ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-2 pointer-events-none absolute'"
            >
                <img src="../assets/icons/search.svg" alt="search-left" class="w-5 h-5 filter invert" />
            </div>

            <input
                id="search-input"
                v-model="searchTerm"
                type="text"
                placeholder="Search..."
                class="flex-1 bg-transparent outline-none text-white placeholder-gray-300 font-light transition-all duration-300 ease-in-out"
                :class="isOpen ? 'opacity-100 max-w-full' : 'opacity-0 max-w-0 pointer-events-none'"
            />

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
                        class="w-5 h-5 filter invert transition-transform duration-300 hover:scale-120 hover:bg-black/20 rounded-md p-1"
                    />
                </transition>
            </button>
        </div>

        <!-- Search By Dropdown -->
        <div class="relative">
            <button
                @click="isDropdownOpen = !isDropdownOpen"
                class="flex items-center gap-2 px-3 py-2 rounded-2xl bg-glass border border-white/20 cursor-pointer hover:bg-white/20 transition text-white/80 text-sm"
            >
                <img src="../assets/icons/category-search.svg" alt="Filter" class="w-6 h-6 z-10" />
                <!-- Show label only if not 'none' -->
                <span v-if="selectedSearchBy !== 'none'">
                    {{ optionsWithNone.find(opt => opt.key === selectedSearchBy)?.label }}
                </span>
            </button>

            <div
                v-if="isDropdownOpen"
                class="absolute right-0 mt-2 w-40 bg-neutral-900/80 border border-white/10 rounded-xl shadow-lg backdrop-blur-md z-10"
            >
                <ul class="divide-y divide-white/10">
                    <li
                        v-for="option in optionsWithNone"
                        :key="option.key"
                        class="px-3 py-2 text-white text-sm hover:bg-white/10 cursor-pointer transition"
                        @click="selectSearchBy(option.key)"
                    >
                        {{ option.label }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>
.icon-fade-enter-active,
.icon-fade-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}
.icon-fade-enter-from,
.icon-fade-leave-to {
    opacity: 0;
    transform: scale(0.8) rotate(-90deg);
}
</style>
