import React, { useState, useEffect } from "react";

export default function EmailTips({ keyWords }, name) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch("http://localhost:8000/email-tips", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ keywords: [keyWords] }),
        });

        if (!response.ok) {
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
      <h1 className="header">
        Email Tips for <p style={{ textTransform: "capitalize" }}>{name}</p>
      </h1>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: "red" }}>Error: {error}</p>
      ) : results && results.length > 0 ? (
        <ul>
          {/* Todo : display the results */}
        </ul>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}
