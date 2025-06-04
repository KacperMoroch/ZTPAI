import React, { useState } from "react";
import axios from "axios";
import { Box, Button, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import backgroundImage from '../assets/tlo_login.jpg';
import mobileBackgroundImage from '../assets/mobile_login.jpg';

const Login = () => {
    // Stany do przechowywania danych formularza logowania
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate(); // Hook do nawigacji

    // Obsługa wysyłania formularza logowania
    const handleSubmit = async (e) => {
        e.preventDefault(); // Zapobiega przeładowaniu strony
        setError(""); // Resetowanie błędu

        try {
            // Wysłanie danych logowania do backendu
            const response = await axios.post("http://127.0.0.1:8000/api/login/", { email, password });

            // Odbiór danych z odpowiedzi
            const { access, refresh, is_superuser, message } = response.data;

            // Jeżeli otrzymano token, zapisujemy dane do sessionStorage i przekierowujemy do strony głównej
            if (access) {
                sessionStorage.setItem("token", access);
                sessionStorage.setItem("refresh", refresh);
                sessionStorage.setItem("is_superuser", is_superuser);
                navigate("/"); // Przejście do strony głównej
            } else {
                // Obsługa przypadku, gdy nie otrzymano tokena
                setError("Błąd: brak tokena w odpowiedzi");
            }
        } catch (error) {
            // Obsługa błędów z serwera (np. błędne dane logowania)
            if (error.response) {
                setError(error.response.data.error || "Nieprawidłowe dane logowania!");
            } else {
                // Obsługa błędów połączenia
                setError("Błąd połączenia z serwerem!");
            }
        }
    };


    return (
        <Box
            sx={{
                position: "fixed",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                backgroundImage: `url(${backgroundImage})`,
                backgroundSize: "cover",
                backgroundRepeat: "no-repeat",
                backgroundAttachment: "fixed",
                "@media (max-width: 600px) and (orientation: portrait)": {
                    backgroundImage: `url(${mobileBackgroundImage})`,
                },
            }}
        >
            <Box
                sx={{
                    textAlign: "center",
                    padding: "40px",
                    width: "90%",
                    maxWidth: "400px",
                    borderRadius: "10px",
                    marginTop: "18%",
                    "@media (max-width: 852px)": {
                        width: "60%",
                        padding: "20px",
                    },
                    "@media (max-width: 852px) and (max-height: 500px)": {
                        width: "80%",
                        padding: "10px",
                        transform: "scale(0.6)",
                    },
                    "@media (max-width: 480px)": {
                        width: "100%",
                    },
                }}
            >
                <Typography
                    variant="h3"
                    component="h1"
                    sx={{ fontSize: "2.5rem", mt: 3.7, mb: 0.5, color: "white" }}
                >
                    ZALOGUJ SIĘ
                </Typography>

                {error && <Typography sx={{ color: "red", fontSize: "1rem", mt: 0.7, mb: 0.8 }}>{error}</Typography>}

                <form onSubmit={handleSubmit}>
                    <TextField
                        label="E-mail"
                        variant="outlined"
                        fullWidth
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        sx={{
                            mb: 2,
                            "& .MuiInputBase-root": { backgroundColor: "rgba(255,255,255,0.2)", color: "white" },
                            "& .MuiInputBase-input": { color: "white" },
                            "& .MuiInputLabel-root": { color: "white" },
                            "& .MuiInputLabel-root.Mui-focused": { color: "white" },
                        }}
                    />
                    <TextField
                        label="Hasło"
                        variant="outlined"
                        type="password"
                        fullWidth
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        sx={{
                            mb: 2,
                            "& .MuiInputBase-root": { backgroundColor: "rgba(255,255,255,0.2)", color: "white" },
                            "& .MuiInputBase-input": { color: "white" },
                            "& .MuiInputLabel-root": { color: "white" },
                            "& .MuiInputLabel-root.Mui-focused": { color: "white" },
                        }}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        sx={{
                            p: 1,
                            fontSize: "1.2rem",
                            bgcolor: "#26d027",
                            color: "white",
                            borderRadius: "10px",
                            cursor: "pointer",
                            transition: "background-color 0.3s ease",
                            "&:hover": { bgcolor: "#228b22" },
                        }}
                    >
                        ZALOGUJ SIĘ
                    </Button>
                </form>

                <Typography sx={{ color: "white", mt: 2 }}>Nie masz jeszcze konta?</Typography>

                <Button
                    fullWidth
                    onClick={() => navigate("/register")}
                    sx={{
                        p: 1,
                        fontSize: "1.2rem",
                        mt: 1,
                        bgcolor: "#26d027",
                        color: "white",
                        borderRadius: "10px",
                        cursor: "pointer",
                        transition: "background-color 0.3s ease",
                        "&:hover": { bgcolor: "#228b22" },
                    }}
                >
                    ZAREJESTRUJ SIĘ
                </Button>
            </Box>
        </Box>
    );
};

export default Login;
