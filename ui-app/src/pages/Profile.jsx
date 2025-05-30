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
    Button,
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
    const [uploading, setUploading] = useState(false);
    const navigate = useNavigate();

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

    useEffect(() => {
        fetchProfile();
    }, []);

    const handleFileChange = async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("image", file);

        setUploading(true);
        try {
            const data = await fetchWithRefresh("http://127.0.0.1:8000/api/profile/upload-picture/", {
                method: "POST",
                body: formData,
            });

            if (data?.success) {
                await fetchProfile();
            } else {
                console.error(data);
                alert("Błąd przy przesyłaniu zdjęcia.");
            }
        } catch (err) {
            console.error(err);
            alert("Błąd sieci przy przesyłaniu zdjęcia.");
        } finally {
            setUploading(false);
        }
    };

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
                                    top: "4px",
                                    left: "1px",
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
                            alignItems: "center",
                            flexDirection: "column",
                            display: "flex",
                            minHeight: "300px",
                            textAlign: "center",
                            borderRadius: "12px",
                        }}
                    >
                        {/* zawartość profilu */}
                        <Typography variant="h4" gutterBottom>
                            Witaj, {profile.login}!
                        </Typography>
                        <Typography variant="subtitle1">
                            Konto założone: {new Date(profile.created_at).toLocaleDateString()}
                        </Typography>

                        <Avatar
                            sx={{ width: 100, height: 100, mb: 2, mt: 1 }}
                            src={
                                profile.profile_picture
                                    ? `data:image/jpeg;base64,${profile.profile_picture}`
                                    : undefined
                            }
                            alt={profile.login}
                        />
                        <Button
                            variant="contained"
                            component="label"
                            disabled={uploading}
                            sx={{ mb: 0.1 }}
                        >
                            {uploading ? "Wysyłanie..." : "Zmień zdjęcie profilowe"}
                            <input
                                hidden
                                accept="image/*"
                                type="file"
                                onChange={handleFileChange}
                            />
                        </Button>

                        <Typography variant="h6" sx={{ mt: 2 }}>
                            Łączna liczba punktów:{" "}
                            <strong style={{ color: "#1976d2" }}>{total_points}</strong>
                        </Typography>
                        <Typography variant="body1">
                            ({points_guess} za <em>Zgadnij piłkarza</em>, {points_transfer} za <em>Zgadnij transfer</em>)
                        </Typography>

                        <Box sx={{ mt: 2, width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
                            <Typography
                                variant="h6"
                                gutterBottom
                                sx={{ textAlign: "center", fontWeight: "bold" }}
                            >
                                Osiągnięcia:
                            </Typography>
                            {renderAchievements()}
                        </Box>
                    </Paper>
                </Box>
            </Box>
        </>
    );
}

export default Profile;
