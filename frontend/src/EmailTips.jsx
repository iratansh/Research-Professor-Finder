import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";

export default function EmailTips({ keywords, name }) {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!keywords) {
      console.log("No keywords provided, skipping fetch.");
      return;
    }

    let isSubscribed = true;
    const fetchResults = async () => {
      console.log("Fetching email tips with keywords:", keywords);
      setLoading(true);
      setError(null);

      const keywordsPayload = Array.isArray(keywords) ? keywords : [keywords];

      try {
        const minimumLoadingTime = 30000;
        const startTime = Date.now();

        const response = await fetch("http://localhost:8000/email-tips", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ keywords: keywordsPayload, name: name }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Network response was not ok");
        }

        const data = await response.json();
        console.log("Received data:", data);

        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, minimumLoadingTime - elapsedTime);

        setTimeout(() => {
          if (isSubscribed) {
            if (data.status === "success") {
              console.log("Setting results:", data.tips);
              setResults(data); 
              setLoading(false);
            } else {
              throw new Error("Error fetching results");
            }
          }
        }, remainingTime);

      } catch (err) {
        console.error("Error in fetchResults:", err);
        if (isSubscribed) {
          setError(err.message);
          setLoading(false);
        }
      }
    };

    fetchResults();

    return () => {
      isSubscribed = false;
    };
  }, [keywords]);

  console.log("Current state:", { results, loading, error });

  return (
    <div className="w-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg min-h-[200px]">
      <div className="p-8">
        <h2 className="text-2xl font-bold mb-6">
          Email Tips for <span className="capitalize">{name}</span>
        </h2>
        
        {loading ? (
          <div className="space-y-4">
            <div className="flex items-center justify-center space-x-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
              <span className="text-gray-600">Generating email tips...</span>
            </div>
            <div className="h-2 bg-gray-200 rounded overflow-hidden">
              <div className="h-full bg-blue-500 animate-pulse"></div>
            </div>
          </div>
        ) : error ? (
          <div className="p-4 bg-red-100 text-red-700 rounded-lg">
            Error: {error}
          </div>
        ) : results?.status === 'success' ? (
          <div className="prose max-w-none">
            <div className="p-6 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 whitespace-pre-wrap text-gray-800 leading-relaxed">
              <ReactMarkdown>{results.tips}</ReactMarkdown>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-600 p-4">
            No results found.
          </div>
        )}
      </div>
    </div>
  );
}
