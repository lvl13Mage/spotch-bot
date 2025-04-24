import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App"; // Ensure this points to your main App component
import "./index.css"; // Ensure your global styles are imported

const root = createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <h1	>Spotify Bot</h1>
    <App />
  </React.StrictMode>
);
