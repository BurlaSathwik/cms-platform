const API_BASE_URL = "https://cms-api-y505.onrender.com";

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const res = await fetch(API_URL + path, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const err = await res.json();
    throw err;
  }

  return res.json();
}
