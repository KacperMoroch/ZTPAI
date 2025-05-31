import React, { useState } from "react";
import axios from "axios";
import { Box, Button, Typography, TextField } from "@mui/material";
import { useNavigate } from "react-router-dom";
import backgroundImage from '../assets/tlo_register.jpg';
import mobileBackgroundImage from '../assets/mobile_registration.jpg';

const Register = () => {
    // Stany do przechowywania danych z formularza rejestracji
    const [email, setEmail] = useState("");
    const [login, setLogin] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate(); // Hook do nawigacji po stronie

    // Funkcja obsługująca wysłanie formularza rejestracyjnego
    const handleSubmit = async (e) => {
        e.preventDefault(); // Zapobiega przeładowaniu strony

        // Sprawdzenie, czy hasła są identyczne
        if (password !== confirmPassword) {
            setError("Hasła nie są takie same!");
            return;
        }

        // Dane użytkownika do wysłania na backend
        const userData = { email, login, password };

        try {
            // Wysłanie danych do API rejestracji
            const response = await axios.post("http://127.0.0.1:8000/api/register/", userData);
            console.log("Rejestracja udana:", response.data);
            navigate("/login"); // Przekierowanie do strony logowania po sukcesie
        } catch (error) {
            // Obsługa błędów odpowiedzi z serwera
            if (error.response) {
                setError(error.response.data.error || "Wystąpił błąd podczas rejestracji!");
            } else {
                // Obsługa błędów połączenia
                setError("Błąd połączenia z serwerem!");
            }
        }
    };


    return (
        <Box
            key="register-page"
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
                    marginTop: "8%",
                    "@media (max-width: 852px)": {
                        width: "50%",
                        padding: "20px",
                    },
                    "@media (max-width: 852px) and (max-height: 500px)": {
                        width: "100%",
                        padding: "10px",
                        transform: "scale(0.55)",
                    },
                    "@media (max-width: 480px)": {
                        width: "100%",
                    },
                }}
            >
                <Typography
                    variant="h3"
                    component="h1"
                    gutterBottom
                    sx={{ fontSize: "2.25rem", mt: 4, mb: 0.8, color: "white" }}
                >
                    ZAREJESTRUJ SIĘ
                </Typography>

                {error && <Typography sx={{ color: "red", fontSize: "1.1rem", mt: 0 }}>{error}</Typography>}

                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Adres e-mail"
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
                        label="Login"
                        variant="outlined"
                        fullWidth
                        required
                        value={login}
                        onChange={(e) => setLogin(e.target.value)}
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
                    <TextField
                        label="Powtórz hasło"
                        variant="outlined"
                        type="password"
                        fullWidth
                        required
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
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
                            p: 2,
                            fontSize: "1.08rem",
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
                </form>

                <Typography sx={{ color: "white", mt: 1.9, fontSize: "0.9rem" }}>Masz już konto? Zaloguj się!</Typography>

                <Button
                    fullWidth
                    onClick={() => navigate("/login")}
                    sx={{
                        p: 2,
                        fontSize: "1.08rem",
                        mt: 0.5,
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
            </Box>
        </Box>
    );
};

export default Register;
