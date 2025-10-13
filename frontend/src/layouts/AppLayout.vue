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

const isAdmin = computed(() => {
    const user = userStore.currentUser
    console.log('Current user:', user) // Debug log
    return user?.role === 'admin'
})

// =========================
// Tab Logic
// =========================
const availableTabs = ref([
    { id: 0, page: 'STUDENTS' as ApplicationPage, icon: 'student', label: 'Students' },
    { id: 1, page: 'PROGRAMS' as ApplicationPage, icon: 'close-book', label: 'Programs' },
    { id: 2, page: 'COLLEGES' as ApplicationPage, icon: 'school', label: 'Colleges' }
])

const tabs = computed(() => {
    console.log('🔄 Computing tabs, isAdmin:', isAdmin.value)
    
    const baseTabs = [...availableTabs.value]
    
    if (isAdmin.value) {
        // Check if Users tab already exists to avoid duplicates
        if (!baseTabs.find(tab => tab.page === 'USERS')) {
            baseTabs.push({ id: 3, page: 'USERS' as ApplicationPage, icon: 'circle-user', label: 'Users' })
            console.log('➕ Added Users tab')
        }
    } else {
        // Remove Users tab if not admin
        const usersIndex = baseTabs.findIndex(tab => tab.page === 'USERS')
        if (usersIndex > -1) {
            baseTabs.splice(usersIndex, 1)
            console.log('➖ Removed Users tab')
        }
    }
    
    console.log('📋 Final tabs:', baseTabs.map(t => t.label))
    return baseTabs
})

const selectedTab = computed(() => {
    const tab = tabs.value.find(tab => tab.page === props.currentPage)
    return tab ? tab.id : 0
})

const highlightPosition = computed(() => `${selectedTab.value * 3.5}rem`)
const highlightWidth = computed(() => (sidebarOpen.value ? '11rem' : '2.5rem'))

function selectTab(tabId: number) {
    const tab = tabs.value.find(t => t.id === tabId)
    if (tab) {
        emit('change-page', tab.page)
    }
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

// Icon mapping to fix dynamic imports
const iconMap: Record<string, string> = {
    'student': new URL('../assets/icons/student.svg', import.meta.url).href,
    'close-book': new URL('../assets/icons/close-book.svg', import.meta.url).href,
    'school': new URL('../assets/icons/school.svg', import.meta.url).href,
    'circle-user': new URL('../assets/icons/circle-user.svg', import.meta.url).href,
    'chevron-right': new URL('../assets/icons/chevron-right.svg', import.meta.url).href,
    'chevron-left': new URL('../assets/icons/chevron-left.svg', import.meta.url).href,
}

function getIconPath(iconName: string): string {
    return iconMap[iconName] || ''
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
        <div class="w-full h-[90vh] flex p-8 rounded-xl bg-glass border border-white/10 shadow-xl">
            
            <!-- Sidebar -->
            <nav
                id="sidebar"
                class="relative flex flex-col h-full justify-between gap-[30vh] bg-[#1d1d1d] rounded-xl p-4 transition-all duration-300 ease-in-out overflow-hidden"
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
                                    :src="getIconPath('chevron-right')"
                                    alt="Open Sidebar"
                                    class="w-5 h-5 filter invert"
                                >
                                <img
                                    v-else
                                    key="chevron-left"
                                    :src="getIconPath('chevron-left')"
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
                            v-for="tab in tabs"
                            :key="tab.id"
                            class="relative flex items-center gap-3 cursor-pointer w-full h-10 rounded-md transition-all duration-300 hover:bg-white/5"
                            :class="sidebarOpen ? 'pl-2' : 'pl-[6px]'"
                            @click="selectTab(tab.id)"
                        >
                            <img
                                :src="getIconPath(tab.icon)"
                                :alt="tab.label"
                                class="w-6 h-6 filter invert"
                            />

                            <!-- Tab Labels -->
                            <transition name="fade">
                                <span v-if="showLabels" class="text-white text-sm whitespace-nowrap">
                                    {{ tab.label }}
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
                    <img :src="getIconPath('circle-user')" class="w-10 h-10 rounded-full p-1 filter invert" />
                    <transition name="fade">
                        <div v-if="showLabels" class="flex flex-col text-white text-sm min-w-0 flex-1">
                            <span class="truncate">{{ userStore.currentUser?.username || 'User' }}</span>
                            <span class="text-xs text-white/60 truncate">{{ userStore.currentUser?.email || 'No email' }}</span>
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