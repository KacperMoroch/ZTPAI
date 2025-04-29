import { useNavigate } from "react-router-dom";

export const logout = () => {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("refresh");
    window.location.href = "/login";
};

export const refreshAccessToken = async () => {
    const refreshToken = sessionStorage.getItem("refresh");
    if (!refreshToken) {
        logout();
        return null;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (!response.ok) throw new Error("Nie udało się odświeżyć tokenu");

        const data = await response.json();
        sessionStorage.setItem("token", data.access);
        return data.access;
    } catch (err) {
        console.error(err);
        logout();
        return null;
    }
};

export const isLoggedIn = () => {
    return !!sessionStorage.getItem("token");
};
