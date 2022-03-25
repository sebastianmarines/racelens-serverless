import create from "zustand";

interface AuthState {
    token: string | null;
    user: {
        name: string | null;
        email: string | null;
    };
    isAuthenticated: boolean;
    error: string | null;
    setToken: (token: string | null) => void;
    setUser: (user: {
        name: string | null;
        email: string | null;
    }) => void;
    setIsAuthenticated: (isAuthenticated: boolean) => void;
    setError: (error: string | null) => void;
}

export const authStore = create<AuthState>(set => ({
    token: null,
    user: {
        name: null,
        email: null,
    },
    isAuthenticated: false,
    error: null,
    setToken: (token: string | null) => set(state => ({ ...state, token })),
    setUser: (user: { name: string | null; email: string | null; }) => set(state => ({ ...state, user })),
    setIsAuthenticated: (isAuthenticated: boolean) => set(state => ({ ...state, isAuthenticated })),
    setError: (error: string | null) => set(state => ({ ...state, error })),
}));