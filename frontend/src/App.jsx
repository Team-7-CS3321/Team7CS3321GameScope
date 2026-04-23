import { useState } from "react";
import logo from "./assets/Gamescope_Image.png"; // 👈 make sure filename matches

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);

  const handleSearch = async () => {
    try {
      console.log("Searching for:", query);

      const response = await fetch(
        `http://localhost:8000/report/?game_name=${query}`
      );

      const data = await response.json();
      console.log("DATA:", data);

      setResults(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

const getDifficultyLabel = (score) => {
  if (score <= 20) return "Very Easy";
  if (score <= 40) return "Easy";
  if (score <= 60) return "Moderate";
  if (score <= 80) return "Hard";
  return "Very Hard";
};

  return (
    <div style={{ textAlign: "center", marginTop: "40px" }}>
      
      {/* HEADER */}
      <div>
        <img src={logo} alt="GameScope Logo" style={{ width: "220px", marginBottom: "5px" }} />
      </div>

      {/* SEARCH */}
      <input
        type="text"
        placeholder="Search for a game..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <br /><br />

      <button onClick={handleSearch}>Search</button>

      {/* RESULTS */}
      {results?.data?.game && (
        <div>
          <h2>{results.data.game.name}</h2>

          <p>
            <strong>Release Date:</strong>{" "}
            {results.data.game.release_date}
          </p>

          <p>
            <strong>Rating:</strong>{" "}
            {results.data.game.rating}
          </p>

          <p>
            <strong>Genres:</strong>{" "}
            {results.data.game.genres.join(", ")}
          </p>

          <p>
            <strong>Achievements:</strong>{" "}
            {results.data.game.achievement_count}
          </p>

          <p>{results.data.game.description}</p>

	<p>
	  <strong>Difficulty:</strong>{" "}
	  {getDifficultyLabel(results.data.game.difficulty_score)} (
	  {results.data.game.difficulty_score})
	</p>

	<div style={{
	  width: "100%",
	  backgroundColor: "#ddd",
	  borderRadius: "8px",
	  overflow: "hidden",
	  marginBottom: "10px"
	}}>
	  <div
	    style={{
	      width: `${results.data.game.difficulty_score}%`,
	      backgroundColor: "orange",
	      height: "20px"
	    }}
	  />
	</div>

          <h3>Top Achievements:</h3>
          {results.data.game.achievements
            ?.slice(0, 5)
            .map((ach, index) => (
              <div key={index}>
                <p>
                  {ach.display_name} - {ach.global_percentage}%
                </p>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}

export default App;
