import { useEffect, useState } from "react";
import "./App.css";


const App = () => {
  const [users, setUsers] = useState([]);
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [firstUser, setFirstUser] = useState(null);
  const [firstPlayer, setFirstPlayer] = useState(null);


  useEffect(() => {
    Promise.all([
      fetch("http://127.0.0.1:8000/api/users/").then((res) => res.json()),
      fetch("http://127.0.0.1:8000/api/players/").then((res) => res.json()),
    ])
      .then(([usersData, playersData]) => {
        setUsers(usersData);
        setPlayers(playersData);
        setLoading(false);

        // pobranie pierwszego użytkownika
        if (usersData.length > 0) {
          fetch(`http://127.0.0.1:8000/api/users/${usersData[0].id}/`)
            .then((res) => res.json())
            .then((userData) => setFirstUser(userData))
            .catch((err) => console.error("Błąd pobierania pierwszego użytkownika:", err));
        }

        // pobranie pierwszego piłkarza
        if (playersData.length > 0) {
          fetch(`http://127.0.0.1:8000/api/players/${playersData[0].id}/`)
            .then((res) => res.json())
            .then((playerData) => setFirstPlayer(playerData))
            .catch((err) => console.error("Błąd pobierania pierwszego piłkarza:", err));
        }
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);


  return (
    <div className="container">
      <h1>Lista użytkowników</h1>
      {loading && <p>Ładowanie...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <strong>{user.login}</strong> ({user.email})
          </li>
        ))}
      </ul>

      <h2>Pierwszy użytkownik</h2>
      {firstUser ? (
        <p>
          <strong>{firstUser.login}</strong> ({firstUser.email})
        </p>
      ) : (
        <p>Brak danych o pierwszym użytkowniku</p>
      )}

      <h1>Lista piłkarzy</h1>
      <ul>
        {players.map((player) => (
          <li key={player.id}>
            <strong>{player.name}</strong> - Klub: {player.club_name}, Liga: {player.league_name}, Kraj: {player.country_name},
            Pozycja: {player.position_name}, Wiek: {player.age_value}, Numer: {player.shirt_number_value}
          </li>
        ))}
      </ul>

      <h2>Pierwszy piłkarz</h2>
      {firstPlayer ? (
        <p>
          <strong>{firstPlayer.name}</strong> - Klub: {firstPlayer.club_name}, Liga: {firstPlayer.league_name}, Kraj:{" "}
          {firstPlayer.country_name}, Pozycja: {firstPlayer.position_name}, Wiek: {firstPlayer.age_value}, Numer:{" "}
          {firstPlayer.shirt_number_value}
        </p>
      ) : (
        <p>Brak danych o pierwszym piłkarzu</p>
      )}
    </div>
  );
};

export default App;
