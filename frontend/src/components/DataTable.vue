<script setup lang="ts">
import type { SortOrder, TableColumn } from '../types'
import LoadingSkeleton from '../components/LoadingSkeleton.vue'
import { buildPhotoUrl } from '../utils/photoUrlHelper'
import { ref } from 'vue'

// =========================
// Props & Emits
// =========================
const props = defineProps<{
    columns: TableColumn<any>[]
    rows: any[]
    emptyMessage?: string
    sortBy?: string
    sortOrder?: SortOrder
    loading?: boolean
}>()

const emit = defineEmits<{
    (e: 'update:sortBy', key: string): void
    (e: 'update:sortOrder', order: 'ASC' | 'DESC'): void
    (e: 'edit', row: any): void
    (e: 'delete', row: any): void
}>()

// =========================
// Modal State
// =========================
const showModal = ref(false)
const selectedStudent = ref<any>(null)

// =========================
// Methods
// =========================
function handleHeaderClick(col: TableColumn<any>) {
    if (!col.sortable) return

    if (props.sortBy === col.key) {
        emit('update:sortOrder', props.sortOrder === 'ASC' ? 'DESC' : 'ASC')
    } else {
        emit('update:sortBy', col.key as string)
        emit('update:sortOrder', 'ASC')
    }
}

function openPhotoModal(row: any) {
    selectedStudent.value = row
    showModal.value = true
}

function closeModal() {
    showModal.value = false
    selectedStudent.value = null
}

// Close modal when clicking outside the image
function handleBackdropClick(event: MouseEvent) {
    if ((event.target as HTMLElement).classList.contains('modal-backdrop')) {
        closeModal()
    }
}

// Close modal with Escape key
function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape' && showModal.value) {
        closeModal()
    }
}
</script>

