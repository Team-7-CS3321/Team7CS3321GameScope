import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const searchGames = async () => {
    try {
      const res = await fetch(`http://localhost:8000/search?query=${query}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>🎮 GameScope</h1>

      <input
        type="text"
        placeholder="Search for a game..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button onClick={searchGames}>Search</button>

      <ul>
        {results.map((game, index) => (
          <li key={index}>{game.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
