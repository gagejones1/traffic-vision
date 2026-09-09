import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import "./App.css";

function App() {
  const [stats, setStats] = useState(null);
  const [vehicles, setVehicles] = useState([]);
  const [error, setError] = useState(null);

  const fetchData = () => {
    fetch("http://localhost:8080/api/stats")
      .then((response) => response.json())
      .then((data) => {
        setStats(data);
        setError(null);
      })
      .catch((error) => {
        console.error("Error fetching traffic stats:", error)
        setError("Unable to connect to the backend.");
      });

    fetch("http://localhost:8080/api/vehicles")
      .then((response) => response.json())
      .then((data) => {
        setVehicles(data);
        setError(null);
      })
      .catch((error) => {
        console.error("Error fetching vehicles:", error);
        setError("Unable to connect to the backend.");
      });
  };

  useEffect(() => {
    fetchData();

    const interval = setInterval(fetchData, 3000);

    return () => clearInterval(interval);
  }, []);

  const vehicleTypeData = stats 
    ? [
      { name: "Cars", count: stats.carCount },
      { name: "Trucks", count: stats.truckCount },
      { name: "Buses", count: stats.busCount },
      { name: "Moto", count: stats.motorcycleCount }
    ]
  : [];

  const directionData = stats 
    ? [
        { name: "Up", count: stats.upCount },
        { name: "Down", count: stats.downCount }
    ]
  : [];

  return (
    <div>
      <h1>Traffic Vision Dashboard</h1>
      <p>Real-time traffic analytics powered by computer vision.</p>

      {error && (
        <p className="error-message">{error}</p>
      )}

      {!stats && !error && (
        <p className="loading-message">Loading traffic data...</p>
      )}

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

      <div className="charts-grid">

        <div className="chart-section">
          <h2>Vehicle Types</h2>

          <div className="chart-card">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={vehicleTypeData}>
                <XAxis dataKey="name" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-section">
          <h2>Traffic Direction</h2>

          <div className="chart-card">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={directionData}>
                <XAxis dataKey="name" interval={0} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count" fill="#22c55e" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

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
              {vehicles.slice(-10).reverse().map((vehicle) => (
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