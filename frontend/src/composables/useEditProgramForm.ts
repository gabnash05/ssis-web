import { ref } from 'vue'
import { listColleges } from '../api/colleges'
import type { Program } from '../types'

export function useEditProgramForm(emit: any) {
// =========================
// State
// =========================
    const editedProgram = ref({
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
// Form Logic
// =========================
    function resetForm() {
        Object.assign(editedProgram.value, {
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

    function loadProgram(program: Program) {
        Object.assign(editedProgram.value, program)
    }

    function validateForm() {
        const currentErrors = {
            program_code: editedProgram.value.program_code.trim() ? '' : 'Required*',
            program_name: editedProgram.value.program_name.trim() ? '' : 'Required*',
            college_code: editedProgram.value.college_code.trim() ? '' : 'Required*',
        }

        if (editedProgram.value.program_code.trim() && editedProgram.value.program_code.trim().length > 20) {
            currentErrors.program_code = 'Too Long'
        }

        if (editedProgram.value.program_name.trim() && editedProgram.value.program_name.trim().length > 50) {
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
        generalError.value = err.message || 'Failed to update program. Please try again.';
    }

    function handleSubmit() {
        return validateForm()
    }

    return {
        editedProgram,
        errors,
        colleges,
        generalError,
        resetForm,
        fetchInitialData,
        loadProgram,
        handleSubmit,
        handleBackendErrors,
    }
}
