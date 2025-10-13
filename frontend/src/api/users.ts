import { apiClient } from "./index";
import type { User, Paginated } from "../types";

export async function listUsers(params: Record<string, any>): Promise<Paginated<User>> {
    const { data } = await apiClient.get("/users", { params });
    return data as Paginated<User>;
}

export async function getUser(user_id: number): Promise<User> {
    const { data } = await apiClient.get(`/users/${user_id}`);
    return data.data as User;
}

export async function createUser(user: User) {
    return apiClient.post("/users", user);
}

export async function updateUser(user_id: number, updates: Partial<User>) {
    return apiClient.put(`/users/${user_id}`, updates);
}

export async function deleteUser(user_id: number) {
    return apiClient.delete(`/users/${user_id}`);
}
