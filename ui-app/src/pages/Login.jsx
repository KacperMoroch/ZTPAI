import React, { useState } from "react";
import axios from "axios";
import { Box, Button, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import backgroundImage from '../assets/tlo_login.jpg';

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/login/", { email, password });
            const { access, refresh, is_superuser, message } = response.data;

            if (access) {
                sessionStorage.setItem("token", access);
                sessionStorage.setItem("refresh", refresh);
                sessionStorage.setItem("is_superuser", is_superuser);
                console.log(message || "Zalogowano pomyślnie.");
                navigate("/");
            } else {
                setError("Błąd: brak tokena w odpowiedzi");
            }
        } catch (error) {
            if (error.response) {
                setError(error.response.data.error || "Nieprawidłowe dane logowania!");
            } else {
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
                        width: "50%",
                        padding: "15px",
                    },
                    "@media (max-width: 480px)": {
                        width: "100%",
                    }
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
