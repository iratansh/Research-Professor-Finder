import React, { useState, useEffect } from "react";
import ResultsPage from "./ResultsPage";  // Import ResultsPage

const SearchResults = ({ searchQuery }) => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch("http://localhost:8000/match-professors", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ keywords: [searchQuery] }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Network response was not ok");
        }

        const data = await response.json();
        console.log(data);

        if (data.status === "success") {
          setResults(data.results);  // Assuming data.results contains the professors
        } else {
          throw new Error("Error fetching results");
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [searchQuery]);
  let results2 = {JohnAdams: 0, ConnorMcnugget: 6, MilesMorales:7}
  return (
    <div className="content">
      <h1 className="header">Results for "{searchQuery}"</h1>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: "red" }}>Error: {error}</p>
      ) : results && results.length > 0 ? (
        <ResultsPage data={results2} />  // Call ResultsPage and pass results as data
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
};

export default SearchResults;
