import { Link } from "react-router-dom";
import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Button,
    IconButton,
    Drawer,
    List,
    ListItem,
    ListItemButton,
    ListItemText,
    useMediaQuery,
    useTheme
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { logout } from "../utils/auth";
import { useState } from "react";

const Navbar = () => {
    const [drawerOpen, setDrawerOpen] = useState(false);
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down("md"));

    const handleToggleDrawer = () => {
        setDrawerOpen(!drawerOpen);
    };

    const commonLinks = [
        { label: "Twój profil", to: "/profile" },
        ...(sessionStorage.getItem("is_superuser") === "True"
            ? [{ label: "Panel administratora", to: "/admin" }]
            : []),
        { label: "Ustawienia", to: "/settings" },
        { label: "Wyloguj się", action: logout },
    ];

    const renderLinks = () =>
        commonLinks.map(({ label, to, action }, idx) => (
            <ListItem key={idx} disablePadding>
                <ListItemButton
                    component={to ? Link : "button"}
                    to={to}
                    onClick={() => {
                        if (action) action();
                        setDrawerOpen(false);
                    }}
                >
                    <ListItemText primary={label} />
                </ListItemButton>
            </ListItem>
        ));

    return (
        <AppBar position="static" sx={{ bgcolor: "#1976d2", marginBottom: 0 }}>
            <Toolbar sx={{ justifyContent: "space-between" }}>
                <Button
                    component={Link}
                    to="/"
                    sx={{
                        fontWeight: "bold",
                        fontSize: isMobile ? "1.1rem" : "1.5rem",
                        color: "#fff",
                        textTransform: "none",
                        background: "linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)",
                        borderRadius: 2,
                        padding: "4px 20px",
                        boxShadow: "0 3px 5px 2px rgba(33, 203, 243, .3)",
                        '&:hover': {
                            background: "linear-gradient(45deg, #1e88e5 30%, #1de9b6 90%)",
                            color: "#a7ffeb",
                        },
                    }}
                >
                    GOALDLE
                </Button>

                {isMobile && (
                    <IconButton
                        edge="end"
                        color="inherit"
                        aria-label="menu"
                        onClick={handleToggleDrawer}
                    >
                        <MenuIcon />
                    </IconButton>
                )}

                {!isMobile && (
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                        {commonLinks.map(({ label, to, action }, index) => (
                            <Button
                                key={index}
                                color="inherit"
                                component={to ? Link : "button"}
                                to={to}
                                onClick={action}
                                sx={{
                                    ml: 2,
                                    ...(label === "Wyloguj się" && { mr: 3 }),
                                    '&:hover': {
                                        backgroundColor: '#1565c0',
                                        color: '#fff',
                                    },
                                }}
                            >
                                {label}
                            </Button>
                        ))}
                    </Box>
                )}
            </Toolbar>

            {isMobile && (
                <Drawer
                    anchor="right"
                    open={drawerOpen}
                    onClose={handleToggleDrawer}
                >
                    <Box
                        sx={{ width: 250 }}
                        role="presentation"
                        onClick={handleToggleDrawer}
                        onKeyDown={handleToggleDrawer}
                    >
                        <List>
                            {renderLinks()}
                        </List>
                    </Box>
                </Drawer>
            )}
        </AppBar>
    );
};

export default Navbar;
