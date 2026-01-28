export default function SummaryCards({ summary }) {
  if (!summary) return null;

  return (
    <>
      <div className="card">
        <h3>Total Purchase</h3>
        <p>₹ {summary.total_purchase.toFixed(2)}</p>
      </div>
      <div className="card">
        <h3>Total Sales</h3>
        <p>₹ {summary.total_sales.toFixed(2)}</p>
      </div>
      <div className="card highlight">
        <h3>Profit</h3>
        <p>₹ {summary.profit.toFixed(2)}</p>
      </div>
    </>
  );
}
