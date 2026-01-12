export default function Card({ children }) {
    return (
      <div
        style={{
          background: "white",
          padding: "16px",
          borderRadius: "10px",
          boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
          marginBottom: "16px",
        }}
      >
        {children}
      </div>
    );
  }
  