import React, { useState, useEffect } from "react";
import ResultsPage from "./ResultsPage";
import { useNavigate } from "react-router-dom";

const SearchResults = ({ searchQuery }) => {
	const [results, setResults] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);
	const navigate = useNavigate();

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
				<ResultsPage data={results} keywords={searchQuery} />
			) : (
				<view>
					<p>No results found.</p>
					<button title="Return Home" className="btn" onClick={() => navigate("/")}>
						Return Home
					</button>
				</view>
			)}
		</div>
	);
};

export default SearchResults;
