import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ResultsPage.css";
import FloatingIcons from "./FloatingIcons";

const ResultsPage = ({ data, keywords }) => {
	const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
	const navigate = useNavigate();

	useEffect(() => {
		const handleMouseMove = (event) => {
			setMousePosition({ x: event.clientX, y: event.clientY });
		};

		window.addEventListener("mousemove", handleMouseMove);
		return () => {
			window.removeEventListener("mousemove", handleMouseMove);
		};
	}, []);

	const handleProfessorClick = (professor) => {
		navigate(`/professor/${professor.id}`, { state: { professor, keywords } });
	};

	return (
		<div className="results-page">
			<FloatingIcons />
			<div
				className="flashlight"
				style={{
					top: `${mousePosition.y}px`,
					left: `${mousePosition.x}px`,
				}}
			></div>

			<div className="results-container">
				<h1 className="results-header">Professor Results:</h1>
				<div className="professor-list">
					{data.length > 0 ? (
						data.map((professor) => (
							<div
								className="professor-item"
								key={professor.id}
								onClick={() => handleProfessorClick(professor)}
								style={{ cursor: "pointer" }}
							>
								<div className="professor-name">{professor.name}</div>
								<div className="professor-title">{professor.title}</div>
								<div className="professor-faculty">{professor.faculty}</div>
							</div>
						))
					) : (
						<div className="no-results">No professors found</div>
					)}
				</div>
			</div>
		</div>
	);
};

export default ResultsPage;
