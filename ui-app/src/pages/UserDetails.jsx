import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Paper,
    CircularProgress,
    Alert,
    Button,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import { isLoggedIn } from "../utils/auth";
import Loading from "../components/Loading";
import ErrorComponent from "../components/Error";

const UserDetails = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Sprawdzenie, czy użytkownik jest zalogowany i czy jest superużytkownikiem
        const token = sessionStorage.getItem("token");
        const isSuperuser = sessionStorage.getItem("is_superuser");

        if (!token || isSuperuser !== "True") {
            navigate("/");  // Przekierowanie, jeśli nie jest superużytkownikiem
            return;
        }

        const fetchUserData = async () => {
            setLoading(true);
            setError(null);

            try {
                const userData = await fetchWithRefresh(`http://127.0.0.1:8000/api/users/${id}/`);
                setUser(userData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, [id, navigate]);

    if (loading) return <Loading />;
    if (error) return <ErrorComponent message={error} />;

    return (
        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw", textAlign: "center", padding: "20px", marginTop: "-50px", bgcolor: "#30d1f6" }}>
            <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", maxWidth: "900px", width: "100%", bgcolor: "#1976d2" }}>
                <Paper sx={{ padding: "40px", width: "100%", maxWidth: "700px", textAlign: "center" }}>
                    <Typography variant="h3" sx={{ marginBottom: "20px" }}>
                        Szczegóły użytkownika
                    </Typography>

                    <Typography variant="body1" sx={{ marginBottom: "12px", fontSize: "20px" }}>
                        <strong>ID:</strong> {user.id}
                    </Typography>
                    <Typography variant="body1" sx={{ marginBottom: "12px", fontSize: "20px" }}>
                        <strong>Login:</strong> {user.login}
                    </Typography>
                    <Typography variant="body1" sx={{ marginBottom: "12px", fontSize: "20px" }}>
                        <strong>Email:</strong> {user.email}
                    </Typography>
                    <Typography variant="body1" sx={{ marginBottom: "20px", fontSize: "20px" }}>
                        <strong>Admin:</strong> {user.is_superuser ? "Tak" : "Nie"}
                    </Typography>

                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => navigate("/admin")}
                    >
                        Wróć do Panelu Administratora
                    </Button>
                </Paper>
            </Box>
        </Box>
    );
};

export default UserDetails;
