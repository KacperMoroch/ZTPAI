import { useEffect, useState } from "react";
import {
    Box, Typography, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Paper, Button, CircularProgress, Alert
} from "@mui/material";
import { useNavigate, Link } from "react-router-dom";
import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import Navbar from "../components/Navbar";

const AdminPanel = () => {
    // Stan na listę użytkowników, stan ładowania oraz błąd
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [deletingId, setDeletingId] = useState(null); // do pokazywania loadera na usuwanym użytkowniku
    // Hook do nawigacji
    const navigate = useNavigate();

    // Funkcja pobierająca użytkowników z API
    const fetchUsers = async () => {
        setLoading(true);
        setError(null);
        try {
            const usersData = await fetchWithRefresh("http://127.0.0.1:8000/api/users/");
            setUsers(usersData);
        } catch (err) {
            // Obsługa błędu
            setError(err.message);
        } finally {
            // Wyłączenie stanu ładowania
            setLoading(false);
        }
    };

    // Hook useEffect uruchamiający się po załadowaniu komponentu
    useEffect(() => {
        // Sprawdzanie, czy użytkownik jest zalogowany i czy jest superużytkownikiem
        const token = sessionStorage.getItem("token");
        const isSuperuser = sessionStorage.getItem("is_superuser");

        // Jeśli nie ma tokena lub użytkownik nie jest superużytkownikiem, przekieruj na stronę główną
        if (!token || isSuperuser !== "True") {
            navigate("/");
            return;
        }

        // Pobieranie użytkowników
        fetchUsers();
    }, [navigate]);

    // funkcja usuwająca użytkownika
    const handleDeleteUser = async (userId) => {
        if (!window.confirm("Czy na pewno chcesz usunąć tego użytkownika?")) return;

        setDeletingId(userId);
        setError(null);

        try {
            const response = await fetchWithRefresh(`http://127.0.0.1:8000/api/users/${userId}/`, {
                method: 'DELETE'
            });

            if (!response.success) {
                throw new Error("Usunięcie nie powiodło się.");
            }

            setUsers(users.filter(user => user.id !== userId));
        } catch (err) {
            setError(`Błąd usuwania użytkownika: ${err.message}`);
        }
    };

    return (
        <>
            <Navbar />
            <Box
                sx={{
                    pt: "64px",
                    bgcolor: "#30d1f6",
                    minHeight: "100vh",
                    width: "100vw",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "flex-start",
                    padding: "20px",
                }}
            >
                <Box
                    sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        maxWidth: "800px",
                        width: "100%",
                        bgcolor: "#1976d2",
                        borderRadius: "12px",
                        overflow: "hidden",
                        boxShadow: 3,
                        minHeight: "300px",
                        mt: 4,
                    }}
                >
                    <Paper
                        sx={{
                            padding: "30px",
                            width: "100%",
                            maxWidth: "600px",
                            minHeight: "300px",
                            textAlign: "center",
                            borderRadius: "12px",
                        }}
                    >
                        <Typography variant="h4" gutterBottom>
                            Panel Administratora
                        </Typography>

                        {loading && <CircularProgress size={30} />}
                        {error && <Alert severity="error">{error}</Alert>}

                        {!loading && !error && (
                            <Box sx={{ display: "flex", justifyContent: "center", width: "100%" }}>
                                <TableContainer component={Paper} sx={{ width: "100%", maxWidth: "500px" }}>
                                    <Table size="medium">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell align="center" sx={{ fontSize: "1rem" }}><strong>Login</strong></TableCell>
                                                <TableCell align="center" sx={{ fontSize: "1rem" }}><strong>Akcje</strong></TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {users.map((user) => (
                                                <TableRow key={user.id}>
                                                    <TableCell align="center" sx={{ fontSize: "1rem" }}>
                                                        <Link to={`/users/${user.id}`} style={{ textDecoration: "none" }}>
                                                            <Typography
                                                                variant="body2"
                                                                sx={{ color: "#007bff", cursor: "pointer", fontWeight: "bold" }}
                                                            >
                                                                {user.login}
                                                            </Typography>
                                                        </Link>
                                                    </TableCell>
                                                    <TableCell align="center">
                                                        <Button
                                                            variant="contained"
                                                            color="error"
                                                            size="small"
                                                            disabled={deletingId === user.id}
                                                            onClick={() => handleDeleteUser(user.id)}
                                                        >
                                                            {deletingId === user.id ? <CircularProgress size={20} color="inherit" /> : 'Usuń'}
                                                        </Button>
                                                    </TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Box>
                        )}

                        <Button variant="contained" sx={{ mt: 2, fontSize: "1rem", padding: "6px 12px" }} onClick={() => navigate("/")}>
                            Wróć do strony głównej
                        </Button>
                    </Paper>
                </Box>
            </Box>
        </>
    );
};

export default AdminPanel;
