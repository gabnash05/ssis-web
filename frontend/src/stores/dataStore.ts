import { defineStore } from 'pinia'
import { listStudents } from '../api/students'
import { listPrograms } from '../api/programs'
import { listColleges } from '../api/colleges'
import { listUsers } from '../api/users'

export const useDataStore = defineStore('data', {
    state: () => ({
        students: [] as any[],
        programs: [] as any[],
        colleges: [] as any[],
        users: [] as any[],
        // meta returned by paginated endpoints
        meta: {
            students: null as any | null,
            programs: null as any | null,
            colleges: null as any | null,
            users: null as any | null,
        },
        // last params used to fetch each resource
        params: {
            students: {} as Record<string, any>,
            programs: {} as Record<string, any>,
            colleges: {} as Record<string, any>,
            users: {} as Record<string, any>,
        },
        // per-resource loading state
        loading: {
            students: false,
            programs: false,
            colleges: false,
            users: false,
        },
        loaded: {
            students: false,
            programs: false,
            colleges: false,
            users: false,
        },
        version: 0,
    }),
    actions: {
        // fetch all with optional params map: { students?: params, programs?: params, colleges?: params }
        async fetchAll(paramsMap: Record<string, any> = {}, force = false) {
            await Promise.all([
                this.fetchStudents(paramsMap.students || {}, force),
                this.fetchPrograms(paramsMap.programs || {}, force),
                this.fetchColleges(paramsMap.colleges || {}, force),
                this.fetchUsers(paramsMap.users || {}, force),
            ])
        },
        async fetchStudents(params: Record<string, any> = {}, force = false) {
            const sameParams = JSON.stringify(this.params.students) === JSON.stringify(params)
            if (!this.loaded.students || force || !sameParams) {
                try {
                    this.loading.students = true
                    const res = await listStudents(params)
                    this.students = res.data || []
                    this.meta.students = res.meta || null
                    this.params.students = params
                    this.loaded.students = true
                } finally {
                    this.loading.students = false
                }
            }
        },
        async fetchPrograms(params: Record<string, any> = {}, force = false) {
            const sameParams = JSON.stringify(this.params.programs) === JSON.stringify(params)
            if (!this.loaded.programs || force || !sameParams) {
                try {
                    this.loading.programs = true
                    const res = await listPrograms(params)
                    this.programs = res.data || []
                    this.meta.programs = res.meta || null
                    this.params.programs = params
                    this.loaded.programs = true
                } finally {
                    this.loading.programs = false
                }
            }
        },
        async fetchColleges(params: Record<string, any> = {}, force = false) {
            const sameParams = JSON.stringify(this.params.colleges) === JSON.stringify(params)
            if (!this.loaded.colleges || force || !sameParams) {
                try {
                    this.loading.colleges = true
                    const res = await listColleges(params)
                    this.colleges = res.data || []
                    this.meta.colleges = res.meta || null
                    this.params.colleges = params
                    this.loaded.colleges = true
                } finally {
                    this.loading.colleges = false
                }
            }
        },
        async fetchUsers(params: Record<string, any> = {}, force = false) {
            const sameParams = JSON.stringify(this.params.users) === JSON.stringify(params)
            if (!this.loaded.users || force || !sameParams) {
                try {
                    this.loading.users = true
                    const res = await listUsers(params)
                    this.users = res.data || []
                    this.meta.users = res.meta || null
                    this.params.users = params
                    this.loaded.users = true
                } finally {
                    this.loading.users = false
                }
            }
        },
        // helper mutators for local updates (useful for optimistic UI)
        addStudent(item: any) {
            this.students.unshift(item)
        },
        updateStudentInStore(id: string, item: any) {
            const idx = this.students.findIndex((s: any) => s.id_number === id)
            if (idx !== -1) this.students.splice(idx, 1, item)
        },
        removeStudentFromStore(id: string) {
            this.students = this.students.filter((s: any) => s.id_number !== id)
        },
        addProgram(item: any) { this.programs.unshift(item) },
        updateProgramInStore(code: string, item: any) {
            const idx = this.programs.findIndex((p: any) => p.program_code === code)
            if (idx !== -1) this.programs.splice(idx, 1, item)
        },
        removeProgramFromStore(code: string) {
            this.programs = this.programs.filter((p: any) => p.program_code !== code)
        },
        addCollege(item: any) { this.colleges.unshift(item) },
        updateCollegeInStore(code: string, item: any) {
            const idx = this.colleges.findIndex((c: any) => c.college_code === code)
            if (idx !== -1) this.colleges.splice(idx, 1, item)
        },
        removeCollegeFromStore(code: string) {
            this.colleges = this.colleges.filter((c: any) => c.college_code !== code)
        },

        bumpVersion() {
            this.version++
        },

        invalidateAll() {
            this.loaded.students = false
            this.loaded.programs = false
            this.loaded.colleges = false
            this.loaded.users = false
            this.bumpVersion()
        },

        invalidate(type: 'students' | 'programs' | 'colleges' | 'users') {
            this.loaded[type] = false
            this.bumpVersion()
        },
    },
})