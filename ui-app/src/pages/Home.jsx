import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import {
    AppBar,
    Toolbar,
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
import { isLoggedIn, logout } from "../utils/auth";

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

            <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw", textAlign: "center", padding: "20px", bgcolor: "#30d1f6" }}>
                <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", maxWidth: "900px", width: "100%" }}>
                    {/* Sekcja ładowania i błędów */}
                    {loading && <CircularProgress />}
                    {error && <Alert severity="error">{error}</Alert>}
                    <Button
                        variant="contained"
                        color="secondary"
                        component={Link}
                        to="/guess_player"
                        sx={{ marginBottom: 2 }}
                    >
                        Zgadnij piłkarza
                    </Button>
                    {/* Przycisk odświeżania */}
                    <Button
                        variant="contained"
                        color="primary"
                        sx={{ marginBottom: 2 }}
                        onClick={() => fetchData(sessionStorage.getItem("token"))}
                    >
                        Odśwież dane
                    </Button>



                    {/* Tabela piłkarzy */}
                    <Typography variant="h5" sx={{ marginBottom: 2, marginTop: 4, color: "black" }}>Lista piłkarzy</Typography>
                    <Box sx={{ display: "flex", justifyContent: "center", width: "100%" }}>
                        <TableContainer component={Paper} sx={{ width: "100%" }}>
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
                                    {players.map((player) => (
                                        <TableRow key={player.id}>
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
            </Box>
        </>
    );
};

export default Home;