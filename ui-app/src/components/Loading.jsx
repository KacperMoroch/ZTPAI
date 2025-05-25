import { Box, CircularProgress } from "@mui/material";

const Loading = () => (
    <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", width: "100vw" }}>
        <CircularProgress />
    </Box>
);

export default Loading;
