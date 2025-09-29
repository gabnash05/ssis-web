import { apiClient } from "./index";
import type { Program, Paginated } from "../types";

export async function listPrograms(params: Record<string, any>) {
    const { data } = await apiClient.get("/programs", { params });
    return data as Paginated<Program>;
}

export async function createProgram(program: Program) {
    return apiClient.post("/programs", program);
}

export async function updateProgram(program_code: string, updates: Partial<Program>) {
    return apiClient.put(`/programs/${program_code}`, updates);
}

export async function deleteProgram(program_code: string) {
    return apiClient.delete(`/programs/${program_code}`);
}
