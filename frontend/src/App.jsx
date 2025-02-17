import SearchResults from "./SearchResults";
import Home from "./Home";
import FloatingIcons from "./FloatingIcons";
import ProfData from "./ProfData";
import { BrowserRouter as Router, Route, Routes, useNavigate, useParams } from "react-router-dom";
import "./App.css";

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
        <Route path="/professor/:id" element={<ProfData />} />
      </Routes>
    </Router>
  );
}

export default App;
