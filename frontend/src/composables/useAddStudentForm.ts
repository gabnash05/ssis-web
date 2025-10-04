import { ref, watch } from 'vue'
import { listColleges } from '../api/colleges'
import { listPrograms } from '../api/programs'

export function useAddStudentForm(emit: any) {
// =========================
// State
// =========================
    const newStudent = ref({
        id_number: '',
        first_name: '',
        last_name: '',
        year_level: 1,
        gender: 'FEMALE',
        program_code: '',
    })

    const errors = ref({
        id_number: '',
        first_name: '',
        last_name: '',
        year_level: '',
        gender: '',
        college_code: '',
        program_code: '',
    })

    const colleges = ref<{ code: string; name: string }[]>([])
    const programs = ref<{ code: string; name: string; college_code: string }[]>([])
    const filteredPrograms = ref<{ code: string; name: string }[]>([])
    const college_code = ref('')
    const generalError = ref('')

// =========================
// State
// =========================

    function resetForm() {
        Object.assign(newStudent.value, {
            id_number: '',
            first_name: '',
            last_name: '',
            year_level: 1,
            gender: 'FEMALE',
            program_code: '',
        })
        college_code.value = ''
        filteredPrograms.value = []

        resetErrors()
    }

    function resetErrors() {
        Object.keys(errors.value).forEach((key) => {
            errors.value[key as keyof typeof errors.value] = ''
        })
        generalError.value = ''
    }

    async function fetchInitialData() {
        const collegesRes = await listColleges({})
        colleges.value = collegesRes.data.map(c => ({
            code: c.college_code,
            name: c.college_name,
        }))

        const programsRes = await listPrograms({})
        programs.value = programsRes.data.map(p => ({
            code: p.program_code,
            name: p.program_name,
            college_code: p.college_code,
        }))
    }

    function validateForm() {
        const currentErrors = {
            id_number: newStudent.value.id_number.trim() ? '' : 'Required*',
            first_name: newStudent.value.first_name.trim() ? '' : 'Required*',
            last_name: newStudent.value.last_name.trim() ? '' : 'Required*',
            year_level: newStudent.value.year_level ? '' : 'Required*',
            gender: newStudent.value.gender ? '' : 'Required*',
            college_code: college_code.value ? '' : 'Required*',
            program_code: newStudent.value.program_code ? '' : 'Required*',
        }

        if (newStudent.value.first_name.trim() && newStudent.value.first_name.trim().length > 50) {
            currentErrors.first_name = 'Too Long'
        }

        if (newStudent.value.last_name.trim() && newStudent.value.last_name.trim().length > 50) {
            currentErrors.last_name = 'Too Long'
        }

        if (newStudent.value.id_number.trim() && !/^[0-9]{4}-[0-9]{4}$/.test(newStudent.value.id_number)) {
            currentErrors.id_number = 'Format: YYYY-NNNN'
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
            if (details.id_number) errors.value.id_number = details.id_number;
            if (details.first_name) errors.value.first_name = details.first_name;
            if (details.last_name) errors.value.last_name = details.last_name;
            if (details.year_level) errors.value.year_level = details.year_level;
            if (details.gender) errors.value.gender = details.gender;
            if (details.college_code) errors.value.college_code = details.college_code;
            if (details.program_code) errors.value.program_code = details.program_code;
        }
        
        // Display general error message
        generalError.value = err.message || 'Failed to create student. Please try again.';
    }

    function handleSubmit() {
        return validateForm()
    }

    function handleIdInput(event: Event) {
        const input = event.target as HTMLInputElement
        let value = input.value.replace(/[^0-9-]/g, '')
        if (value.length > 4 && value[4] !== '-') {
            value = value.slice(0, 4) + '-' + value.slice(4)
        }
        
        value = value.slice(0, 9)
        newStudent.value.id_number = value

        input.value = value
    }

    watch(college_code, (code) => {
        filteredPrograms.value = programs.value.filter((p) => p.college_code === code)

        if (!filteredPrograms.value.some((p) => p.code === newStudent.value.program_code)) {
            newStudent.value.program_code = ''
        }
    })

    return {
        newStudent,
        errors,
        college_code,
        colleges,
        programs,
        filteredPrograms,
        generalError,
        resetForm,
        fetchInitialData,
        handleSubmit,
        handleIdInput,
        handleBackendErrors,
    }
}
