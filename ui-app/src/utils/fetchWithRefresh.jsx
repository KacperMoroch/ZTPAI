// Importowanie funkcji do odświeżania tokenu i wylogowywania użytkownika
import { refreshAccessToken, logout } from "./auth";

// Funkcja fetchWithRefresh umożliwia wykonanie zapytania fetch z automatycznym odświeżeniem tokenu, jeśli wygasł
export const fetchWithRefresh = async (url, options = {}) => {
    // Pobranie aktualnego tokenu z sessionStorage
    const token = sessionStorage.getItem("token");

    // Jeśli token nie istnieje – wyloguj użytkownika i zakończ funkcję
    if (!token) {
        logout();
        throw new Error("Sesja wygasła...");
    }

    // Przygotowanie nagłówków z aktualnym tokenem
    const headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
    };

    try {
        // Wysłanie żądania fetch z bieżącym tokenem
        let response = await fetch(url, { ...options, headers });

        // Jeśli odpowiedź to 401 Unauthorized – spróbuj odświeżyć token
        if (response.status === 401) {
            const newToken = await refreshAccessToken(); // próba odświeżenia tokenu
            if (!newToken) {
                logout();
                throw new Error("Sesja wygasła...");
            }// jeśli odświeżenie się nie powiedzie – zakończ

            // Przygotowanie nagłówków z nowym tokenem
            const retryHeaders = {
                ...options.headers,
                Authorization: `Bearer ${newToken}`,
            };

            // Powtórzenie zapytania z nowym tokenem
            response = await fetch(url, { ...options, headers: retryHeaders });
        }


        // Parsowanie odpowiedzi do formatu JSON
        const data = await response.json();
        return data;
    } catch (err) {
        // Wyrzucenie błędu do obsługi przez wywołujący kod
        throw err;
    }
};
