import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import Navbar from "../components/Navbar";
import Card from "../components/Card";
import { Link } from "react-router-dom";

export default function PublicPrograms() {
  const [programs, setPrograms] = useState([]);

  useEffect(() => {
    apiFetch("/catalog/programs")
      .then(setPrograms)
      .catch(console.error);
  }, []);

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>Programs</h2>

        {programs.map((p) => (
          <Card key={p.id}>
            <h3>{p.title}</h3>

            <p style={{ opacity: 0.7 }}>
              {p.description || "No description available"}
            </p>

            <p>
              <strong>Languages:</strong>{" "}
              {p.languages_available?.join(", ")}
            </p>

            <Link to={`/programs/${p.id}`}>
              <button style={{ marginTop: "10px" }}>
                View Program
              </button>
            </Link>
          </Card>
        ))}

        {programs.length === 0 && (
          <p style={{ opacity: 0.6 }}>No programs published yet</p>
        )}
      </div>
    </>
  );
}
