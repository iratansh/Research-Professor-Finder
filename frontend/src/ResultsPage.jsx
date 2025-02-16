import React from "react";
import "./ResultsPage.css"; // Import the CSS file for styling

const ResultsPage = ({ data }) => {
  const professorNames = Object.keys(data).filter(key => key !== "status");

  return (
    <div className="results-container">
      <h1 className="results-header">Professor Search Results</h1>
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
  );
};

export default ResultsPage;

