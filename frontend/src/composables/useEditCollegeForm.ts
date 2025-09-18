import { ref } from 'vue'
import type { College } from '../types'

export function useEditCollegeForm(emit: any) {
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

    function handleSubmit() {
        return validateForm()
    }

    return {
        editedCollege,
        errors,
        resetForm,
        loadCollege,
        handleSubmit,
    }
}
