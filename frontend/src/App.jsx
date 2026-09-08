import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [stats, setStats] = useState(null);
  const [vehicles, setVehicles] = useState([]);

  const fetchData = () => {
    fetch("http://localhost:8080/api/stats")
      .then((response) => response.json())
      .then((data) => {
        setStats(data);
      })
      .catch((error) => {
        console.error("Error fetching traffic stats:", error)
      });

    fetch("http://localhost:8080/api/vehicles")
      .then((response) => response.json())
      .then((data) => {
        setVehicles(data);
      })
      .catch((error) => {
        console.error("Error fetching vehicles:", error);
      });
  };

  useEffect(() => {
    fetchData();

    const interval = setInterval(fetchData, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Traffic Vision Dashboard</h1>
      <p>Real-time traffic analytics powered by computer vision.</p>

      {stats && (
        <div className="dashboard">
          <h2>Traffic Statistics</h2>

          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Vehicles</h3>
              <p>{stats.totalVehicles}</p>
            </div>

            <div className="stat-card">
              <h3>Average Speed</h3>
              <p>{stats.averageSpeed.toFixed(1)} MPH</p>
            </div>     

            <div className="stat-card">
              <h3>Up</h3>
              <p>{stats.upCount}</p>
             </div>

             <div className="stat-card">
              <h3>Down</h3>
              <p>{stats.downCount}</p>
             </div>

             <div className="stat-card">
              <h3>Cars</h3>
              <p>{stats.carCount}</p>
             </div>

             <div className="stat-card">
              <h3>Trucks</h3>
              <p>{stats.truckCount}</p>
             </div>

             <div className="stat-card">
              <h3>Buses</h3>
              <p>{stats.busCount}</p>
             </div>

             <div className="stat-card">
              <h3>Motorcycles</h3>
              <p>{stats.motorcycleCount}</p>
             </div>
            </div>
          </div>
        )}

        <div className="vehicle-section">
          <h2>Recent Vehicles</h2>

          <table>
            <thead>
              <tr>
                <th>Vehicle ID</th>
                <th>Type</th>
                <th>Direction</th>
                <th>Travel Time</th>
                <th>Speed</th>
              </tr>
            </thead>

            <tbody>
              {vehicles.map((vehicle) => (
                <tr key={vehicle.id}>
                  <td>{vehicle.vehicleId}</td>
                  <td>{vehicle.type}</td>
                  <td>{vehicle.direction}</td>
                  <td>{vehicle.travelTime.toFixed(2)} s</td>
                  <td>{vehicle.speedMph.toFixed(1)} MPH</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
  );
}

export default App;