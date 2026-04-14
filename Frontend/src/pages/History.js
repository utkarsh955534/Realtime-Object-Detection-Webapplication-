import { useEffect, useState } from "react";
import axios from "axios";

export default function History() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API}/api/history/`,
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token")
            }
          }
        );

        setData(res.data);

      } catch (err) {
        console.log("ERROR:", err);   // 🔥 important
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="container">
      <h2>History</h2>

      {data.map((item, index) => (
        <div key={index} className="card" style={{ marginBottom: "20px" }}>
          
          <h4>📁 {item.file}</h4>

          {item.detections.map((d, i) => (
            <p key={i}>
              🧠 <b>{d.class}</b> → {(d.confidence * 100).toFixed(1)}%
            </p>
          ))}

        </div>
      ))}
    </div>
  );
}
