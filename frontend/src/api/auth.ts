import { apiClient } from "./index";

export async function signup(username: string, email: string, password: string) {
    return apiClient.post("/auth/signup", { username, email, password });
}

export async function login(email: string, password: string) {
    return apiClient.post("/auth/login", { email, password });
}

export async function logout() {
    return apiClient.post("/auth/logout");
}

export async function getCurrentUser() {
    return apiClient.get("/auth/me");
}

export async function updateUser(data: { username?: string; password?: string }) {
    return apiClient.put("/auth/update", data);
}
