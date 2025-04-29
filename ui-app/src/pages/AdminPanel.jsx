import { useEffect, useState } from "react";
import {
    Box, Typography, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Paper, Button, CircularProgress, Alert
} from "@mui/material";
import { useNavigate, Link } from "react-router-dom";
import { fetchWithRefresh } from "../utils/fetchWithRefresh";

const AdminPanel = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const fetchUsers = async () => {
        setLoading(true);
        setError(null);

        try {
            const usersData = await fetchWithRefresh("http://127.0.0.1:8000/api/users/");
            setUsers(usersData);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        const isSuperuser = sessionStorage.getItem("is_superuser");

        if (!token || isSuperuser !== "True") {
            navigate("/");
            return;
        }

        fetchUsers();
    }, [navigate]);

    return (
        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw", textAlign: "center", padding: "20px", bgcolor: "#30d1f6" }}>
            <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", maxWidth: "900px", width: "100%", bgcolor: "#1976d2" }}>
                <Paper sx={{ padding: "40px", width: "100%", maxWidth: "700px", textAlign: "center" }}>
                    <Typography variant="h4" gutterBottom>
                        Panel Administratora
                    </Typography>

                    {loading && <CircularProgress />}
                    {error && <Alert severity="error">{error}</Alert>}

                    {/* Tabela użytkowników */}
                    {!loading && !error && (
                        <Box sx={{ display: "flex", justifyContent: "center", width: "100%" }}>
                            <TableContainer component={Paper} sx={{ width: "100%", maxWidth: "700px" }}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell align="center" sx={{ maxWidth: "150px", width: "150px" }}><strong>Login</strong></TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {users.map((user) => (
                                            <TableRow key={user.id}>
                                                <TableCell align="center" sx={{ maxWidth: "150px", width: "150px" }}>
                                                    <Link to={`/users/${user.id}`} style={{ textDecoration: "none" }}>
                                                        <Typography variant="body1" sx={{ color: "#007bff", cursor: "pointer", fontWeight: "bold" }}>
                                                            {user.login}
                                                        </Typography>
                                                    </Link>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </Box>
                    )}

                    <Button variant="contained" sx={{ mt: 3 }} onClick={() => navigate("/")}>
                        Wróć do strony głównej
                    </Button>
                </Paper>
            </Box>
        </Box>
    );
}

export default AdminPanel;
