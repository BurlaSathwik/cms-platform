import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [role, setRole] = useState(localStorage.getItem("role"));

  const login = async (token) => {
    localStorage.setItem("token", token);
    setToken(token);

    // 🔥 ALWAYS FETCH ROLE FROM BACKEND
    const res = await fetch("https://cms-api-y505.onrender.com/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();

    localStorage.setItem("role", data.role);
    setRole(data.role);
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
