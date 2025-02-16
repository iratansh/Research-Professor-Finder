import React, { useState, useEffect } from "react";

const SearchResults = ({ searchQuery }) => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      setError(null);
      try {
        // Use localhost rather than 0.0.0.0 for the client request.
        const response = await fetch("http://localhost:8000/match-professors", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ keywords: [searchQuery] }),
        });

        if (!response.ok) {
          // Attempt to read the error detail from the backend
          const errorData = await response.json();
          throw new Error(errorData.detail || "Network response was not ok");
        }

        const data = await response.json();
        console.log(data);

        if (data.status === "success") {
          setResults(data.results);
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

  return (
    <div className="content">
      <h1 className="header">Results for "{searchQuery}"</h1>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: "red" }}>Error: {error}</p>
      ) : results && results.length > 0 ? (
        <ul>
          {results.map((professor, index) => (
            <li key={index}>
              {professor.name} - Score: {professor.score}
            </li>
          ))}
        </ul>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
};

export default SearchResults;
