import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { CircularProgress, Alert, Box, Typography, Paper } from "@mui/material";

const UserDetails = () => {
    const { id } = useParams();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/users/${id}/`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Nie znaleziono użytkownika!");
                }
                return res.json();
            })
            .then((data) => {
                setUser(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [id]);

    if (loading) return (
        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw" }}>
            <CircularProgress />
        </Box>
    );

    if (error) return (
        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw" }}>
            <Alert severity="error">{error}</Alert>
        </Box>
    );

    return (
        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw", textAlign: "center", padding: "20px", marginTop: "-50px" }}>
            <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", maxWidth: "900px", width: "100%" }}>
                <Paper sx={{ padding: "40px", width: "100%", maxWidth: "700px", textAlign: "center" }}>
                    <Typography variant="h3" sx={{ marginBottom: "20px" }}>
                        Szczegóły użytkownika
                    </Typography>
                    <Typography variant="body1" sx={{ marginBottom: "12px", fontSize: "20px" }}>
                        <strong>Login:</strong> {user.login}
                    </Typography>
                    <Typography variant="body1" sx={{ fontSize: "20px" }}>
                        <strong>Email:</strong> {user.email}
                    </Typography>
                </Paper>
            </Box>
        </Box>
    );
};

export default UserDetails;
