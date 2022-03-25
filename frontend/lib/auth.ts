import { Auth } from "aws-amplify";
import { authStore } from "./authStore";
import shallow from "zustand/shallow";

const useAuth = () => {
    const {
        token,
        user,
        isAuthenticated,
        error,
        setToken,
        setUser,
        setIsAuthenticated,
        setError,
    } = authStore((store) => ({
        token: store.token,
        user: store.user,
        isAuthenticated: store.isAuthenticated,
        error: store.error,
        setToken: store.setToken,
        setUser: store.setUser,
        setIsAuthenticated: store.setIsAuthenticated,
        setError: store.setError,
    }), shallow);

    return { token, user, isAuthenticated, error, setToken, setUser, setIsAuthenticated, setError };
};



export async function signIn(username: string, password: string) {
    try {
        const cognitoUser = await Auth.signIn(username, password);
        authStore().setToken(cognitoUser.signInUserSession.accessToken.jwtToken);
        authStore().setUser({ name: cognitoUser.attributes.name, email: cognitoUser.attributes.email });
        authStore().setError(null);
        authStore().setIsAuthenticated(true);
    } catch (error) {
        console.log(error);
        return false;
    }

    return true;
}