import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiFetch } from "../api/client";
import Navbar from "../components/Navbar";
import Card from "../components/Card";

export default function PublicProgramDetail() {
  const { id } = useParams();
  const [program, setProgram] = useState(null);

  useEffect(() => {
    apiFetch(`/catalog/programs/${id}`)
      .then(setProgram)
      .catch(console.error);
  }, [id]);

  if (!program) return <p>Loading...</p>;

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>{program.title}</h2>

        <Card>
          <p>{program.description || "No description available"}</p>

          <p>
            <strong>Primary Language:</strong>{" "}
            {program.language_primary}
          </p>

          <p>
            <strong>Available Languages:</strong>{" "}
            {program.languages_available.join(", ")}
          </p>
        </Card>

        <h3>Curriculum</h3>

        {program.terms.map((term) => (
          <Card key={term.id}>
            <h4>Term {term.term_number}</h4>

            {term.lessons.map((lesson) => (
              <div key={lesson.id} style={{ marginBottom: "6px" }}>
                📘 Lesson {lesson.lesson_number}: {lesson.title}
              </div>
            ))}

            {term.lessons.length === 0 && (
              <p style={{ opacity: 0.6 }}>
                No published lessons yet
              </p>
            )}
          </Card>
        ))}
      </div>
    </>
  );
}