<template>
    <div class="relative max-h-[65vh] overflow-x-auto overflow-y-auto rounded-xl border border-white/10 bg-[#1d1d1d]/40 shadow-lg">
        <table class="min-w-full text-sm text-left text-white">
            <thead class="bg-[#777777]/95 uppercase text-xs font-semibold sticky top-0 z-1">
                <tr>
                    <th
                        v-for="col in columns"
                        :key="col.key as string"
                        :class="[
                            'px-4 py-3 select-none',
                            sortBy === col.key ? 'bg-white/10': '',
                            col.sortable ? 'cursor-pointer hover:bg-white/10' : '',
                            col.class
                        ]"
                        @click="handleHeaderClick(col)"
                    >
                        <div class="flex items-center gap-1">
                            <span>{{ col.label }}</span>
                            <!-- Reserve icon space always -->
                            <span
                                v-if="col.sortable"
                                class="ml-2 inline-flex w-3 h-3 relative"
                            >
                                <transition name="fade">
                                    <img
                                        v-if="sortBy === col.key && sortOrder === 'ASC'"
                                        key="ASC"
                                        src="../assets/icons/chevron-down.svg"
                                        alt="ASCending Sort"
                                        class="absolute inset-0 w-3 h-3 filter invert"
                                    />
                                    <img
                                        v-else-if="sortBy === col.key && sortOrder === 'DESC'"
                                        key="DESC"
                                        src="../assets/icons/chevron-up.svg"
                                        alt="DESCending Sort"
                                        class="absolute inset-0 w-3 h-3 filter invert"
                                    />
                                </transition>
                            </span>
                        </div>
                    </th>
                    <!-- Actions Column Header -->
                    <th class="px-4 py-3 text-right">Actions</th>
                </tr>
            </thead>
            <tbody class="relative">
                <tr v-if="rows.length === 0" class="text-center">
                    <td
                        :colspan="columns.length + 1"
                        class="px-4 py-6 text-gray-400"
                    >
                        {{ emptyMessage || 'No records found.' }}
                    </td>
                </tr>
                <tr
                    v-for="(row, rowIndex) in rows"
                    :key="rowIndex"
                    class="hover:bg-white/5 transition"
                    :title="(Object.values(row).includes('Malik') || Object.values(row).includes('Maulana')) ? 'Flat 1 Sir Please HEHE <3' : ''"
                >
                    <td
                        v-for="col in columns"
                        :key="col.key as string"
                        :class="[
                            'px-4 py-3', 
                            col.class, 
                            (row[col.key] === 'Malik' || row[col.key] === 'Maulana') ? ' text-yellow-300 font-medium' : ''
                        ]"
                    >
                        <template v-if="col.key === 'photo_url'">
                            <!-- Pressable Photo -->
                            <button
                                v-if="row.photo_path"
                                @click="openPhotoModal(row)"
                                class="cursor-pointer hover:opacity-80 transition-opacity duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 rounded-full"
                                aria-label="View student photo"
                            >
                                <img
                                    :src="buildPhotoUrl(row.photo_path)"
                                    class="w-10 h-10 rounded-full object-cover"
                                    alt="Profile"
                                />
                            </button>
                            
                            <div v-else class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
                                <img 
                                    src="../assets/icons/circle-user.svg" 
                                    class="w-6 h-6 text-gray-400 filter invert" 
                                    alt="No profile"
                                />
                            </div>
                        </template>
                        
                        <template v-else>
                            {{ row[col.key] && row[col.key] !== '' ? row[col.key] : '-' }}
                        </template>
                    </td>

                    <!-- Actions Column -->
                    <td class="px-4 py-3 text-right flex items-center justify-end gap-2">
                        <!-- Edit Button -->
                        <button
                            class="group p-1 rounded hover:bg-white/10 transition cursor-pointer relative w-7 h-7 flex items-center justify-center"
                            @click="$emit('edit', row)"
                            aria-label="Edit"
                        >
                            <!-- Default Icon -->
                            <img
                                src="../assets/icons/edit.svg"
                                alt="Edit"
                                class="absolute inset-0 m-auto w-5 h-5 filter invert opacity-100 group-hover:opacity-0 transition-opacity duration-200 ease-in-out"
                            >
                            <!-- Hover Icon -->
                            <img
                                src="../assets/icons/edit-pen.svg"
                                alt="Edit Hover"
                                class="absolute inset-0 m-auto w-5 h-5 filter invert opacity-0 group-hover:opacity-100 transition-opacity duration-200 ease-in-out"
                            >
                        </button>
                        <!-- Delete Button -->
                        <button
                            class="group p-1 rounded hover:bg-white/10 transition cursor-pointer relative w-7 h-7 flex items-center justify-center"
                            @click="$emit('delete', row)"
                            aria-label="Delete"
                        >
                            <!-- Default Icon -->
                            <img
                                src="../assets/icons/trash.svg"
                                alt="Delete"
                                class="absolute inset-0 m-auto w-5 h-5 filter invert opacity-100 group-hover:opacity-0 transition-opacity duration-200 ease-in-out"
                            >
                            <!-- Hover Icon -->
                            <img
                                src="../assets/icons/open-trash.svg"
                                alt="Delete Hover"
                                class="absolute inset-0 m-auto w-6 h-6 filter invert opacity-0 group-hover:opacity-100 transition-opacity duration-200 ease-in-out"
                            >
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <LoadingSkeleton v-if="loading" />
    </div>

    <!-- Photo Modal -->
    <div
        v-if="showModal"
        class="modal-backdrop fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
        @click="handleBackdropClick"
        @keydown="handleKeydown"
    >
        <div class="relative max-w-4xl max-h-full">
            <!-- Close Button -->
            <button
                @click="closeModal"
                class="absolute -top-10 right-0 text-white hover:text-gray-300 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-white rounded-full p-1"
                aria-label="Close modal"
            >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
            
            <!-- Student Photo -->
            <img
                v-if="selectedStudent?.photo_path"
                :src="buildPhotoUrl(selectedStudent.photo_path)"
                class="max-w-full max-h-[80vh] object-contain rounded-lg shadow-2xl"
                :alt="`Photo of ${selectedStudent.name || 'student'}`"
            />
            
            <!-- Fallback if no photo -->
            <div
                v-else
                class="w-64 h-64 bg-gray-700 rounded-lg flex items-center justify-center text-white"
            >
                <div class="text-center">
                    <img 
                        src="../assets/icons/circle-user.svg" 
                        class="w-20 h-20 mx-auto mb-4 filter invert opacity-50" 
                        alt="No profile"
                    />
                    <p class="text-gray-400">No photo available</p>
                </div>
            </div>
            
            <!-- Student Name (if available) -->
            <div
                v-if="selectedStudent?.name"
                class="text-white text-center mt-4 text-lg font-semibold"
            >
                {{ selectedStudent.name }}
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Fade in/out for sort icons */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

/* Edit Button Hover (Blue) */
.group:hover img[alt="Edit"],
.group:hover img[alt="Edit Hover"] {
    filter: invert(39%) sepia(87%) saturate(2586%) hue-rotate(185deg) brightness(97%) contrast(102%);
    transition: filter 0.1s ease-in-out;
}

/* Trash Button Hover (Red) */
.group:hover img[alt="Delete"],
.group:hover img[alt="Delete Hover"] {
    filter: invert(32%) sepia(86%) saturate(2643%) hue-rotate(340deg) brightness(96%) contrast(103%);
    transition: filter 0.1s ease-in-out;
}

/* Modal animations */
.modal-backdrop {
    animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>