import { Navigate } from "react-router-dom";

const PublicRoute = ({ children }) => {
    const isAuthenticated = !!sessionStorage.getItem("token");

    return isAuthenticated ? <Navigate to="/" /> : children;
};

export default PublicRoute;