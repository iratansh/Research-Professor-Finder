import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate, useParams } from "react-router-dom";

export default function Home() {
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState("");
  
    const handleSearch = (event) => {
      if (event.key === "Enter" && searchQuery.trim() !== "") {
        navigate(`/search/${searchQuery}`);
      }
    };
  
    return (
      <div className="content">
        <h1 className="header">Research Prof Finder</h1>
        <input
          className="search-bar"
          type="text"
          placeholder="Enter Professor or Research Interests..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleSearch}
        />
      </div>
    );
  };