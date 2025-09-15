<script setup lang="ts">
import type { SortOrder } from '../types'

interface TableColumn<T> {
    key: keyof T
    label: string
    class?: string
    sortable?: boolean
}

const props = defineProps<{
    columns: TableColumn<any>[]
    rows: any[]
    emptyMessage?: string
    sortBy?: string
    sortOrder?: SortOrder
}>()

const emit = defineEmits<{
    (e: 'update:sortBy', key: string): void
    (e: 'update:sortOrder', order: 'ASC' | 'DESC'): void
    (e: 'edit', row: any): void
    (e: 'delete', row: any): void
}>()

function handleHeaderClick(col: TableColumn<any>) {
    if (!col.sortable) return

    if (props.sortBy === col.key) {
        emit('update:sortOrder', props.sortOrder === 'ASC' ? 'DESC' : 'ASC')
    } else {
        emit('update:sortBy', col.key as string)
        emit('update:sortOrder', 'ASC')
    }
}
</script>

<template>
    <div class="max-h-[55vh] overflow-x-auto overflow-y-auto rounded-xl border border-white/10 bg-[#1d1d1d]/40 shadow-lg">
        <table class="min-w-full text-sm text-left text-white">
            <thead class="bg-[#777777]/95 uppercase text-xs font-semibold sticky top-0 z-10">
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

            <tbody>
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
                >
                    <td
                        v-for="col in columns"
                        :key="col.key as string"
                        :class="['px-4 py-3', col.class]"
                    >
                        {{ row[col.key] }}
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
</style>
