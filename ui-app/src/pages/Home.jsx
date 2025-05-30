import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress,
    Alert,
    Box,
    Button,
} from "@mui/material";

import Navbar from "../components/Navbar";
// Komponenty do ładowania i obsługi błędów
import Loading from "../components/Loading";
import ErrorComponent from "../components/Error";

// Pomocnicze funkcje do uwierzytelniania i odświeżania tokena
import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import { isLoggedIn } from "../utils/auth";

const Home = () => {
    // Stan na dane piłkarzy, status ładowania i ewentualny błąd
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Hook nawigacyjny
    const navigate = useNavigate();

    // Funkcja pobierająca dane piłkarzy z API
    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            // Pobieranie danych z API z użyciem funkcji obsługującej odświeżanie tokena
            const playersData = await fetchWithRefresh("http://127.0.0.1:8000/api/players/");
            setPlayers(playersData);
        } catch (err) {
            // Obsługa błędu podczas pobierania
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // Hook uruchamiany po załadowaniu komponentu
    useEffect(() => {
        // Sprawdzenie, czy użytkownik jest zalogowany — jeśli nie, przekierowanie do logowania
        if (!isLoggedIn()) {
            navigate("/login");
            return;
        }

        // Pobieranie danych
        fetchData();
    }, [navigate]);

    // Jeżeli trwa ładowanie – pokaż komponent ładowania
    if (loading) return <Loading />;

    // Jeżeli wystąpił błąd – pokaż komponent błędu
    if (error) return <ErrorComponent message={error} />;

    return (
        <>
            {/* Navbar */}
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
                        maxWidth: "900px",
                        width: "100%",
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        bgcolor: "#fff",
                        borderRadius: 2,
                        padding: 3,
                        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                        mt: 4,
                    }}
                >
                    <Button
                        variant="contained"
                        component={Link}
                        to="/guess_player"
                        sx={{
                            marginBottom: 2,
                            color: "#fff",
                            width: "250px",
                            height: "50px",
                            fontSize: "1.2rem",
                            backgroundColor: "#6a1b9a",
                            '&:hover': {
                                backgroundColor: '#4a148c',
                                color: '#fff',
                            },
                        }}
                    >
                        Zgadnij piłkarza
                    </Button>

                    <Button
                        variant="contained"
                        component={Link}
                        to="/guess_transfer"
                        sx={{
                            marginBottom: 2,
                            color: "#fff",
                            width: "250px",
                            height: "50px",
                            fontSize: "1.2rem",
                            backgroundColor: "#2e7d32",
                            '&:hover': {
                                backgroundColor: '#1b5e20',
                                color: '#fff',
                            },
                        }}
                    >
                        Zgadnij transfer
                    </Button>


                    <Box
                        sx={{
                            width: "100%",
                            backgroundColor: "#e3f2fd",
                            padding: 3,
                            borderRadius: 2,
                            boxShadow: "0 2px 6px rgba(0, 0, 0, 0.1)",
                            mt: 4,

                        }}
                    >
                        <Box
                            sx={{
                                display: "flex",
                                flexDirection: "column",
                                alignItems: "center",
                                justifyContent: "center",
                                marginBottom: 3,
                            }}
                        >
                            <Typography variant="h5" sx={{ marginBottom: 2, color: "black" }}>
                                Lista piłkarzy
                            </Typography>

                            <Button
                                variant="contained"
                                color="primary"
                                onClick={() => fetchData(sessionStorage.getItem("token"))}
                            >
                                Odśwież dane
                            </Button>
                        </Box>

                        <TableContainer
                            component={Paper}
                            sx={{
                                backgroundColor: "#ffffff",
                                borderRadius: 4,
                                boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)",
                            }}
                        >
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell align="center"><strong>Imię</strong></TableCell>
                                        <TableCell align="center"><strong>Klub</strong></TableCell>
                                        <TableCell align="center"><strong>Liga</strong></TableCell>
                                        <TableCell align="center"><strong>Kraj</strong></TableCell>
                                        <TableCell align="center"><strong>Pozycja</strong></TableCell>
                                        <TableCell align="center"><strong>Wiek</strong></TableCell>
                                        <TableCell align="center"><strong>Numer</strong></TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {players.map((player, index) => (
                                        <TableRow
                                            key={player.id}
                                            sx={{
                                                backgroundColor: index % 2 === 0 ? "#f5f5f5" : "#ffffff",
                                            }}
                                        >
                                            <TableCell align="center">{player.name}</TableCell>
                                            <TableCell align="center">{player.club_name}</TableCell>
                                            <TableCell align="center">{player.league_name}</TableCell>
                                            <TableCell align="center">{player.country_name}</TableCell>
                                            <TableCell align="center">{player.position_name}</TableCell>
                                            <TableCell align="center">{player.age_value}</TableCell>
                                            <TableCell align="center">{player.shirt_number_value}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </Box>


                </Box>
            </Box >
        </>
    );
};

export default Home;
