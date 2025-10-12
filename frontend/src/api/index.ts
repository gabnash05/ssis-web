import axios, { AxiosError } from "axios";
import Cookies from "js-cookie";

const BASE_URL = "http://127.0.0.1:5000/api"

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

// Response interceptor to handle backend error format
apiClient.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        if (error.response?.data && typeof error.response.data === 'object') {
            const backendError = error.response.data as any;
            
            if ((backendError.status && backendError.status === "error") || ('success' in backendError && !backendError.success)) {
                const customError = new Error(backendError.message || 'An error occurred');
                (customError as any).response = {
                    ...error.response,
                    data: backendError
                };
                return Promise.reject(customError);
            }
        }
        
        return Promise.reject(error);
    }
);