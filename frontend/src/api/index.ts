import axios from "axios";
import Cookies from "js-cookie";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const apiClient = axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
});

apiClient.interceptors.request.use(config => {
    const csrfToken = Cookies.get("csrf_access_token");
    if (csrfToken) {
        config.headers["X-CSRF-TOKEN"] = csrfToken;
    }
    return config;
});