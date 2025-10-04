import { ref } from 'vue'
import { listColleges } from '../api/colleges'

export function useAddProgramForm(emit: any) {
// =========================
// State
// =========================
    const newProgram = ref({
        program_code: '',
        program_name: '',
        college_code: '',
    })

    const errors = ref({
        program_code: '',
        program_name: '',
        college_code: '',
    })

    const colleges = ref<{ code: string; name: string }[]>([])
    const generalError = ref('')

// =========================
// Methods
// =========================

    function resetForm() {
        Object.assign(newProgram.value, {
            program_code: '',
            program_name: '',
            college_code: '',
        })

        resetErrors()
    }

    function resetErrors() {
        Object.keys(errors.value).forEach((key) => {
            errors.value[key as keyof typeof errors.value] = ''
        })
        generalError.value = ''
    }

    async function fetchInitialData() {
        const res = await listColleges({})
        colleges.value = res.data.map(c => ({
            code: c.college_code,
            name: c.college_name,
        }))
    }

    function validateForm() {
        const currentErrors = {
            program_code: newProgram.value.program_code.trim() ? '' : 'Required*',
            program_name: newProgram.value.program_name.trim() ? '' : 'Required*',
            college_code: newProgram.value.college_code.trim() ? '' : 'Required*',
        }

        if (newProgram.value.program_code.trim() && newProgram.value.program_code.trim().length > 20) {
            currentErrors.program_code = 'Too Long'
        }

        if (newProgram.value.program_name.trim() && newProgram.value.program_name.trim().length > 50) {
            currentErrors.program_name = 'Too Long'
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
            if (details.program_code) errors.value.program_code = details.program_code;
            if (details.program_name) errors.value.program_name = details.program_name;
            if (details.college_code) errors.value.college_code = details.college_code;
        }
        
        // Display general error message
        generalError.value = err.message || 'Failed to create program. Please try again.';
    }

    function handleSubmit() {
        return validateForm()
    }

    return {
        newProgram,
        errors,
        colleges,
        generalError,
        resetForm,
        fetchInitialData,
        handleSubmit,
        handleBackendErrors,
    }
}
