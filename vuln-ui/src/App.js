import { useState } from "react";
import Hero from "./pages/Hero";
import Chat from "./pages/Chat";

function App() {
  const [showHero, setShowHero] = useState(true);

  return showHero ? (
    <Hero onFinish={() => setShowHero(false)} />
  ) : (
    <Chat />
  );
}

export default App;