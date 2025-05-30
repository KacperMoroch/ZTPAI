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
                <Button
                    component={Link}
                    to="/"
                    sx={{
                        fontWeight: "bold",
                        fontSize: "1.5rem",
                        color: "#fff",
                        textTransform: "none",
                        background: "linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)",
                        borderRadius: 2,
                        padding: "4px 20px",
                        boxShadow: "0 3px 5px 2px rgba(33, 203, 243, .3)",
                        cursor: "pointer",
                        '&:hover': {
                            background: "linear-gradient(45deg, #1e88e5 30%, #1de9b6 90%)",
                            color: "#a7ffeb",
                        },
                    }}
                >
                    GOALDLE
                </Button>

                <Box sx={{ display: "flex", alignItems: "center", ml: 0, justifyContent: "flex-start" }}>
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
