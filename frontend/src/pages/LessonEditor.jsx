import { useParams, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import Navbar from "../components/Navbar";
import Card from "../components/Card";
import StatusBadge from "../components/StatusBadge";
import { useAuth } from "../auth/AuthContext";

function formatDateTime(value) {
  if (!value) return "—";
  const utcValue = value.endsWith("Z") ? value : value + "Z";
  return new Date(utcValue).toLocaleString();
}

export default function LessonEditor() {
  const { id } = useParams();
  const { role, token } = useAuth();

  if (!token || !role) return <p>Loading permissions...</p>;
  if (role === "viewer") return <Navigate to="/programs" replace />;

  const [lesson, setLesson] = useState(null);
  const [publishAt, setPublishAt] = useState("");

  const [title, setTitle] = useState("");
  const [isPaid, setIsPaid] = useState(false);
  const [contentType, setContentType] = useState("video");

  const [contentLang, setContentLang] = useState("en");
  const [contentUrl, setContentUrl] = useState("");

  const [thumbLang, setThumbLang] = useState("en");
  const [thumbVariant, setThumbVariant] = useState("portrait");
  const [thumbUrl, setThumbUrl] = useState("");

  const [subLang, setSubLang] = useState("en");
  const [subUrl, setSubUrl] = useState("");

  useEffect(() => {
    apiFetch(`/admin/lessons/${id}`).then((data) => {
      setLesson(data);
      setTitle(data.title);
      setIsPaid(data.is_paid);
      setContentType(data.content_type || "video");
    });
  }, [id]);

  if (!lesson) return <p>Loading lesson...</p>;

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>Lesson Editor</h2>

        {/* STATUS */}
        <Card>
          <StatusBadge status={lesson.status} />
          {lesson.status === "scheduled" && (
            <p>📅 Scheduled: {formatDateTime(lesson.publish_at)}</p>
          )}
          {lesson.status === "published" && (
            <p>✅ Published: {formatDateTime(lesson.published_at)}</p>
          )}
        </Card>

        {/* BASIC DETAILS */}
        <Card>
          <h3>Lesson Details</h3>

          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Lesson title"
          />

          <select
            value={contentType}
            onChange={(e) => setContentType(e.target.value)}
          >
            <option value="video">Video</option>
            <option value="article">Article</option>
          </select>

          <label>
            <input
              type="checkbox"
              checked={isPaid}
              onChange={(e) => setIsPaid(e.target.checked)}
            />
            Paid Lesson
          </label>

          <button
            onClick={async () => {
              await apiFetch(`/admin/lessons/${id}`, {
                method: "PUT",
                body: JSON.stringify({
                  title,
                  is_paid: isPaid,
                  content_type: contentType,
                }),
              });
              window.location.reload();
            }}
          >
            Save
          </button>
        </Card>

        {/* CONTENT URLS */}
        <Card>
          <h3>Content URLs</h3>

          <input
            placeholder="Language"
            value={contentLang}
            onChange={(e) => setContentLang(e.target.value)}
          />
          <input
            placeholder="Content URL"
            value={contentUrl}
            onChange={(e) => setContentUrl(e.target.value)}
          />

          <button
            onClick={async () => {
              await apiFetch(`/admin/lessons/${id}/content`, {
                method: "POST",
                body: JSON.stringify({
                  language: contentLang,
                  url: contentUrl,
                }),
              });
              setContentUrl("");
            }}
          >
            Add
          </button>
        </Card>

        {/* THUMBNAILS */}
        <Card>
          <h3>Thumbnails</h3>

          <select
            value={thumbVariant}
            onChange={(e) => setThumbVariant(e.target.value)}
          >
            <option value="portrait">Portrait</option>
            <option value="landscape">Landscape</option>
            <option value="square">Square</option>
            <option value="banner">Banner</option>
          </select>

          <input
            placeholder="Language"
            value={thumbLang}
            onChange={(e) => setThumbLang(e.target.value)}
          />
          <input
            placeholder="Image URL"
            value={thumbUrl}
            onChange={(e) => setThumbUrl(e.target.value)}
          />

          <button
            onClick={async () => {
              await apiFetch(`/admin/lessons/${id}/assets/`, {
                method: "POST",
                body: JSON.stringify({
                  language: thumbLang,
                  variant: thumbVariant,
                  url: thumbUrl,
                }),
              });
              setThumbUrl("");
            }}
          >
            Save
          </button>

          {thumbUrl && (
            <img
              src={thumbUrl}
              alt="preview"
              style={{ maxWidth: "200px", marginTop: "10px" }}
            />
          )}
        </Card>

        {/* SUBTITLES */}
        <Card>
          <h3>Subtitles</h3>

          <input
            placeholder="Language"
            value={subLang}
            onChange={(e) => setSubLang(e.target.value)}
          />
          <input
            placeholder="Subtitle URL"
            value={subUrl}
            onChange={(e) => setSubUrl(e.target.value)}
          />

          <button
            onClick={async () => {
              await apiFetch(`/admin/lessons/${id}/assets/`, {
                method: "POST",
                body: JSON.stringify({
                  language: subLang,
                  variant: "subtitle",
                  url: subUrl,
                }),
              });
              setSubUrl("");
            }}
          >
            Save
          </button>
        </Card>

        {/* PUBLISH */}
        <Card>
          <button
            onClick={async () => {
              await apiFetch(`/admin/lessons/${id}/publish`, {
                method: "POST",
              });
              window.location.reload();
            }}
          >
            Publish Now
          </button>

          <input
            type="datetime-local"
            onChange={(e) =>
              setPublishAt(new Date(e.target.value).toISOString())
            }
          />

          <button
            onClick={async () => {
              await apiFetch(`/admin/lessons/${id}/schedule`, {
                method: "POST",
                body: JSON.stringify({ publish_at: publishAt }),
              });
              window.location.reload();
            }}
          >
            Schedule
          </button>
        </Card>
      </div>
    </>
  );
}
