import { useEffect } from "react";
import "../styles.css";

export default function Hero({ onFinish }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onFinish();
    }, 3000); // 3 sec

    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <div className="hero">

      <div className="hero-box">
        <div className="hero-icon">🛡️</div>

        <h1>VulnScanner</h1>
        <p>AI-powered C code vulnerability detection</p>

        <div className="loader"></div>
      </div>

    </div>
  );
}