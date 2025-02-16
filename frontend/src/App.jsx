import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import "./App.css";

const researchIcons = ["📖", "💻", "📜", "📊", "💡", "🖊️"];

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

const Home = () => {
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
        placeholder="Search Professor..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onKeyDown={handleSearch}
      />
    </div>
  );
};

const SearchResults = ({ searchQuery }) => {
  return (
    <div className="content">
      <h1 className="header">Results for "{searchQuery}"</h1>
      <p>Displaying search results...</p>
    </div>
  );
};

const SearchPage = () => {
  const { searchQuery } = useParams();
  return <SearchResults searchQuery={searchQuery} />;
};

function App() {
  return (
    <Router>
      <FloatingIcons />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/search/:searchQuery" element={<SearchPage />} />
      </Routes>
    </Router>
  );
}

export default App;
