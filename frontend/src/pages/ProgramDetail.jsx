import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { apiFetch } from "../api/client";
import Card from "../components/Card";
import StatusBadge from "../components/StatusBadge";
import Navbar from "../components/Navbar";
import { useAuth } from "../auth/AuthContext";

export default function ProgramDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { role } = useAuth();

  const canEdit = role === "admin" || role === "editor";

  const [program, setProgram] = useState(null);
  const [termNumber, setTermNumber] = useState("");

  const [assetLang, setAssetLang] = useState("en");
  const [assetVariant, setAssetVariant] = useState("portrait");
  const [assetUrl, setAssetUrl] = useState("");

  useEffect(() => {
    if (!role) return;

    const path = canEdit ? `/admin/programs/${id}` : `/catalog/programs/${id}`;

    apiFetch(path).then(setProgram).catch(console.error);
  }, [id, role]);

  if (!program) return <p>Loading...</p>;

  // ✅ CORRECT poster selection (THIS IS CRITICAL)
  const poster = Array.isArray(program.assets)
    ? program.assets.find(
        (a) =>
          a.language === program.language_primary && a.variant === "portrait"
      )
    : null;

  return (
    <>
      <Navbar />

      <div className="container">
        <button className="secondary" onClick={() => navigate("/cms/programs")}>
          ← Back
        </button>

        <h2>{program.title}</h2>
        {canEdit && <StatusBadge status={program.status} />}

        <Card>
          <div style={{ display: "flex", gap: "20px" }}>
            <div style={{ flex: 1 }}>
              <p>{program.description || "No description"}</p>
              <p>
                <strong>Languages:</strong>{" "}
                {program.languages_available.join(", ")}
              </p>
            </div>

            {poster && (
              <img
                src={poster.url}
                alt="Program poster"
                style={{
                  width: "180px",
                  borderRadius: "8px",
                  objectFit: "cover",
                }}
              />
            )}
          </div>
        </Card>

        {canEdit && (
          <Card>
            <h3>Program Assets</h3>

            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
              <select
                value={assetLang}
                onChange={(e) => setAssetLang(e.target.value)}
              >
                {program.languages_available.map((l) => (
                  <option key={l} value={l}>
                    {l}
                  </option>
                ))}
              </select>

              <select
                value={assetVariant}
                onChange={(e) => setAssetVariant(e.target.value)}
              >
                <option value="portrait">Portrait</option>
                <option value="landscape">Landscape</option>
                <option value="square">Square</option>
                <option value="banner">Banner</option>
              </select>

              <input
                placeholder="Image URL"
                value={assetUrl}
                onChange={(e) => setAssetUrl(e.target.value)}
                style={{ minWidth: "260px" }}
              />

              <button
                onClick={async () => {
                  if (!assetUrl) return alert("Image URL required");

                  await apiFetch(`/admin/programs/${program.id}/assets/`, {
                    method: "POST",
                    body: JSON.stringify({
                      asset_type: "poster",
                      language: assetLang,
                      variant: assetVariant,
                      url: assetUrl,
                    }),
                  });

                  // 🔁 Re-fetch program
                  const refreshed = await apiFetch(
                    `/admin/programs/${program.id}`
                  );
                  setProgram(refreshed);

                  // clear input
                  setAssetUrl("");
                }}
              >
                Save
              </button>
              {assetUrl && (
                <img
                  src={assetUrl}
                  alt="preview"
                  style={{
                    marginTop: "10px",
                    maxWidth: "200px",
                    borderRadius: "6px",
                  }}
                />
              )}
            </div>
          </Card>
        )}

        {canEdit && (
          <Card>
            <h4>Create Term</h4>
            <input
              type="number"
              placeholder="Term Number"
              value={termNumber}
              onChange={(e) => setTermNumber(e.target.value)}
            />
            <button
              onClick={async () => {
                await apiFetch("/admin/terms/", {
                  method: "POST",
                  body: JSON.stringify({
                    program_id: program.id,
                    term_number: Number(termNumber),
                  }),
                });

                const refreshed = await apiFetch(
                  `/admin/programs/${program.id}`
                );
                setProgram(refreshed);
                setTermNumber("");
              }}
            >
              Add Term
            </button>
          </Card>
        )}
        <h3>Terms</h3>

        {program.terms?.length === 0 && (
          <p style={{ opacity: 0.6 }}>No terms yet</p>
        )}

        {program.terms?.map((t) => (
          <Card key={t.id} style={{ marginBottom: "16px" }}>
            <h4>Term {t.term_number}</h4>

            {/* Lessons */}
            {t.lessons?.length === 0 && (
              <p style={{ opacity: 0.6 }}>No lessons yet</p>
            )}

            {t.lessons?.map((l) => (
              <div
                key={l.id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: "6px",
                }}
              >
                <span>
                  Lesson {l.lesson_number}: {l.title}
                </span>

                {canEdit && (
                  <button
                    onClick={() => navigate(`/lessons/${l.id}`)}
                    className="secondary"
                  >
                    Edit
                  </button>
                )}
              </div>
            ))}

            {/* ➕ ADD LESSON */}
            {canEdit && (
              <button
                style={{ marginTop: "10px" }}
                onClick={async () => {
                  const title = prompt("Lesson title?");
                  if (!title) return;

                  await apiFetch("/admin/lessons/", {
                    method: "POST",
                    body: JSON.stringify({
                      term_id: t.id,
                      lesson_number: (t.lessons?.length || 0) + 1,
                      title,
                      content_type: "video",
                      is_paid: false,
                    }),
                  });

                  // refresh program
                  const refreshed = await apiFetch(
                    `/admin/programs/${program.id}`
                  );
                  setProgram(refreshed);
                }}
              >
                + Add Lesson
              </button>
            )}
          </Card>
        ))}
      </div>
    </>
  );
}
