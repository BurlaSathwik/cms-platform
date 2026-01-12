import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [role, setRole] = useState(localStorage.getItem("role"));

  const login = (token) => {
    const payload = JSON.parse(atob(token.split(".")[1]));

    // ✅ STORE TOKEN (CRITICAL)
    localStorage.setItem("token", token);
    localStorage.setItem("role", payload.role);

    setToken(token);
    setRole(payload.role);
  };

  const logout = () => {
    localStorage.clear();
    setToken(null);
    setRole(null);
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider value={{ token, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
