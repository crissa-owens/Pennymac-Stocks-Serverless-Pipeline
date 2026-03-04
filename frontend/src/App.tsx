import { useEffect, useState } from "react";

const API_URL = "https://ui07bqfkv4.execute-api.us-east-1.amazonaws.com/prod/movers";

interface StockMover {
  date: string;
  ticker: string;
  percent_change: number;
  closing_price: number;
}

function App() {
  const [movers, setMovers] = useState<StockMover[]>([]);

  useEffect(() => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => setMovers(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Top Stock Movers (Last 7 Days)</h1>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Date</th>
            <th>Ticker</th>
            <th>% Change</th>
            <th>Closing Price</th>
          </tr>
        </thead>
        <tbody>
          {movers.map((item, index) => (
            <tr key={index}>
              <td>{item.date}</td>
              <td>{item.ticker}</td>
              <td style={{
                color: item.percent_change >= 0 ? "green" : "red",
                fontWeight: "bold"
              }}>
                {item.percent_change}%
              </td>
              <td>${item.closing_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;