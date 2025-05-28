import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    Box,
    Typography,
    CircularProgress,
    Alert,
    Avatar,
    Tooltip,
    Paper,
} from "@mui/material";
import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import Navbar from "../components/Navbar";

import quest1 from "../assets/quest1.svg";
import quest12 from "../assets/quest12.svg";
import quest123 from "../assets/quest123.svg";
import quest2 from "../assets/quest2.svg";
import quest23 from "../assets/quest23.svg";
import quest234 from "../assets/quest234.svg";

const Profile = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await fetchWithRefresh("http://127.0.0.1:8000/api/profile/");
                setProfile(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, []);

    const points_guess = profile?.points_guess ?? 0;
    const points_transfer = profile?.points_transfer ?? 0;
    const total_points = points_guess + points_transfer;

    const renderAchievements = () => {
        const achievements = [];

        if (points_guess >= 500) achievements.push({ src: quest123, text: "500 pkt – Zgadnij piłkarza" });
        else if (points_guess >= 300) achievements.push({ src: quest12, text: "300 pkt – Zgadnij piłkarza" });
        else if (points_guess >= 100) achievements.push({ src: quest1, text: "100 pkt – Zgadnij piłkarza" });

        if (points_transfer >= 500) achievements.push({ src: quest234, text: "500 pkt – Zgadnij transfer" });
        else if (points_transfer >= 300) achievements.push({ src: quest23, text: "300 pkt – Zgadnij transfer" });
        else if (points_transfer >= 100) achievements.push({ src: quest2, text: "100 pkt – Zgadnij transfer" });

        if (achievements.length === 0) {
            return <Typography sx={{ mt: 2 }}>Brak osiągnięć!</Typography>;
        }

        return (
            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    flexWrap: "wrap",
                    justifyContent: "center",
                    mt: 2,
                }}
            >
                {achievements.map((a, index) => (
                    <Tooltip key={index} title={a.text}>
                        <Box
                            sx={{
                                width: 86,
                                height: 86,
                                backgroundColor: "white",
                                boxShadow: "0 3px 8px rgba(0,0,0,0.2)",
                                borderRadius: "50%",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                            }}
                        >
                            <img
                                src={a.src}
                                alt="achievement"
                                style={{
                                    width: "56px",
                                    height: "56px",
                                    position: "relative",
                                    top: "5.7px",
                                    left: "1.5px",
                                }}
                            />
                        </Box>


                    </Tooltip>
                ))}
            </Box>
        );
    };

    if (loading) {
        return (
            <>
                <Navbar />
                <Box
                    sx={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        minHeight: "100vh",
                        bgcolor: "#30d1f6",
                    }}
                >
                    <CircularProgress />
                </Box>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Navbar />
                <Box
                    sx={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        minHeight: "100vh",
                        bgcolor: "#30d1f6",
                    }}
                >
                    <Alert severity="error">{error}</Alert>
                </Box>
            </>
        );
    }

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
                <Paper
                    elevation={6}
                    sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        maxWidth: "800px",
                        width: "100%",
                        padding: 4,
                        borderRadius: 4,
                        backgroundColor: "white",
                    }}
                >
                    <Typography variant="h4" gutterBottom>
                        Witaj, {profile.login}!
                    </Typography>
                    <Typography variant="subtitle1">
                        Konto założone: {new Date(profile.created_at).toLocaleDateString()}
                    </Typography>
                    <Typography variant="h6" sx={{ mt: 3 }}>
                        Łączna liczba punktów:{" "}
                        <strong style={{ color: "#1976d2" }}>{total_points}</strong>
                    </Typography>
                    <Typography variant="body1">
                        ({points_guess} za <em>Zgadnij piłkarza</em>, {points_transfer} za <em>Zgadnij transfer</em>)
                    </Typography>

                    <Box sx={{ mt: 4, width: "100%" }}>
                        <Typography variant="h6" gutterBottom>
                            Osiągnięcia:
                        </Typography>
                        {renderAchievements()}
                    </Box>
                </Paper>
            </Box>
        </>
    );
};

export default Profile;
