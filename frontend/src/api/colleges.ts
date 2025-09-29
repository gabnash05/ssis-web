import { apiClient } from "./index";
import type { College, Paginated } from "../types";

export async function listColleges(params: Record<string, any>): Promise<Paginated<College>> {
    const { data } = await apiClient.get("/colleges", { params });
    return data as Paginated<College>;
}

export async function createCollege(college: College) {
    return apiClient.post("/colleges", college);
}

export async function updateCollege(college_code: string, updates: Partial<College>) {
    return apiClient.put(`/colleges/${college_code}`, updates);
}

export async function deleteCollege(college_code: string) {
    return apiClient.delete(`/colleges/${college_code}`);
}
