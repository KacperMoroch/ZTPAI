import { Box, Alert } from "@mui/material";

const ErrorComponent = ({ message }) => (
    <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw" }}>
        <Alert severity="error">{message}</Alert>
    </Box>
);

export default ErrorComponent;
