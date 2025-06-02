import { useState, useEffect } from "react";
import {
    Box,
    Typography,
    Button,
    Alert,
    CircularProgress,
    Paper,
    TextField,
    Autocomplete,
} from "@mui/material";
import debounce from "lodash.debounce";

import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import Navbar from "../components/Navbar";

const GuessTransfer = () => {
    const [playerName, setPlayerName] = useState("");
    const [playerOptions, setPlayerOptions] = useState([]);
    const [remainingAttempts, setRemainingAttempts] = useState(5);
    const [transferDetails, setTransferDetails] = useState(null);
    const [message, setMessage] = useState(null);
    const [loading, setLoading] = useState(true);
    const [gameOver, setGameOver] = useState(false);

    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                setLoading(true);
                const data = await fetchWithRefresh("http://127.0.0.1:8000/api/transfer/start");

                setTransferDetails(data.transfer_details);
                setRemainingAttempts(data.remaining_attempts);
                setGameOver(data.game_over);

                if (data.game_over) {
                    if (data.guessed_correctly) {
                        setMessage({
                            type: "info",
                            text: `Już zgadłeś dzisiaj piłkarza. Spróbuj ponownie jutro.\nPiłkarzem do zgadnięcia był: ${data.correct_player}.`
                        });
                    } else {
                        setMessage({
                            type: "warning",
                            text: `Nie masz więcej prób. Spróbuj ponownie jutro. Piłkarzem do zgadnięcia był: ${data.correct_player}.`
                        });
                    }
                }
            } catch (error) {
                setMessage({ type: "error", text: error.message || "Błąd ładowania danych" });
            } finally {
                setLoading(false);
            }
        };

        fetchInitialData();
    }, []);

    const fetchSuggestions = debounce(async (input) => {
        try {
            const res = await fetchWithRefresh(`http://127.0.0.1:8000/api/player-names/?query=${input}`);
            setPlayerOptions(res.players || []);
        } catch (err) {
            console.error("Błąd pobierania nazwisk piłkarzy:", err);
        }
    }, 300);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage(null);

        if (!playerName.trim()) {
            setMessage({ type: "error", text: "Wpisz nazwisko piłkarza." });
            return;
        }

        try {
            setLoading(true);
            const response = await fetchWithRefresh("http://127.0.0.1:8000/api/transfer/guess", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ player_name: playerName.trim() }),
            });

            if (response.error) {
                setMessage({ type: "error", text: response.error });
                if (response.game_over) {
                    setGameOver(true);
                    if (response.from_club && response.to_club && response.transfer_amount) {
                        setTransferDetails({
                            from_club: response.from_club,
                            to_club: response.to_club,
                            transfer_amount: response.transfer_amount,
                        });
                    }
                }
                return;
            }

            setRemainingAttempts(response.remaining_attempts);
            setGameOver(response.game_over);
            setPlayerName("");

            if (response.guessed_correctly) {
                setMessage({
                    type: "success",
                    text: `Brawo! Zgadłeś piłkarza: ${response.correct_player}`,
                });
                setTransferDetails({
                    from_club: response.from_club,
                    to_club: response.to_club,
                    transfer_amount: response.transfer_amount,
                });
            } else {
                if (response.game_over) {
                    setTransferDetails({
                        from_club: response.from_club,
                        to_club: response.to_club,
                        transfer_amount: response.transfer_amount,
                    });

                    setMessage({
                        type: "warning",
                        text: `Nie masz więcej prób. Piłkarzem do zgadnięcia był: ${response.correct_player}`,
                    });
                } else {
                    setMessage({
                        type: "error",
                        text: `Niestety, to nie ten piłkarz`,
                    });
                }
            }
        } catch (error) {
            setMessage({ type: "error", text: "Błąd podczas wysyłania zgadnięcia." });
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <Navbar />
            <Box
                sx={{
                    minHeight: "100vh",
                    width: "100vw",
                    bgcolor: "#30d1f6",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    padding: "20px",
                }}
            >
                <Box
                    sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        maxWidth: "900px",
                        width: "100%",
                    }}
                >
                    <Typography
                        variant="h3"
                        fontWeight={600}
                        sx={{
                            textAlign: "center",
                            fontSize: { xs: "1.4rem", md: "2.3rem" },
                            color: "#0078A0",
                            textShadow: "1px 1px 2px rgba(0,0,0,0.2)",
                            px: 7,
                            mb: 4,
                        }}
                    >
                        Zgadnij transfer w TOP 5 ligach europejskich
                    </Typography>

                    <Paper
                        elevation={6}
                        sx={{
                            padding: { xs: 2, md: 3 },
                            maxWidth: { xs: 300, md: 400 },
                            width: "100%",
                            textAlign: "center",
                            backgroundColor: "#0078A0",
                            color: "#fff",
                        }}
                    >
                        <Typography variant="h5" align="center" mb={1.5}>
                            Zgadnij transfer
                        </Typography>

                        <Typography mb={1}>Pozostałe próby: {remainingAttempts}</Typography>

                        <form onSubmit={handleSubmit}>
                            <Autocomplete
                                freeSolo
                                options={playerOptions}
                                inputValue={playerName}
                                onInputChange={(event, newInputValue) => {
                                    setPlayerName(newInputValue);
                                    fetchSuggestions(newInputValue);
                                }}
                                disabled={loading || gameOver}
                                renderInput={(params) => (
                                    <TextField
                                        {...params}
                                        fullWidth
                                        placeholder="Wpisz nazwisko piłkarza"
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
                                color="primary"
                                sx={{ mt: 2 }}
                                disabled={loading || gameOver}
                                fullWidth
                            >
                                Zgadnij
                            </Button>
                        </form>

                        {loading && (
                            <Box mt={2} display="flex" justifyContent="center">
                                <CircularProgress size={24} />
                            </Box>
                        )}

                        {message && (
                            <Alert severity={message.type} sx={{ mt: 2 }}>
                                {message.text}
                            </Alert>
                        )}

                        {transferDetails && (
                            <Box mt={3} textAlign="left" sx={{ fontSize: "1rem" }}>
                                <Typography>
                                    Transfer z: <strong>{transferDetails.from_club}</strong> do{" "}
                                    <strong>{transferDetails.to_club}</strong>
                                </Typography>
                                <Typography>
                                    Kwota transferu:{" "}
                                    <strong>{transferDetails.transfer_amount} mln €</strong>
                                </Typography>
                            </Box>
                        )}
                    </Paper>
                </Box>
            </Box>
        </>
    );
};

export default GuessTransfer;
