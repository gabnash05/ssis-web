// Main Types
export interface Student {
    id_number: string;      //YYYY-NNNN
    first_name: string;
    last_name: string;
    year_level: number;
    gender: Gender;
    program_code: string;   //FK to Program.program_code
}

export interface Program {
    program_code: string;   //e.g., "BSCS"
    program_name: string;   //e.g., "Bachelor of Science in Computer Science"
    college_code: string;   //FK to College.college_code
}

export interface College {
    college_code: string;   //e.g., "COE"
    college_name: string;   //e.g., "College of Engineering"
}

// Auxiliary Types
export interface Paginated<T> {
    items: T[];
    meta: {
        page: number;
        per_page: number;
        total: number;
    };
}

export interface QueryParams {
    page?: number;
    per_page?: number;
    sort_by?: keyof Student | keyof Program | keyof College;
    sort_order?: SortOrder;
    filter?: Partial<Record<keyof Student | keyof Program | keyof College, string | number>>;
    query?: string;
}

// Utility Types
export type SortOrder = "ASC" | "DESC";
export type Gender = "MALE" | "FEMALE" | "OTHER";

export type ApplicationPage = "STUDENTS" | "PROGRAMS" | "COLLEGES";