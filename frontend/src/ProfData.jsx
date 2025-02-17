import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./ProfData.css";

const ProfData = () => {
  const location = useLocation();
  const professor = location.state || {};
  const navigate = useNavigate();

  return (
    <div className="prof-data-page">
      <button className="back-button" onClick={() => navigate(-1)}>← Back</button>

      <h1 className="prof-name">{professor.name}</h1>

      {/* Professor Info Box */}
      <div className="prof-info">
        <p><strong>Title:</strong> {professor.title}</p>
        <p><strong>Email:</strong> {professor.email}</p>
        <p><strong>Phone:</strong> {professor.number}</p>
        <p><strong>Location:</strong> {professor.location}</p>
      </div>

      {/* Bio Box */}
      <div className="prof-bio">
        <h2>Biography</h2>
        <p>{professor.bio || "No biography available."}</p>
      </div>

      {/* Tips Box */}
      <div className="prof-tips">
        <h2>Tips for Students</h2>
        <p>{professor.tips || "No tips available."}</p>
      </div>
    </div>
  );
};

export default ProfData;
