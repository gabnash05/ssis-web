<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { ApplicationPage } from '../types'
import { useUserStore } from '../stores/userStore'
import UserEditModal from '../components/UserEditModal.vue';

// =========================
// Props & Emits
// =========================
const props = defineProps<{
    currentPage: ApplicationPage
}>()

const emit = defineEmits<{
    (e: 'change-page', page: ApplicationPage): void
}>()

// =========================
// Sidebar State
// =========================
const sidebarOpen = ref(false)
const showLabels = ref(false)
const showLogo = ref(false)

// =========================
// User State
// =========================
const userStore = useUserStore()

onMounted(async () => {
    try {
        await userStore.fetchCurrentUser()
    } catch (err) {
        console.error('Failed to fetch current user:', err)
    }
})

// =========================
// Tab Logic
// =========================
const tabPositions = [0, 1, 2] // 0: Students, 1: Programs, 2: Colleges
const selectedTab = computed(() => {
    switch (props.currentPage) {
        case 'STUDENTS': return 0
        case 'PROGRAMS': return 1
        case 'COLLEGES': return 2
        default: return 0
    }
})

const highlightPosition = computed(() => `${selectedTab.value * 3.5}rem`)
const highlightWidth = computed(() => (sidebarOpen.value ? '11rem' : '2.5rem'))

function selectTab(index: number) {
    const page: ApplicationPage =
        index === 0 ? 'STUDENTS' : index === 1 ? 'PROGRAMS' : 'COLLEGES'
    emit('change-page', page)
}

function toggleSidebar() {
    if (sidebarOpen.value) {
        showLabels.value = false
        showLogo.value = false
        setTimeout(() => (sidebarOpen.value = false), 200)
    } else {
        sidebarOpen.value = true
        setTimeout(() => {
            showLogo.value = true
            showLabels.value = true
        }, 250)
    }
}
</script>

<template>
    <!-- Background -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
        <div class="absolute w-[500px] h-[500px] bg-[#2e64b0]/40 rounded-full blur-[100px] top-1/4 left-1/4"></div>
        <div class="absolute w-[600px] h-[600px] bg-[#d425c9]/20 rounded-full blur-[120px] top-2/3 right-1/4"></div>
        <div class="absolute w-[450px] h-[450px] bg-[#2cdfdf]/20 rounded-full blur-[90px] bottom-1/4 left-1/2"></div>
    </div>

    <!-- Glass Background -->
    <div class="min-h-screen py-7 px-15 flex justify-center items-center">
        <div class="w-full h-full max-h-[calc(100vh-5rem)] flex p-8 rounded-xl bg-glass border border-white/10 shadow-xl">
            
            <!-- Sidebar -->
            <nav
                id="sidebar"
                class="relative flex flex-col h-full justify-between gap-[35vh] bg-[#1d1d1d] rounded-xl p-4 transition-all duration-300 ease-in-out overflow-hidden"
                :class="sidebarOpen ? 'w-52' : 'w-18'"
            >
                <div class="flex flex-col gap-5 w-full">
                    <!-- Top Control Button Row -->
                    <div class="flex justify-between items-center w-full">
                        <!-- Logo (fades in when sidebar is open) -->
                        <transition name="fade">
                            <div v-if="showLogo" class="w-10 h-10 bg-white rounded-md"></div>
                        </transition>

                        <!-- Toggle Button (always right-aligned) -->
                        <button
                            @click.stop="toggleSidebar"
                            class="w-10 h-10 rounded-md flex justify-center items-center hover:bg-white/5 transition cursor-pointer"
                        >
                            <transition name="fade" mode="out-in">
                                <img
                                    v-if="!sidebarOpen"
                                    key="chevron-right"
                                    src="../assets/icons/chevron-right.svg"
                                    alt="Open Sidebar"
                                    class="w-5 h-5 filter invert"
                                >
                                <img
                                    v-else
                                    key="chevron-left"
                                    src="../assets/icons/chevron-left.svg"
                                    alt="Close Sidebar"
                                    class="w-5 h-5 filter invert"
                                >
                            </transition>
                        </button>
                    </div>

                    <!-- Tabs -->
                    <div class="relative flex flex-col gap-4 mt-6 w-full">
                        <!-- Moving glass highlight -->
                        <div
                            class="absolute h-10 rounded-md bg-glass border border-white/10 shadow-xl transition-all duration-300 ease-in-out"
                            :style="{ 
                                top: highlightPosition, 
                                width: highlightWidth,
                            }"
                        ></div>

                        <!-- Tab buttons -->
                        <div
                            v-for="(_, index) in tabPositions"
                            :key="index"
                            class="relative flex items-center gap-3 cursor-pointer w-full h-10 rounded-md transition-all duration-300 hover:bg-white/5"
                            :class="sidebarOpen ? 'pl-2' : 'pl-[6px]'"
                            @click="selectTab(index)"
                        >
                            <img
                                v-if="index === 0"
                                src="../assets/icons/student.svg"
                                alt="Students"
                                class="w-6 h-6 filter invert"
                            >
                            <img
                                v-else-if="index === 1"
                                src="../assets/icons/close-book.svg"
                                alt="Programs"
                                class="w-6 h-6 filter invert"
                            >
                            <img
                                v-else
                                src="../assets/icons/school.svg"
                                alt="Colleges"
                                class="w-6 h-6 filter invert"
                            >

                            <!-- Tab Labels -->
                            <transition name="fade">
                                <span v-if="showLabels" class="text-white text-sm whitespace-nowrap">
                                    {{ index === 0 ? 'Students' : index === 1 ? 'Programs' : 'Colleges' }}
                                </span>
                            </transition>
                        </div>
                    </div>
                </div>

                <!-- Bottom User Section -->
                <div
                    class="flex items-center gap-3 w-full h-14 rounded-md transition-all duration-300 hover:bg-white/5 cursor-pointer"
                    :class="sidebarOpen ? 'pl-2' : 'justify-center'"
                    @click="userStore.showUserModal = true"
                >
                    <img src="../assets/icons/circle-user.svg" class="w-10 h-10 rounded-full p-1 filter invert" />
                    <transition name="fade">
                        <div v-if="showLabels" class="flex flex-col text-white text-sm min-w-0 flex-1"> <!-- Added min-w-0 and flex-1 -->
                            <span class="truncate">{{ userStore.currentUser?.username || 'User' }}</span> <!-- Added truncate -->
                            <span class="text-xs text-white/60 truncate">{{ userStore.currentUser?.email || 'No email' }}</span> <!-- Added truncate -->
                        </div>
                    </transition>
                </div>
            </nav>

            <UserEditModal
                v-model="userStore.showUserModal"
                :user="userStore.currentUser"
            />
            <!-- Main Content Area -->
            <div class="flex-1 px-6 overflow-y-auto">
                <slot />
            </div>
        </div>
    </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateX(-10px);
}
</style>
