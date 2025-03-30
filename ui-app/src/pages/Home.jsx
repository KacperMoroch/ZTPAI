import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, CircularProgress, Alert, Box, Button } from "@mui/material";

const Home = () => {
    const [users, setUsers] = useState([]);
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchData = () => {
        setLoading(true);
        setError(null);

        Promise.all([
            fetch("http://127.0.0.1:8000/api/users/").then((res) => res.json()),
            fetch("http://127.0.0.1:8000/api/players/").then((res) => res.json()),
        ])
            .then(([usersData, playersData]) => {
                setUsers(usersData);
                setPlayers(playersData);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    };

    // wywołanie fetchData po załadowaniu komponentu
    useEffect(() => {
        fetchData();
    }, []);

    return (
        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw", textAlign: "center", padding: "20px" }}>
            <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", maxWidth: "900px", width: "100%" }}>
                {/* Nawigacja */}
                <nav style={{ marginBottom: "20px" }}>
                    <Link to="/login" style={{ textDecoration: "none", marginRight: "15px", fontWeight: "bold", color: "#007bff" }}>
                        Logowanie
                    </Link>
                    |
                    <Link to="/register" style={{ textDecoration: "none", marginLeft: "15px", fontWeight: "bold", color: "#007bff" }}>
                        Rejestracja
                    </Link>
                </nav>

                {/* Sekcja ładowania i błędów */}
                {loading && <CircularProgress />}
                {error && <Alert severity="error">{error}</Alert>}

                {/* Przycisk odświeżania */}
                <Button
                    variant="contained"
                    color="primary"
                    sx={{ marginBottom: 2 }}
                    onClick={fetchData}
                >
                    Odśwież dane
                </Button>

                {/* Tabela użytkowników */}
                <Typography variant="h5" sx={{ marginBottom: 2, marginTop: 2 }}>Lista użytkowników</Typography>
                <Box sx={{ display: "flex", justifyContent: "center", width: "100%" }}>
                    <TableContainer component={Paper} sx={{ width: "30%" }}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell align="center" sx={{ maxWidth: "100px", width: "100px" }}><strong>Login</strong></TableCell>
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

                {/* Tabela piłkarzy */}
                <Typography variant="h5" sx={{ marginBottom: 2, marginTop: 4 }}>Lista piłkarzy</Typography>
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
    );
};

export default Home;
