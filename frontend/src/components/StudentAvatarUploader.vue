<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
    modelValue: File | null
    existingAvatarUrl?: string
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: File | null): void
    (e: 'removeExisting'): void  // Add this new emit
}>()

const avatarPreview = ref<string>('')
const fileInput = ref<HTMLInputElement>()
const hasExistingAvatar = ref(false)

// Initialize with existing avatar if provided
if (props.existingAvatarUrl) {
    avatarPreview.value = props.existingAvatarUrl
    hasExistingAvatar.value = true
}

function handleFileSelect(event: Event) {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0]
    
    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file')
            return
        }
        
        // Validate file size (e.g., 5MB max)
        if (file.size > 5 * 1024 * 1024) {
            alert('File size must be less than 5MB')
            return
        }
        
        emit('update:modelValue', file)
        
        // Create preview
        const reader = new FileReader()
        reader.onload = (e) => {
            avatarPreview.value = e.target?.result as string
        }
        reader.readAsDataURL(file)
        
        // User selected a new file, so they're replacing the existing one
        hasExistingAvatar.value = false
    }
}

function removeAvatar() {
    if (hasExistingAvatar.value) {
        // User wants to remove the existing avatar
        emit('removeExisting')
        avatarPreview.value = ''
        hasExistingAvatar.value = false
    } else {
        // User wants to remove the newly selected file
        emit('update:modelValue', null)
        // Revert to showing existing avatar if available
        if (props.existingAvatarUrl) {
            avatarPreview.value = props.existingAvatarUrl
            hasExistingAvatar.value = true
        } else {
            avatarPreview.value = ''
        }
    }
    
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}

function triggerFileInput() {
    fileInput.value?.click()
}

// Watch for changes to existingAvatarUrl
watch(() => props.existingAvatarUrl, (newUrl) => {
    if (newUrl && !avatarPreview.value.startsWith('data:')) {
        avatarPreview.value = newUrl
        hasExistingAvatar.value = true
    }
})
</script>

<template>
    <div class="flex flex-col items-center gap-4">
        <label class="block text-xs text-white/70 mb-1 self-start">
            Profile Photo
        </label>
        
        <div class="relative">
            <!-- Avatar Display -->
            <div 
                v-if="avatarPreview" 
                class="w-24 h-24 rounded-full bg-gray-700 overflow-hidden border-2 border-white/20"
            >
                <img 
                    :src="avatarPreview" 
                    alt="Profile preview" 
                    class="w-full h-full object-cover"
                />
            </div>
            
            <!-- Placeholder when no avatar -->
            <div 
                v-else 
                class="w-24 h-24 rounded-full bg-gray-700 flex items-center justify-center border-2 border-white/20"
            >
                <img 
                    src="../assets/icons/circle-user.svg" 
                    class="w-12 h-12 text-gray-400 filter invert" 
                    alt="No profile"
                />
            </div>
            
            <!-- Remove button (show only when there's an avatar) -->
            <button
                v-if="avatarPreview"
                @click="removeAvatar"
                class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-white text-xs hover:bg-red-600 transition-colors cursor-pointer"
                type="button"
            >
                ×
            </button>
        </div>
        
        <!-- File Input (hidden) -->
        <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            class="hidden"
        />
        
        <!-- Upload Button -->
        <button
            @click="triggerFileInput"
            type="button"
            class="px-4 py-2 bg-glass border border-white/20 rounded-lg text-white hover:bg-white/20 cursor-pointer transition text-sm"
        >
            {{ avatarPreview ? 'Change Photo' : 'Upload Photo' }}
        </button>
        
        <p class="text-xs text-white/50 text-center">
            JPG, PNG or WebP. Max 5MB.
        </p>
    </div>
</template>