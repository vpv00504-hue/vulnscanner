import { useEffect } from "react";

export default function Hero({ onFinish }) {

  useEffect(() => {
    const timer = setTimeout(() => {
      onFinish();
    }, 4000); // 4 seconds

    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <section className="hero-container">

      {/* Background animation */}
      <iframe
        src="https://www.unicorn.studio/embed/NMRiXfKy3YEmt17mbSx0"
        title="Hero background"
        className="hero-bg"
      />

      {/* Overlay */}
      <div className="overlay"></div>

      {/* Content */}
      <div className="hero-content">
        <div className="logo">🛡️</div>

        <h1>VulnScanner</h1>

        <p>AI-powered C Code Vulnerability Detection</p>

        <div className="loader"></div>
      </div>

    </section>
  );
}