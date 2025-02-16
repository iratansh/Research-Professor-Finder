import React, { useEffect, useState } from "react";
import "./ResultsPage.css";

const ResultsPage = ({ data }) => {
  const professorNames = Object.keys(data).filter((key) => key !== "status");
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (event) => {
      setMousePosition({ x: event.clientX, y: event.clientY });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <div className="results-page">
      {/* Flashlight div follows cursor */}
      <div
        className="flashlight"
        style={{ top: `${mousePosition.y}px`, left: `${mousePosition.x}px` }}
      ></div>

      <div className="results-container">
        <h1 className="results-header">Professor Results</h1>
        <div className="professor-list">
          {professorNames.length > 0 ? (
            professorNames.map((professorName) => (
              <div className="professor-item" key={professorName}>
                {professorName}
              </div>
            ))
          ) : (
            <div className="no-results">No professors found</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
