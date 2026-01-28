import { useState } from "react";
import api from "./services/api";
import UploadCard from "./components/UploadCard";
import SummaryCards from "./components/SummaryCards";
import ProfitChart from "./components/ProfitChart";
import AnalyseButton from "./components/AnalyseButton";
import "./index.css";

export default function App() {
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);

  const analyseAndLoad = async () => {
    const summaryRes = await api.get("/summary");
    const historyRes = await api.get("/profit-history");

    setSummary(summaryRes.data);
    setHistory(historyRes.data.reverse());
  };

  return (
    <div className="container">
      <header className="header">
        <h1>expenso.ai</h1>
        <button className="primary">Sign up</button>
      </header>

     
      <div className="upload-section">
  <div className="cards upload-cards">
    <UploadCard
      title="Upload Purchase Bill"
      endpoint="/upload-purchase-bill"
    />
    <UploadCard
      title="Upload Sales Bill"
      endpoint="/upload-sales-bill"
    />
  </div>

  <div className="analyse-section">
    <AnalyseButton onAnalyse={analyseAndLoad} />
    </div>
  </div>

    
      {summary && (
        <div className="cards" style={{ marginTop: "20px" }}>
          <SummaryCards summary={summary} />
        </div>
      )}

      {history.length > 0 && (
        <div className="chart-box">
          <h2>Financial Overview</h2>
          <ProfitChart data={history} />
        </div>
      )}
    </div>
  );
}
