import React, { useEffect, useState, useRef } from "react";
import {
    Autocomplete,
    TextField,
    Button,
    Typography,
    Box,
    Paper,
    Alert,
    CircularProgress,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import debounce from "lodash.debounce";

import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import { isLoggedIn } from "../utils/auth";
import Navbar from "../components/Navbar";

const GuessPlayerPage = () => {
    const [guess, setGuess] = useState("");
    const [playerOptions, setPlayerOptions] = useState([]);
    const [message, setMessage] = useState("");
    const [remaining, setRemaining] = useState(5);
    const [correct, setCorrect] = useState(false);
    const [gameOver, setGameOver] = useState(false);
    const [guesses, setGuesses] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const bottomRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isLoggedIn()) {
            navigate("/login");
        }
    }, [navigate]);

    useEffect(() => {
        const fetchGameStatus = async () => {
            try {
                const res = await fetchWithRefresh("http://127.0.0.1:8000/api/game-status/");
                if (!res.error) {
                    setRemaining(res.remaining_attempts);
                    if (res.guessed_correctly) {
                        setCorrect(true);
                        setGameOver(true);
                        setMessage(`Brawo! Już zgadłeś dzisiaj piłkarza. Szukanym piłkarzem był: ${res.target_player_name}.`);
                    } else if (res.remaining_attempts === 0) {
                        setGameOver(true);
                        setMessage(`Gra zakończona. Wykorzystałeś wszystkie próby na dzisiaj. Szukanym piłkarzem był: ${res.target_player_name}. Spróbuj jutro!`);
                    }
                }
            } catch (err) {
                console.error("Błąd pobierania statusu gry:", err);
            }
        };

        fetchGameStatus();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (gameOver) return;

        setLoading(true);
        setError(null);
        setMessage("");

        try {
            const res = await fetchWithRefresh("http://127.0.0.1:8000/api/guess/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ player_name: guess }),
            });

            if (res.error) {
                setError(res.error);
                setRemaining(res.remaining_attempts ?? remaining);
                setGameOver(res.game_over ?? false);
            } else {
                setMessage(res.message);
                setRemaining(res.remaining_attempts);
                setCorrect(res.correct);
                setGameOver(res.correct || res.remaining_attempts === 0);
                if (res.player_data) {
                    setGuesses((prev) => [
                        ...prev,
                        {
                            player: res.player_data,
                            matches: res.matches,
                            correct: res.correct,
                        },
                    ]);
                }
            }
        } catch (err) {
            setError("Błąd serwera. Spróbuj ponownie.");
        } finally {
            setLoading(false);
        }
    };

    const fetchSuggestions = debounce(async (input) => {
        try {
            const res = await fetchWithRefresh(`http://127.0.0.1:8000/api/player-names/?query=${input}`);
            setPlayerOptions(res.players || []);
        } catch (err) {
            console.error("Błąd pobierania nazwisk piłkarzy:", err);
        }
    }, 300);

    const AttributeBox = ({ label, value, match, comparison }) => {
        const bgColor = match ? "#33cc66" : "#cc3333";
        const arrow = comparison === "up" ? "↑" : comparison === "down" ? "↓" : "";
        return (
            <Box
                sx={{
                    backgroundColor: bgColor,
                    color: "#fff",
                    borderRadius: 1,
                    p: 1,
                    my: 0.5,
                    fontWeight: "bold",
                }}
            >
                {label}: {value} {arrow}
            </Box>
        );
    };

    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [guesses]);

    return (
        <>
            <Navbar />

            <Box
                sx={{
                    minHeight: "100vh",
                    width: "100vw",
                    bgcolor: "#30d1f6",
                    //overflowX: "hidden",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    padding: "20px",
                }}
            >
                <Typography
                    variant="h3"
                    fontWeight={600}
                    sx={{
                        textAlign: { xs: "center", sm: "center" },
                        fontSize: { xs: "1.5rem", sm: "2rem", md: "2.3rem" },
                        color: "#0078A0",
                        textShadow: "1px 1px 2px rgba(0,0,0,0.2)",
                        px: { xs: 2, md: 8 },
                        mb: 4,
                        // wordBreak: "break-word",
                    }}
                >
                    Zgadnij piłkarza z TOP 5 lig europejskich
                </Typography>

                <Box
                    sx={{
                        display: "flex",
                        flexDirection: { xs: "column", md: "row" },
                        gap: { xs: 3.3, md: 8 },
                        justifyContent: "center",
                        alignItems: { xs: "center", md: "flex-start" },
                        width: "100%",
                        maxWidth: "1200px",
                        // px: { xs: 0, sm: 2 },
                    }}
                >
                    <Paper
                        elevation={4}
                        sx={{
                            p: { xs: 2, sm: 3 },
                            backgroundColor: "#0078A0",
                            color: "#fff",
                            width: "100%",
                            maxWidth: { xs: 320, sm: 400 },
                            //mx: "auto",

                            alignSelf: { xs: "center", sm: "center" },
                        }}
                    >
                        <Typography variant="h5" align="center" gutterBottom>
                            Zgadnij piłkarza
                        </Typography>
                        <form onSubmit={handleSubmit}>
                            <Autocomplete
                                freeSolo
                                inputValue={guess}
                                onInputChange={(event, newInputValue) => {
                                    setGuess(newInputValue);
                                    fetchSuggestions(newInputValue);
                                }}
                                options={playerOptions}
                                disabled={gameOver}
                                renderInput={(params) => (
                                    <TextField
                                        {...params}
                                        label="Wpisz nazwisko piłkarza"
                                        variant="outlined"
                                        required
                                        sx={{ backgroundColor: "#fff", borderRadius: 1 }}
                                        onFocus={() => {
                                            if (playerOptions.length === 0) {
                                                fetchSuggestions("");
                                            }
                                        }}
                                    />
                                )}
                            />
                            <Button
                                type="submit"
                                variant="contained"
                                fullWidth
                                sx={{ mt: 2, py: 1.5, fontSize: { xs: "0.9rem", sm: "1rem" } }}
                                disabled={gameOver || loading}
                            >
                                Zgadnij
                            </Button>
                        </form>

                        <Typography
                            variant="subtitle1"
                            sx={{ mt: 2, textAlign: "center", display: "block", width: "100%" }}
                        >
                            Pozostałe próby: {remaining}
                        </Typography>

                        {loading && <CircularProgress sx={{ mt: 2 }} />}
                        {error && (
                            <Alert severity="error" sx={{ mt: 2 }}>
                                {error}
                            </Alert>
                        )}
                        {message && !error && (
                            <Alert severity={correct ? "success" : "info"} sx={{ mt: 2 }}>
                                {message}
                            </Alert>
                        )}
                    </Paper>

                    {guesses.length > 0 && (
                        <Paper
                            elevation={4}
                            sx={{
                                p: { xs: 1, sm: 1.5 },
                                backgroundColor: "#00698c",
                                borderRadius: 2,
                                width: "100%",
                                maxWidth: { xs: 337, sm: 400 },
                                maxHeight: { xs: "50vh", sm: "345px" },
                                overflowY: "auto",

                            }}
                        >
                            {guesses.map((guess, index) => (
                                <Box
                                    key={index}
                                    sx={{
                                        p: { xs: 1, sm: 2 },
                                        mb: 2,
                                        border: "1px solid #ccc",
                                        borderRadius: 2,
                                        backgroundColor: guess.correct ? "#e0ffe0" : "#FADBD8",
                                    }}
                                >
                                    <Typography fontWeight="bold" sx={{ color: "#0044cc", mb: 1 }}>
                                        {guess.player.name}
                                    </Typography>
                                    <AttributeBox label="Kraj" value={guess.player.country} match={guess.matches.country} />
                                    <AttributeBox label="Liga" value={guess.player.league} match={guess.matches.league} />
                                    <AttributeBox label="Klub" value={guess.player.club} match={guess.matches.club} />
                                    <AttributeBox label="Pozycja" value={guess.player.position} match={guess.matches.position} />
                                    <AttributeBox label="Wiek" value={guess.player.age} match={guess.matches.age} comparison={guess.matches.age_comparison} />
                                    <AttributeBox label="Numer" value={guess.player.number} match={guess.matches.shirt_number} comparison={guess.matches.shirt_number_comparison} />
                                </Box>
                            ))}
                            <div ref={bottomRef} />
                        </Paper>
                    )}
                </Box>
            </Box>
        </>
    );
};

export default GuessPlayerPage;
