import { useEffect, useRef, useState } from "react";
import axios from "axios";

export default function WebcamDetect() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [detections, setDetections] = useState([]);

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => videoRef.current.srcObject = stream);
  }, []);

  const capture = async () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    ctx.drawImage(videoRef.current, 0, 0, 640, 480);
    const img = canvas.toDataURL("image/jpeg");

    const res = await axios.post(
      `${process.env.REACT_APP_API}/api/detect/webcam`,
      { image: img }
    );

    setDetections(res.data.detections);
  };

  useEffect(() => {
    const interval = setInterval(capture, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card">
      <h3>Live Detection</h3>

      <video ref={videoRef} autoPlay width="400" />
      <canvas ref={canvasRef} width="640" height="480" hidden />

      {detections.map((d,i)=>(
        <p key={i}>
          {d.class} ({(d.confidence*100).toFixed(1)}%)
        </p>
      ))}
    </div>
  );
}
