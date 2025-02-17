import React, { useEffect, useState } from "react";

export default function ProfData(primaryK) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch("http://localhost:8000/info", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ primary_key: [primaryK] }),
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
    <div>
      <h1>Name</h1>
      <div class="basic">Title | Email | Num | Location</div>
      <div class="bio"></div>
      <div class="tips"></div>
    </div>
  );
};
