import { useState } from "react";
import logo from "./assets/Gamescope_Image.png";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [zoomed, setZoomed] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedAchievement, setSelectedAchievement] = useState(null);

  const handleSearch = async (customQuery) => {
    const searchTerm =
      typeof customQuery === "string" ? customQuery : query;

    try {
      setLoading(true);
      setResults(null);

      const API =
        import.meta.env.VITE_API_URL || "http://localhost:8000";

      const response = await fetch(
        `${API}/report/?game_name=${searchTerm}`
      );
      const data = await response.json();

      // ❗ NO RESULTS
      if (!data?.data?.game) {
        setResults({ error: "No results found" });
        setRecommendations([]);
        return;
      }

      setResults(data);

      // 🔥 Recommendations
      const genres = data.data.game.genres
        .map((g) => g.toLowerCase())
        .join(",");

      const recRes = await fetch(
        `${API}/report/recommend/?genres=${genres}`
      );
      const recData = await recRes.json();

      setRecommendations(recData.results || []);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
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
    <div className="layout">
      {/* LEFT SIDEBAR */}
      {results?.data?.game && (
        <div className="sidebar">
          <h3>All Achievements</h3>

          {/* SCROLLABLE ACHIEVEMENTS */}
          <div className="achievements-scroll">
            {results.data.game.achievements?.length > 0 ? (
              results.data.game.achievements
                .sort(
                  (a, b) =>
                    parseFloat(a.global_percentage) -
                    parseFloat(b.global_percentage)
                )
                .map((ach, index) => (
                  <div
                    className="achievement"
                    key={index}
                    onClick={() => setSelectedAchievement(ach)}
                    style={{ cursor: "pointer" }}
                  >
                    <img
                      src={ach.icon}
                      alt="icon"
                      className="achievement-icon"
                    />
                    <span>
                      {ach.display_name} - {ach.global_percentage}%
                    </span>
                  </div>
                ))
            ) : (
              <p>No achievements available.</p>
            )}
          </div>

          {/* ✅ RECOMMENDED SECTION (SEPARATE CARD) */}
          <div className="recommended-section">
            <h3>Recommended Games</h3>

            {recommendations.length > 0 ? (
              recommendations.map((game, index) => (
                <div
                  key={index}
                  className="achievement"
                  onClick={() => {
                    setQuery(game.name);
                    handleSearch(game.name);
                  }}
                  style={{ cursor: "pointer" }}
                >
                  {game.cover_art && (
                    <img
                      src={game.cover_art}
                      className="achievement-icon"
                    />
                  )}
                  <span>{game.name}</span>
                </div>
              ))
            ) : (
              <p>No recommendations available.</p>
            )}
          </div>
        </div>
      )}

      {/* ✅ ACHIEVEMENT POPUP */}
      {selectedAchievement && (
        <div
          className="overlay"
          onClick={() => setSelectedAchievement(null)}
        >
          <div
            className="card"
            onClick={(e) => e.stopPropagation()}
          >
            <h2>{selectedAchievement.display_name}</h2>

            {selectedAchievement.icon && (
              <img
                src={selectedAchievement.icon}
                className="achievement-icon"
                style={{ width: "64px", height: "64px" }}
              />
            )}

            <p>
              {selectedAchievement.description ||
                "No description available"}
            </p>

            <p>
              <strong>Global Completion:</strong>{" "}
              {selectedAchievement.global_percentage}%
            </p>
          </div>
        </div>
      )}

      {/* RIGHT MAIN AREA */}
      <div className="main">
        <div className="search-section">
          <img src={logo} alt="GameScope Logo" className="logo" />

          <input
            className="search-box"
            type="text"
            placeholder="Search for a game..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <button className="button" onClick={handleSearch}>
            Search
          </button>

          {loading && <div className="loader"></div>}

          {/* ❗ NO RESULTS DISPLAY */}
          {results?.error && (
            <div className="card">
              <h2>No results found</h2>
              <p>Try a different game name.</p>
            </div>
          )}

          {/* ✅ GAME DISPLAY */}
          {results?.data?.game && (
            <div className={`card ${loading ? "dim" : ""}`}>
              <h2>{results.data.game.name}</h2>

              {results.data.game.cover_art && (
                <>
                  <img
                    src={results.data.game.cover_art}
                    alt="Game Cover"
                    className="game-image"
                    onClick={() => setZoomed(true)}
                  />

                  {zoomed && (
                    <div
                      className="overlay"
                      onClick={() => setZoomed(false)}
                    >
                      <img
                        src={results.data.game.cover_art}
                        className="zoomed-full"
                      />
                    </div>
                  )}
                </>
              )}

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

              {/* ✅ Difficulty OR fallback */}
              {results.data.game.achievement_count > 0 ? (
                <>
                  <p>
                    <strong>Difficulty:</strong>{" "}
                    {getDifficultyLabel(
                      results.data.game.difficulty_score
                    )}{" "}
                    ({results.data.game.difficulty_score})
                  </p>

                  <div className="difficulty-bar">
                    <div
                      className="difficulty-fill"
                      style={{
                        width: `${results.data.game.difficulty_score}%`,
                      }}
                    />
                  </div>
                </>
              ) : (
                <p>No achievements → difficulty not available.</p>
              )}

              <h3>Top Achievements (Hardest)</h3>

              {results.data.game.achievements?.length > 0 ? (
                results.data.game.achievements
                  .sort(
                    (a, b) =>
                      parseFloat(a.global_percentage) -
                      parseFloat(b.global_percentage)
                  )
                  .slice(0, 5)
                  .map((ach, index) => (
                    <div className="achievement" key={index}>
                      <img
                        src={ach.icon}
                        alt="icon"
                        className="achievement-icon"
                      />
                      <span>
                        {ach.display_name} -{" "}
                        {ach.global_percentage}%
                      </span>
                    </div>
                  ))
              ) : (
                <p>No achievements available.</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;