import { refreshAccessToken, logout } from "./auth";

export const fetchWithRefresh = async (url, options = {}) => {
    const token = sessionStorage.getItem("token");
    if (!token) {
        logout();
        return null;
    }

    const headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
    };

    try {
        let response = await fetch(url, { ...options, headers });

        if (response.status === 401) {
            const newToken = await refreshAccessToken();
            if (!newToken) return null;

            // Spróbuj ponownie z nowym tokenem
            const retryHeaders = {
                ...options.headers,
                Authorization: `Bearer ${newToken}`,
            };
            response = await fetch(url, { ...options, headers: retryHeaders });
        }

        if (!response.ok) {
            throw new Error("Błąd pobierania danych!");
        }

        const data = await response.json();
        return data;
    } catch (err) {
        throw err;
    }
};
