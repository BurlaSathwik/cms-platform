import { useState } from "react";
import { apiFetch } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { Link, useNavigate } from "react-router-dom";

export default function Signup() {
  const { login } = useAuth();
  const navigate = useNavigate(); // ✅ ADD THIS

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await apiFetch("/auth/signup", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      login(res.access_token);

      // 🔥 REQUIRED REDIRECT
      navigate("/cms/programs");

    } catch (err) {
      setError(err.detail || "Signup failed");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "400px" }}>
      <h2>Create Account</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={submit}>
        <label>Email</label>
        <input required type="email" onChange={(e) => setEmail(e.target.value)} />

        <label>Password</label>
        <input
          required
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={{ width: "100%" }}>Sign Up</button>
      </form>

      <p style={{ marginTop: "10px" }}>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}
