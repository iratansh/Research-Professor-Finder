import React, { useEffect, useState } from "react";
import "./App.css";

const researchIcons = [
  "📖", // Book
  "💻", // Microscope
  "📜", // Research Paper
  "📊", // Data Chart
  "💡", // Idea/Innovation
  "🖊️", // Pen
];

// Floating Research Icons (No Change)
const FloatingIcons = () => {
  const icons = Array.from({ length: 10 }).map((_, index) => {
    const randomX = Math.random() * 100;
    const randomY = Math.random() * 100;
    const randomDuration = Math.random() * 10 + 5;

    return (
      <span
        key={index}
        className="icon"
        style={{
          left: `${randomX}vw`,
          top: `${randomY}vh`,
          animationDuration: `${randomDuration}s`,
          fontSize: "2rem",
        }}
      >
        {researchIcons[index % researchIcons.length]}
      </span>
    );
  });

  return <div className="research-bg">{icons}</div>;
};

// Floating Moving Constellations
const FloatingConstellations = () => {
  const [stars, setStars] = useState([]);
  const [lines, setLines] = useState([]);

  useEffect(() => {
    const numStars = 30; // More but smaller stars
    let starArray = [];
    let lineArray = [];

    for (let i = 0; i < numStars; i++) {
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      starArray.push({ x, y });
    }

    // Connecting some stars randomly
    for (let i = 0; i < numStars - 1; i++) {
      if (Math.random() > 0.7) { // Lower probability for more space between connections
        const x1 = starArray[i].x;
        const y1 = starArray[i].y;
        const x2 = starArray[i + 1].x;
        const y2 = starArray[i + 1].y;
        const length = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
        const angle = Math.atan2(y2 - y1, x2 - x1) * (180 / Math.PI);

        lineArray.push({ x1, y1, length, angle });
      }
    }

    setStars(starArray);
    setLines(lineArray);
  }, []);

  return (
    <div className="constellations">
      {stars.map((star, index) => (
        <div
          key={index}
          className="star"
          style={{
            left: `${star.x}vw`,
            top: `${star.y}vh`,
            animationDelay: `${Math.random() * 5}s`,
          }}
        ></div>
      ))}
      {lines.map((line, index) => (
        <div
          key={index}
          className="constellation-line"
          style={{
            left: `${line.x1}vw`,
            top: `${line.y1}vh`,
            height: "1px",
            width: `${line.length}vw`,
            transform: `rotate(${line.angle}deg)`,
            animationDelay: `${Math.random() * 3}s`,
          }}
        ></div>
      ))}
    </div>
  );
};

function App() {
  return (
    <div className="app">
      <FloatingIcons />
      <FloatingConstellations />
      <div className="content">
        <h1 className="header">Research Prof Finder</h1>
        <input className="search-bar" type="text" placeholder="Search Professor..." />
      </div>
    </div>
  );
}

export default App;

