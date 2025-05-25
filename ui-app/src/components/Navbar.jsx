import { Link } from "react-router-dom";
import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Button,
} from "@mui/material";
import { logout } from "../utils/auth";

const Navbar = () => {
    return (
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
    );
};

export default Navbar;
