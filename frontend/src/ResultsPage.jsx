import React, { useEffect, useState } from "react";
import "./ResultsPage.css";
import FloatingIcons from "./FloatingIcons";

const ResultsPage = ({ data }) => {
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
      <FloatingIcons />
      <div
        className="flashlight"
        style={{ top: `${mousePosition.y}px`, left: `${mousePosition.x}px` }}
      ></div>

      <div className="results-container">
        <h1 className="results-header">Professor Results:</h1>
        <div className="professor-list">
          {data.length > 0 ? (
            data.map((professor, index) => (
              <div className="professor-item" key={index}>
                <div 
                  className="professor-name" 
                  style={{ textAlign: "left", flex: 1 }}
                >
                  {professor.name}
                </div>
                <div 
                  className="professor-title" 
                  style={{ textAlign: "center", flex: 1 }}
                >
                  {professor.title}
                </div>
                <div 
                  className="professor-faculty" 
                  style={{ textAlign: "right", flex: 1 }}
                >
                  {professor.faculty}
                </div>
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
