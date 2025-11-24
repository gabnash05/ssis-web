import { apiClient } from "./index";
import type { Student, Paginated } from "../types";

export async function listStudents(params: Record<string, any>): Promise<Paginated<Student>> {
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

export async function getPhotoUploadUrl(id_number: string, filename: string, content_type: string) {
    const { data } = await apiClient.post(`/students/${id_number}/avatar/photo-upload-url`, {
        filename,
        content_type,
    });

    return data;
}

export async function confirmAvatarUpload(id_number: string, avatar_path: string) {
    const { data } = await apiClient.post(`/students/${id_number}/avatar/confirm`, {
        avatar_path,
    });

    return data.data;
}

export async function getAvatarUrl(id_number: string) {
    const { data } = await apiClient.get(`/students/${id_number}/avatar/url`);
    return data.data.avatar_url;
}

export async function deleteAvatar(id_number: string) {
    const { data } = await apiClient.delete(`/students/${id_number}/avatar`);
    return data;
}