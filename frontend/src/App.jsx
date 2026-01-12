import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./auth/AuthContext";

import Login from "./pages/login";
import Signup from "./pages/Signup";
import Programs from "./pages/Programs";
import ProgramDetail from "./pages/ProgramDetail";
import LessonEditor from "./pages/LessonEditor";
import CreateProgram from "./pages/CreateProgram";
import PublicPrograms from "./pages/PublicPrograms";
import PublicProgramDetail from "./pages/PublicProgramDetail";

export default function App() {
  const { token } = useAuth();

  return (
    <Routes>
      {/* 🌍 PUBLIC CATALOG */}
      <Route path="/" element={<PublicPrograms />} />
      <Route path="/programs" element={<PublicPrograms />} />
      <Route path="/programs/:id" element={<PublicProgramDetail />} />

      {/* 🔐 AUTH */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      {/* 🛠 CMS (PROTECTED) */}
      {token ? (
        <>
          <Route path="/cms/programs" element={<Programs />} />
          <Route path="/cms/programs/new" element={<CreateProgram />} />
          <Route path="/cms/programs/:id" element={<ProgramDetail />} />
          <Route path="/lessons/:id" element={<LessonEditor />} />
        </>
      ) : (
        <Route path="/cms/*" element={<Navigate to="/login" />} />
      )}

      {/* fallback */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}
