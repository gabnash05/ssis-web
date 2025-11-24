import { ref } from 'vue'
import type { College } from '../types'

export function useEditCollegeForm() {
// =========================
// State
// =========================
    const editedCollege = ref({
        college_code: '',
        college_name: '',
    })

    const errors = ref({
        college_code: '',
        college_name: '',
    })

    const generalError = ref('')

// =========================
// Form Logic
// =========================
    function resetForm() {
        Object.assign(editedCollege.value, {
            college_code: '',
            college_name: '',
        })

        resetErrors()
    }

    function resetErrors() {
        Object.keys(errors.value).forEach((key) => {
            errors.value[key as keyof typeof errors.value] = ''
        })
        generalError.value = ''
    }

    function loadCollege(college: College) {
        Object.assign(editedCollege.value, college)
    }

    function validateForm() {
        const currentErrors = {
            college_code: editedCollege.value.college_code.trim() ? '' : 'Required*',
            college_name: editedCollege.value.college_name.trim() ? '' : 'Required*',
        }

        if (editedCollege.value.college_code.trim() && editedCollege.value.college_code.trim().length > 20) {
            currentErrors.college_code = 'Too Long'
        }

        if (editedCollege.value.college_name.trim() && editedCollege.value.college_name.trim().length > 50) {
            currentErrors.college_name = 'Too Long'
        }

        errors.value = currentErrors
        return Object.values(currentErrors).every((err) => !err)
    }

    function handleBackendErrors(err: any) {
        // Clear previous errors
        resetErrors()
        
        // Check if it's a backend error with details
        if (err.response?.data?.details) {
            const details = err.response.data.details;
            if (details.college_code) errors.value.college_code = details.college_code;
            if (details.college_name) errors.value.college_name = details.college_name;
        }
        
        // Display general error message
        generalError.value = err.message || 'Failed to update college. Please try again.';
    }

    function handleSubmit() {
        return validateForm()
    }

    return {
        editedCollege,
        errors,
        generalError,
        resetForm,
        loadCollege,
        handleSubmit,
        handleBackendErrors,
    }
}
