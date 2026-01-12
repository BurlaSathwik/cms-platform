import { useState } from "react";
import { apiFetch } from "../api/client";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Card from "../components/Card";

export default function CreateProgram() {
  const [title, setTitle] = useState("");
  const [language, setLanguage] = useState("en");
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();

    const program = await apiFetch("/admin/programs", {
      method: "POST",
      body: JSON.stringify({
        title,
        language_primary: language,
        languages_available: [language],
      }),
    });

    navigate(`/cms/programs/${program.id}`);
  };

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>Create Program</h2>

        <Card>
          <form onSubmit={submit}>
            <label>Title</label>
            <input onChange={(e) => setTitle(e.target.value)} required />

            <label>Primary Language</label>
            <select onChange={(e) => setLanguage(e.target.value)}>
              <option value="en">English</option>
              <option value="te">Telugu</option>
              <option value="hi">Hindi</option>
            </select>

            <button>Create</button>
          </form>
        </Card>
      </div>
    </>
  );
}
