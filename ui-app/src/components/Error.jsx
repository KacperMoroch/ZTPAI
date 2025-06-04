import { Box, Alert, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const ErrorComponent = ({ message }) => {
    const navigate = useNavigate();

    const handleLoginRedirect = () => {
        navigate("/login");
    };

    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "100vh",
                width: "100vw",
                gap: 4,
                bgcolor: "#fefefe",
                px: 2,
            }}
        >
            {message === "Sesja wygasła..." ? (
                <>
                    <Alert
                        severity="error"
                        sx={{
                            fontSize: "2rem",
                            py: 4,
                            px: 6,
                            textAlign: "center",
                        }}
                    >
                        <Typography variant="h3" component="div" sx={{ fontWeight: "bold" }}>
                            {message}
                        </Typography>
                    </Alert>
                    <Button
                        variant="contained"
                        size="large"
                        onClick={handleLoginRedirect}
                        sx={{
                            fontSize: "1.5rem",
                            px: 4,
                            py: 1.5,
                        }}
                    >
                        Przejdź do logowania
                    </Button>
                </>
            ) : (
                <Alert severity="error">{message}</Alert>
            )}
        </Box>
    );
};

export default ErrorComponent;
