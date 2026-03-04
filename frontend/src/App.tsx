import { useEffect, useState } from "react";

const API_URL = "https://ui07bqfkv4.execute-api.us-east-1.amazonaws.com/prod/movers";

interface StockMover {
  date: string;
  ticker: string;
  percent_change: number;
  closing_price: number;
}

/**
 * App component that displays a grid of top stock movers with their performance metrics.
 * 
 * Fetches stock mover data from an API and renders them in a responsive grid layout.
 * The first item spans 3 columns, while remaining items are distributed across a 3-column grid.
 * 
 * Features:
 * - Displays stock ticker, date, percent change, and closing price
 * - Color-codes gains (green) and losses (red)
 * - Applies hover effects with shadow animations
 * - Special glow shadow effect for the featured top mover
 * 
 * @component
 * @returns {React.ReactElement} A styled container with stock mover cards
 */
function App() {
  const [movers, setMovers] = useState<StockMover[]>([]);
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  useEffect(() => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => setMovers(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>Top Stock Movers</h1>
      <p style={styles.subtitle}>Last 7 Market Days</p>

      <div style={styles.grid}>
        {movers.map((item, index) => {
          const isPositive = item.percent_change >= 0;
          const placement =
          index === 0
            ? { gridColumn: "1 / 4" }
            : index === 1
            ? { gridColumn: "1 / 2" }
            : index === 2
            ? { gridColumn: "2 / 3" }
            : index === 3
            ? { gridColumn: "3 / 3" }
            : index === 4
            ? { gridColumn: "1 / 1" }
            : index === 5
            ? { gridColumn: "2 / 3" }
            : index === 6
            ? { gridColumn: "3 / 3" }
            : {};

          return (
            <div
              key={index}
              style={{ ...styles.card, 
                ...(hoveredIndex === index ? styles.cardHover : {}), 
                boxShadow: index === 0 
                ? isPositive 
                  ? "0 0 25px rgba(220, 252, 231, 0.4)" 
                  : "0 0 25px rgba(254, 226, 226, 0.4)" 
                : "0 10px 25px rgba(0,0,0,0.3)", 
                ...placement
              }}
              onMouseEnter={() => setHoveredIndex(index)}
              onMouseLeave={() => setHoveredIndex(null)}
            >
              <div style={styles.date}>{item.date}</div>
              <div style={styles.ticker}>{item.ticker}</div>

              <div
                style={{
                  ...styles.percent,
                  color: isPositive ? "#16a34a" : "#dc2626",
                  backgroundColor: isPositive ? "#dcfce7" : "#fee2e2",
                }}
              >
                {isPositive ? "+" : ""}
                {item.percent_change}%
              </div>

              <div style={styles.price}>
                Closing: ${item.closing_price}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  page: {
    minHeight: "100vh",
    width: "100%",
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
    padding: "20px 20px",
    fontFamily: "Inter, system-ui, sans-serif",
    color: "white",
    textAlign: "center",
    boxSizing: "border-box",
  },
  title: {
    fontSize: "3.2rem",
    marginBottom: "10px",
    marginTop: "10px",
  },
  subtitle: {
    opacity: 0.7,
    marginBottom: "35px",
    marginTop: "0",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: "20px",
    maxWidth: "1100px",
    margin: "0 auto",
  },
  card: {
    background: "#1e293b",
    padding: "15px",
    borderRadius: "16px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.3)",
    cursor: "pointer",
    transition: "transform 0.25s ease, box-shadow 0.25s ease"
  },
  cardHover: {
    transform: "scale(1.03)",
  },
  date: {
    fontSize: "0.9rem",
    opacity: 0.6,
    marginBottom: "10px",
  },
  ticker: {
    fontSize: "2.3rem",
    fontWeight: "bold",
    marginBottom: "5px",
    marginTop: "5px",
  },
  percent: {
    display: "inline-block",
    padding: "6px 12px",
    borderRadius: "999px",
    fontWeight: "bold",
    marginBottom: "10px",
  },
  price: {
    opacity: 0.8,
  },
};

export default App;