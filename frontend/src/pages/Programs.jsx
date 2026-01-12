import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/client";
import Navbar from "../components/Navbar";
import Card from "../components/Card";
import StatusBadge from "../components/StatusBadge";
import { useAuth } from "../auth/AuthContext";

export default function Programs() {
  const [programs, setPrograms] = useState(null);
  const navigate = useNavigate();
  const { role } = useAuth();

  const canCreate = role === "admin" || role === "editor";

  useEffect(() => {
    if (!role) return;

    apiFetch("/admin/programs/")
      .then(setPrograms)
      .catch(console.error);
  }, [role]);

  if (!role || programs === null) {
    return (
      <>
        <Navbar />
        <div className="container">
          <p>Loading programs...</p>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />

      <div className="container">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "16px",
          }}
        >
          <h2>Programs</h2>

          {canCreate && (
            <button onClick={() => navigate("/cms/programs/new")}>
              + New Program
            </button>
          )}
        </div>

        {programs.length === 0 && (
          <p style={{ opacity: 0.6 }}>No programs yet</p>
        )}

        {programs.map((p) => {
          // ✅ SAFE + CONSISTENT poster selection
          const poster = Array.isArray(p.assets)
            ? p.assets.find(
                (a) =>
                  (a.asset_type === "poster" || !a.asset_type) &&
                  a.language === p.language_primary &&
                  a.variant === "portrait"
              )
            : null;

          return (
            <Card key={p.id} style={{ marginBottom: "12px" }}>
              <div
                style={{
                  display: "flex",
                  gap: "16px",
                  alignItems: "center",
                }}
              >
                {/* LEFT */}
                <div style={{ flex: 1 }}>
                  <h3 style={{ marginBottom: "4px" }}>{p.title}</h3>

                  <StatusBadge status={p.status} />

                  <p style={{ opacity: 0.8 }}>
                    {p.description || "No description"}
                  </p>

                  <button
                    className="secondary"
                    onClick={() => navigate(`/cms/programs/${p.id}`)}
                  >
                    Open
                  </button>
                </div>

                {/* RIGHT — IMAGE */}
                {poster ? (
                  <img
                    src={poster.url}
                    alt="Program poster"
                    style={{
                      width: "120px",
                      height: "160px",
                      borderRadius: "8px",
                      objectFit: "cover",
                    }}
                  />
                ) : (
                  <div
                    style={{
                      width: "120px",
                      height: "160px",
                      borderRadius: "8px",
                      background: "#e5e7eb",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "12px",
                      color: "#6b7280",
                    }}
                  >
                    No Image
                  </div>
                )}
              </div>
            </Card>
          );
        })}
      </div>
    </>
  );
}
