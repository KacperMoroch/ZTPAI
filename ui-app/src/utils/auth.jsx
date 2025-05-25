import { useNavigate } from "react-router-dom";

// Funkcja wylogowująca użytkownika – usuwa tokeny z sessionStorage i przekierowuje na stronę logowania
export const logout = () => {
    sessionStorage.removeItem("token");   // Usunięcie tokenu dostępu
    sessionStorage.removeItem("refresh"); // Usunięcie tokenu odświeżającego
    window.location.href = "/login";      // Przekierowanie na stronę logowania
};

// Funkcja próbująca odświeżyć token dostępu przy użyciu tokenu odświeżającego
export const refreshAccessToken = async () => {
    const refreshToken = sessionStorage.getItem("refresh"); // Pobranie tokenu odświeżającego

    // Jeśli brak tokenu odświeżającego – wyloguj użytkownika
    if (!refreshToken) {
        logout();
        return null;
    }

    try {
        // Wysłanie żądania POST do endpointa odświeżania tokenu
        const response = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ refresh: refreshToken }), // Przekazanie tokenu odświeżającego w ciele żądania
        });

        // Jeśli odpowiedź jest nieprawidłowa – rzuć błąd
        if (!response.ok) throw new Error("Nie udało się odświeżyć tokenu");

        // Odczytanie nowego tokenu dostępu z odpowiedzi i zapisanie go
        const data = await response.json();
        sessionStorage.setItem("token", data.access); // Zapis nowego tokenu
        return data.access; // Zwrócenie go do dalszego użycia
    } catch (err) {
        console.error(err); // Logowanie błędu
        logout();           // Wylogowanie użytkownika przy błędzie
        return null;
    }
};

// Funkcja sprawdzająca, czy użytkownik jest zalogowany – na podstawie obecności tokenu
export const isLoggedIn = () => {
    return !!sessionStorage.getItem("token"); // Zwraca true, jeśli token istnieje
};
