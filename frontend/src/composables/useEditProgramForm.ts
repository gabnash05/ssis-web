import { ref } from 'vue'
import { fetchColleges } from '../utils/fetchData'
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
    }

    async function fetchInitialData() {
        colleges.value = await fetchColleges()
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

    function handleSubmit() {
        return validateForm()
    }

    return {
        editedProgram,
        errors,
        colleges,
        resetForm,
        fetchInitialData,
        loadProgram,
        handleSubmit,
    }
}
