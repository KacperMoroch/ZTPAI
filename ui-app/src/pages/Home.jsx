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
    Box,
    Button,
    TextField,
    MenuItem
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

    // stany do paginacji
    const [page, setPage] = useState(1);
    const [count, setCount] = useState(0);
    const [next, setNext] = useState(null);
    const [previous, setPrevious] = useState(null);

    const [country, setCountry] = useState("");
    const [league, setLeague] = useState("");
    const [position, setPosition] = useState("");
    const [sort, setSort] = useState("name");

    const [availableCountries, setAvailableCountries] = useState([]);
    const [availableLeagues, setAvailableLeagues] = useState([]);
    const [availablePositions, setAvailablePositions] = useState([]);

    // Hook nawigacyjny
    const navigate = useNavigate();

    const fetchFilters = async () => {
        try {
            const data = await fetchWithRefresh("http://127.0.0.1:8000/api/filters/");
            setAvailableCountries([...data.countries].sort());
            setAvailableLeagues([...data.leagues].sort());
            setAvailablePositions([...data.positions].sort());
        } catch (err) {
            console.error("Błąd podczas pobierania filtrów:", err);
        }
    };

    // Funkcja pobierająca dane piłkarzy z API
    const fetchData = async (pageNumber = 1) => {
        setLoading(true);
        setError(null);
        try {
            const params = new URLSearchParams({
                page: pageNumber.toString(),
                country,
                league,
                position,
                sort,
            });

            const url = `http://127.0.0.1:8000/api/players/?${params.toString()}`;
            const data = await fetchWithRefresh(url);
            setPlayers(data.results);
            setCount(data.count);
            setNext(data.next);
            setPrevious(data.previous);
            setPage(pageNumber);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    const resetFiltersAndRefresh = () => {
        setCountry("");
        setLeague("");
        setPosition("");
        setSort("name");
    };
    useEffect(() => {
        // Wywołuj fetchData tylko, jeśli wszystkie filtry są puste i sort jest "name"
        if (country === "" && league === "" && position === "" && sort === "name") {
            fetchData(1);
        }
    }, [country, league, position, sort]);
    // Hook uruchamiany po załadowaniu komponentu
    useEffect(() => {
        if (!isLoggedIn()) {
            navigate("/login");
            return;
        }

        fetchData(1);
        fetchFilters();
    }, [navigate]);

    // Jeżeli trwa ładowanie – pokaż komponent ładowania
    if (loading) return <Loading />;

    // Jeżeli wystąpił błąd – pokaż komponent błędu
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
                        maxWidth: "1100px",
                        width: "100%",
                        bgcolor: "#1976d2",
                        borderRadius: "12px",
                        overflow: "hidden",
                        boxShadow: 3,
                        minHeight: "100%",
                        mt: 4,
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
                            borderRadius: "12px",
                            padding: 3,
                            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                            minHeight: "300px",
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
                                <Box
                                    sx={{
                                        display: "flex",
                                        gap: 2,
                                        flexWrap: "wrap",
                                        marginBottom: 2,
                                        justifyContent: "center",
                                    }}
                                >
                                    <TextField
                                        select
                                        label="Kraj"
                                        value={country}
                                        onChange={(e) => setCountry(e.target.value)}
                                        size="small"
                                        sx={{
                                            minWidth: 180,
                                            backgroundColor: '#fff',
                                            borderRadius: 1,
                                        }}
                                    >
                                        <MenuItem value="">Wszystkie kraje</MenuItem>
                                        {availableCountries.map((c) => (
                                            <MenuItem key={c} value={c}>{c}</MenuItem>
                                        ))}
                                    </TextField>

                                    <TextField
                                        select
                                        label="Liga"
                                        value={league}
                                        onChange={(e) => setLeague(e.target.value)}
                                        size="small"
                                        sx={{
                                            minWidth: 180,
                                            backgroundColor: '#fff',
                                            borderRadius: 1,
                                        }}
                                    >
                                        <MenuItem value="">Wszystkie ligi</MenuItem>
                                        {availableLeagues.map((l) => (
                                            <MenuItem key={l} value={l}>{l}</MenuItem>
                                        ))}
                                    </TextField>

                                    <TextField
                                        select
                                        label="Pozycja"
                                        value={position}
                                        onChange={(e) => setPosition(e.target.value)}
                                        size="small"
                                        sx={{
                                            minWidth: 180,
                                            backgroundColor: '#fff',
                                            borderRadius: 1,
                                        }}
                                    >
                                        <MenuItem value="">Wszystkie pozycje</MenuItem>
                                        {availablePositions.map((p) => (
                                            <MenuItem key={p} value={p}>{p}</MenuItem>
                                        ))}
                                    </TextField>

                                    <TextField
                                        select
                                        label="Sortowanie"
                                        value={sort}
                                        onChange={(e) => setSort(e.target.value)}
                                        size="small"
                                        sx={{
                                            minWidth: 180,
                                            backgroundColor: '#fff',
                                            borderRadius: 1,
                                        }}
                                    >
                                        <MenuItem value="name">Imię rosnąco</MenuItem>
                                        <MenuItem value="-name">Imię malejąco</MenuItem>
                                        <MenuItem value="age__value">Wiek rosnąco</MenuItem>
                                        <MenuItem value="-age__value">Wiek malejąco</MenuItem>
                                    </TextField>
                                    <Button variant="contained" onClick={() => fetchData(1)}>
                                        Zastosuj
                                    </Button>
                                </Box>

                                <Button
                                    variant="contained"
                                    color="primary"
                                    onClick={resetFiltersAndRefresh}
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
                                        {players.length === 0 ? (
                                            <TableRow>
                                                <TableCell colSpan={7} align="center">
                                                    Nie znaleziono piłkarzy dla wybranych filtrów.
                                                </TableCell>
                                            </TableRow>
                                        ) : (
                                            players.map((player, index) => (
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
                                            ))
                                        )}
                                    </TableBody>
                                </Table>
                            </TableContainer>

                            <Box sx={{ display: "flex", justifyContent: "center", marginTop: 2 }}>
                                <Button
                                    variant="outlined"
                                    onClick={() => fetchData(page - 1)}
                                    disabled={!previous}
                                    sx={{ marginRight: 1 }}
                                >
                                    Poprzednia
                                </Button>
                                {count > 0 && (
                                    <Typography sx={{ alignSelf: "center", mx: 1, color: "black" }}>
                                        Strona {page} z {Math.ceil(count / 3)}
                                    </Typography>
                                )}
                                <Button
                                    variant="outlined"
                                    onClick={() => fetchData(page + 1)}
                                    disabled={!next}
                                    sx={{ marginLeft: 1 }}
                                >
                                    Następna
                                </Button>
                            </Box>
                        </Box>
                    </Box>
                </Box>
            </Box>
        </>
    );
};

export default Home;
