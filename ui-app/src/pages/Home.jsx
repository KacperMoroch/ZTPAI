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
import Loading from "../components/Loading";
import ErrorComponent from "../components/Error";
import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import { isLoggedIn, logout } from "../utils/auth";

const Home = () => {
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const fetchData = async () => {
        setLoading(true);
        setError(null);

        try {
            const playersData = await fetchWithRefresh("http://127.0.0.1:8000/api/players/");
            setPlayers(playersData);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };


    useEffect(() => {
        if (!isLoggedIn()) {
            navigate("/login");
            return;
        }

        fetchData();
    }, [navigate]);

    if (loading) return <Loading />;
    if (error) return <ErrorComponent message={error} />;

    return (
        <>
            {/* Navbar */}
            <AppBar position="static" sx={{ bgcolor: "#1976d2", marginBottom: 0 }}>
                <Toolbar sx={{ justifyContent: "space-between" }}>
                    <Typography variant="h6" component="div" sx={{ fontWeight: "bold" }}>
                        GOALDLE
                    </Typography>
                    <Box sx={{ display: "flex", alignItems: "center", ml: 0, justifyContent: "flex-start" }}>
                        <Button
                            color="inherit"
                            component={Link}
                            to="/login"
                            sx={{
                                ml: 1,
                                '&:hover': {
                                    backgroundColor: '#1565c0',
                                    color: '#fff',
                                },
                            }}
                        >
                            Logowanie
                        </Button>
                        <Button
                            color="inherit"
                            component={Link}
                            to="/register"
                            sx={{
                                ml: 2,
                                '&:hover': {
                                    backgroundColor: '#1565c0',
                                    color: '#fff',
                                },
                            }}
                        >
                            Rejestracja
                        </Button>
                        <Button
                            color="inherit"
                            component={Link}
                            to="/profile"
                            sx={{
                                ml: 2,
                                '&:hover': {
                                    backgroundColor: '#1565c0',
                                    color: '#fff',
                                },
                            }}
                        >
                            Twój profil
                        </Button>

                        {/* Panel administratora – widoczny tylko dla superusera */}
                        {sessionStorage.getItem("is_superuser") === "True" && (
                            <Button
                                color="inherit"
                                component={Link}
                                to="/admin"
                                sx={{
                                    ml: 2,
                                    '&:hover': {
                                        backgroundColor: '#1565c0',
                                        color: '#fff',
                                    },
                                }}
                            >
                                Panel administratora
                            </Button>
                        )}

                        <Button
                            color="inherit"
                            component={Link}
                            to="/settings"
                            sx={{
                                ml: 2,
                                '&:hover': {
                                    backgroundColor: '#1565c0',
                                    color: '#fff',
                                },
                            }}
                        >
                            Ustawienia
                        </Button>
                        <Button
                            color="inherit"
                            onClick={logout}
                            sx={{
                                ml: 2,
                                mr: 6,
                                '&:hover': {
                                    backgroundColor: '#1565c0',
                                    color: '#fff',
                                },
                            }}
                        >
                            Wyloguj się
                        </Button>
                    </Box>
                </Toolbar>
            </AppBar>

            <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw", textAlign: "center", padding: "20px", bgcolor: "#30d1f6" }}>
                <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", maxWidth: "900px", width: "100%" }}>
                    {/* Sekcja ładowania i błędów */}
                    {loading && <CircularProgress />}
                    {error && <Alert severity="error">{error}</Alert>}

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