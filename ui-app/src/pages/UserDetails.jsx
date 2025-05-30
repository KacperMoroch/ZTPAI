import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
    Typography,
    Box,
    Paper,
    Button,
} from "@mui/material";
import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import Loading from "../components/Loading";
import ErrorComponent from "../components/Error";
import Navbar from "../components/Navbar";

const UserDetails = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        const isSuperuser = sessionStorage.getItem("is_superuser");

        if (!token || isSuperuser !== "True") {
            navigate("/");
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
                            textAlign: "center",
                            borderRadius: "12px",
                            minHeight: "300px",
                        }}
                    >
                        <Typography variant="h3" sx={{ marginBottom: "20px", color: "black" }}>
                            Szczegóły użytkownika
                        </Typography>

                        <Typography variant="body1" sx={{ marginBottom: "12px", fontSize: "20px", color: "black" }}>
                            <strong>ID:</strong> {user.id}
                        </Typography>
                        <Typography variant="body1" sx={{ marginBottom: "12px", fontSize: "20px", color: "black" }}>
                            <strong>Login:</strong> {user.login}
                        </Typography>
                        <Typography variant="body1" sx={{ marginBottom: "12px", fontSize: "20px", color: "black" }}>
                            <strong>Email:</strong> {user.email}
                        </Typography>
                        <Typography variant="body1" sx={{ marginBottom: "20px", fontSize: "20px", color: "black" }}>
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
        </>
    );
};

export default UserDetails;
