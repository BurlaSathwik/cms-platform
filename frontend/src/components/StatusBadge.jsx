const colors = {
    draft: "#6b7280",
    published: "#16a34a",
    scheduled: "#f59e0b",
    archived: "#dc2626",
  };
  
  export default function StatusBadge({ status }) {
    return (
      <span
        style={{
          padding: "4px 8px",
          borderRadius: "6px",
          backgroundColor: colors[status] || "#6b7280",
          color: "white",
          fontSize: "12px",
        }}
      >
        {status}
      </span>
    );
  }
  