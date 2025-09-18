import { ref, watch } from 'vue'
import { fetchColleges, fetchPrograms } from '../utils/fetchData'

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
    }

    async function fetchInitialData() {
        colleges.value = await fetchColleges()
        programs.value = await fetchPrograms()
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
        resetForm,
        fetchInitialData,
        handleSubmit,
        handleIdInput,
    }
}
