import { useAuth } from "../auth/AuthContext";
import { Link } from "react-router-dom";

export default function Navbar() {
  const { token, role, logout } = useAuth();

  const homeLink =
    role === "admin" || role === "editor" ? "/cms/programs" : "/programs";

  return (
    <div
      style={{
        background: "#111827",
        color: "white",
        padding: "12px 20px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <Link
        to={token ? "/cms/programs" : "/programs"}
        style={{ color: "white", textDecoration: "none" }}
      >
        <strong>CMS Platform</strong>
      </Link>

      <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
        {role && <span style={{ opacity: 0.7 }}>{role}</span>}

        {token ? (
          <button className="secondary" onClick={logout}>
            Logout
          </button>
        ) : (
          <Link to="/login">
            <button className="secondary">Login</button>
          </Link>
        )}
      </div>
    </div>
  );
}
