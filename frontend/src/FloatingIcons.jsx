import { useState, useEffect } from "react";

const researchIcons = ["📖", "💻", "📜", "📊", "💡", "🖊️"];

export default function FloatingIcons() {
  const [iconPositions, setIconPositions] = useState([]);

  useEffect(() => {
    // Generate positions once when the component mounts
    const positions = Array.from({ length: 10 }).map(() => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      duration: Math.random() * 10 + 5,
    }));
    setIconPositions(positions);
  }, []); // Empty dependency array ensures this runs only once

  return (
    <div className="research-bg">
      {iconPositions.map((pos, index) => (
        <span
          key={index}
          className="icon"
          style={{
            left: `${pos.x}vw`,
            top: `${pos.y}vh`,
            animationDuration: `${pos.duration}s`,
            fontSize: "2rem",
          }}
        >
          {researchIcons[index % researchIcons.length]}
        </span>
      ))}
    </div>
  );
}
