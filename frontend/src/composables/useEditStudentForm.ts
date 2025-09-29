import { ref, watch } from 'vue'
import { listColleges } from '../api/colleges'
import { listPrograms } from '../api/programs'

export function useEditStudentForm(emit: any) {
// =========================
// State
// =========================
    const editedStudent = ref({
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
// Form Logic
// =========================
    function resetForm() {
        Object.assign(editedStudent.value, {
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

    function loadStudent(student: any) {
        Object.assign(editedStudent.value, student)
        college_code.value = findCollegeCodeByProgram(student.program_code)
        filteredPrograms.value = programs.value.filter((p) => p.college_code === college_code.value)
    }

    function findCollegeCodeByProgram(programCode: string): string {
        const program = programs.value.find((p) => p.code === programCode)
        return program ? program.college_code : ''
    }

    function validateForm() {
        const currentErrors = {
            id_number: editedStudent.value.id_number.trim() ? '' : 'Required*',
            first_name: editedStudent.value.first_name.trim() ? '' : 'Required*',
            last_name: editedStudent.value.last_name.trim() ? '' : 'Required*',
            year_level: editedStudent.value.year_level ? '' : 'Required*',
            gender: editedStudent.value.gender ? '' : 'Required*',
            college_code: college_code.value ? '' : 'Required*',
            program_code: editedStudent.value.program_code ? '' : 'Required*',
        }

        if (editedStudent.value.first_name.trim() && editedStudent.value.first_name.trim().length > 50) {
            currentErrors.first_name = 'Too Long'
        }

        if (editedStudent.value.last_name.trim() && editedStudent.value.last_name.trim().length > 50) {
            currentErrors.last_name = 'Too Long'
        }

        if (editedStudent.value.id_number.trim() && !/^[0-9]{4}-[0-9]{4}$/.test(editedStudent.value.id_number)) {
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
        editedStudent.value.id_number = value

        input.value = value
    }

    watch(college_code, (code) => {
        filteredPrograms.value = programs.value.filter((p) => p.college_code === code)

        if (!filteredPrograms.value.some((p) => p.code === editedStudent.value.program_code)) {
            editedStudent.value.program_code = ''
        }
    })

    return {
        editedStudent,
        errors,
        college_code,
        colleges,
        programs,
        filteredPrograms,
        resetForm,
        fetchInitialData,
        loadStudent,
        handleSubmit,
        handleIdInput,
    }
}
