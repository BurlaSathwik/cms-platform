import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import { apiFetch } from "../api/client";
import { useAuth } from "../auth/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      login(res.access_token);

      // 🔥 THIS IS THE FIX
      navigate("/cms/programs");

    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "400px" }}>
      <h2>Login</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={submit}>
        <label>Email</label>
        <input type="email" required onChange={(e) => setEmail(e.target.value)} />

        <label>Password</label>
        <input
          type="password"
          required
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={{ width: "100%" }}>Login</button>
      </form>

      <p style={{ marginTop: "10px" }}>
        New here? <Link to="/signup">Create account</Link>
      </p>
    </div>
  );
}
