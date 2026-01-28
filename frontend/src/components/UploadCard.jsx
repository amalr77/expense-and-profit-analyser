import { useState } from "react";
import api from "../services/api";

export default function UploadCard({ title, endpoint }) {
  const [fileName, setFileName] = useState("");

  const upload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);

    const form = new FormData();
    form.append("file", file);

    await api.post(endpoint, form);
  };

  return (
    <div className="card upload-card">
      <h3>{title}</h3>

      <label className="upload-btn">
         Upload PDF
        <input
          type="file"
          accept="application/pdf"
          onChange={upload}
          hidden
        />
      </label>

      {fileName && <p className="file-name">{fileName}</p>}
    </div>
  );
}
