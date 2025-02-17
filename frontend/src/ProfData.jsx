import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./ProfData.css";
import EmailTips from "./EmailTips";

const ProfData = () => {
  const location = useLocation();
  const { professor, keywords } = location.state || {};
  const navigate = useNavigate();

  if (!professor) {
    return <p>Professor data not found.</p>;
  }

  return (
    <div className="prof-data-page">
      <button className="back-button" onClick={() => navigate(-1)}>
        ← Back
      </button>

      <h1 className="prof-name">{professor.name}</h1>

      <div className="prof-info">
        <p>
          <strong>Title:</strong> {professor.title}
        </p>
        <p>
          <strong>Email:</strong> {professor.email}
        </p>
        <p>
          <strong>Phone:</strong> {professor.number || "N/A"}
        </p>
        <p>
          <strong>Location:</strong> {professor.location}
        </p>
      </div>

      <div className="prof-bio">
        <h2>Biography</h2>
        <p>{professor.bio || "No biography available."}</p>
      </div>

      <div className="prof-tips">
        <h2>Tips for Students</h2>
        <EmailTips keywords={keywords} name={professor.name} />
      </div>
    </div>
  );
};

export default ProfData;
