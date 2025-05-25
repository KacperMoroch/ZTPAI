import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, TextField, Alert } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import { isLoggedIn } from "../utils/auth";

const SettingsPage = () => {
    const [originalUser, setOriginalUser] = useState({ login: '', email: '' });
    const [user, setUser] = useState({ login: '', email: '' });
    const [success, setSuccess] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        if (!isLoggedIn()) {
            navigate("/login");
            return;
        }

        const fetchUserSettings = async () => {
            try {
                const data = await fetchWithRefresh("http://127.0.0.1:8000/api/settings");
                console.log("response from /settings", data);
                if (data?.user) {
                    setUser(data.user);
                    setOriginalUser(data.user);
                }
            } catch (err) {
                console.error("error while fetching settings", err);
                setError("Nie udało się pobrać ustawień użytkownika.");
            }
        };

        fetchUserSettings();
    }, [navigate]);

    const handleChange = (e) => {
        setUser(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const data = await fetchWithRefresh("http://127.0.0.1:8000/api/updateAccount", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(user),
            });

            if (data.success) {
                setSuccess(data.success);
                setError('');

                if (data.user) {
                    setOriginalUser(data.user);
                }
            } else if (data.error) {
                setError(data.error);
                setSuccess('');
            }
        } catch (err) {
            setError("Wystąpił błąd podczas aktualizacji konta.");
            setSuccess('');
        }
    };

    const handleDelete = async () => {
        try {
            await fetchWithRefresh("http://127.0.0.1:8000/api/deleteAccount", {
                method: "POST",
            });
            navigate("/login");
        } catch (err) {
            setError("Nie udało się usunąć konta.");
        }
    };

    return (
        <>
            <Navbar />

            <Box
                sx={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "100vh",
                    width: "100vw",
                    textAlign: "center",
                    padding: "20px",
                    bgcolor: "#30d1f6",
                }}
            >
                <Box
                    sx={{
                        maxWidth: "500px",
                        width: "100%",
                        padding: "40px",
                        backgroundColor: "#fff",
                        borderRadius: "8px",
                        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
                        fontFamily: "Arial, sans-serif",
                        color: "black"
                    }}
                >
                    <Typography variant="h4" gutterBottom sx={{ color: "black" }}>
                        Ustawienia konta
                    </Typography>
                    <Typography variant="subtitle1" gutterBottom sx={{ color: "black" }}>
                        Witaj, {originalUser.login}!
                    </Typography>

                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                    {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

                    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column" }}>
                        <TextField
                            label="Login"
                            name="login"
                            value={user.login}
                            onChange={handleChange}
                            required
                            sx={{ mb: 2, input: { color: "black" }, label: { color: "black" } }}
                        />
                        <TextField
                            label="E-mail"
                            name="email"
                            type="email"
                            value={user.email}
                            onChange={handleChange}
                            required
                            sx={{ mb: 2, input: { color: "black" }, label: { color: "black" } }}
                        />
                        <Button type="submit" variant="contained" color="primary">
                            Zaktualizuj
                        </Button>
                    </form>

                    <Button
                        variant="contained"
                        color="error"
                        onClick={handleDelete}
                        sx={{ mt: 2 }}
                    >
                        Usuń konto
                    </Button>
                </Box>
            </Box>
        </>
    );
};

export default SettingsPage;
