import { ref } from 'vue'

export function useAddCollegeForm(emit: any) {
// =========================
// State
// =========================
    const newCollege = ref({
        college_code: '',
        college_name: '',
    })

    const errors = ref({
        college_code: '',
        college_name: '',
    })

// =========================
// Methods
// =========================

    function resetForm() {
        Object.assign(newCollege.value, {
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

    function validateForm() {
        const currentErrors = {
            college_code: newCollege.value.college_code.trim() ? '' : 'Required*',
            college_name: newCollege.value.college_name.trim() ? '' : 'Required*',
        }

        if (newCollege.value.college_code.trim() && newCollege.value.college_code.trim().length > 20) {
            currentErrors.college_code = 'Too Long'
        }

        if (newCollege.value.college_name.trim() && newCollege.value.college_name.trim().length > 50) {
            currentErrors.college_name = 'Too Long'
        }

        errors.value = currentErrors
        return Object.values(currentErrors).every((err) => !err)
    }

    function handleSubmit() {
        return validateForm()
    }

    return {
        newCollege,
        errors,
        resetForm,
        handleSubmit,
    }
}
