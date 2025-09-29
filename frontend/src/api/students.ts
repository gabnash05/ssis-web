import { apiClient } from "./index";
import type { Student, Paginated } from "../types";

export async function listStudents(params: Record<string, any>) {
    const { data } = await apiClient.get("/students", { params });
    return data as Paginated<Student>;
}

export async function getStudent(id_number: string) {
    const { data } = await apiClient.get(`/students/${id_number}`);
    return data.data as Student;
}

export async function createStudent(student: Student) {
    return apiClient.post("/students", student);
}

export async function updateStudent(id_number: string, updates: Partial<Student>) {
    return apiClient.put(`/students/${id_number}`, updates);
}

export async function deleteStudent(id_number: string) {
    return apiClient.delete(`/students/${id_number}`);
}
