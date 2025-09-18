export async function fetchColleges() {
    try {
        // Replace with real API later
        return [
            { code: 'COE', name: 'College of Engineering' },
            { code: 'CAS', name: 'College of Arts and Sciences' },
            { code: 'CBA', name: 'College of Business Administration' },
            { code: 'CCS', name: 'College of Computer Studies'},
        ]
    } catch (err) {
        console.error('Failed to fetch colleges:', err)
        return []
    }
}

export async function fetchPrograms() {
    try {
        // Replace with real API later
        return [
            { code: 'BSCS', name: 'B.S. Computer Science', college_code: 'CAS' },
            { code: 'BSIT', name: 'B.S. Information Technology', college_code: 'CAS' },
            { code: 'BSEE', name: 'B.S. Electrical Engineering', college_code: 'COE' },
            { code: 'BSME', name: 'B.S. Mechanical Engineering', college_code: 'COE' },
            { code: 'BSBA', name: 'B.S. Business Administration', college_code: 'CBA' },
        ]
    } catch (err) {
        console.error('Failed to fetch programs:', err)
        return []
    }
}
