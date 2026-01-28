import api from "../services/api";

export default function AnalyseButton({ onAnalyse }) {
  const analyse = async () => {
    await api.post("/calculate-profit");
    onAnalyse();
  };

  return (
    <button className="analyse-btn" onClick={analyse}>
      Analyse
    </button>
  );
}
