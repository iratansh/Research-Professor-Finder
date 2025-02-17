import SearchResults from "./SearchResults";
import Home from "./Home";
import FloatingIcons from "./FloatingIcons";
import ProfData from "./ProfData";
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate, useParams } from "react-router-dom";
import "./App.css";

const SearchPage = () => {
	const { searchQuery } = useParams();
	return <SearchResults searchQuery={searchQuery} />;
};

function App() {
	const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
	useEffect(() => {
		const handleMouseMove = (event) => {
			setMousePosition({ x: event.clientX, y: event.clientY });
		};

		window.addEventListener("mousemove", handleMouseMove);
		return () => {
			window.removeEventListener("mousemove", handleMouseMove);
		};
	}, []);

	return (
		<Router>
			<FloatingIcons />
			<div
				className="flashlight"
				style={{
					top: `${mousePosition.y}px`,
					left: `${mousePosition.x}px`,
				}}
			></div>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/search/:searchQuery" element={<SearchPage />} />
				<Route path="/professor/:id" element={<ProfData />} />
			</Routes>
		</Router>
	);
}

export default App;
