package com.trafficvision.backend;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/stats")
public class TrafficStatsController {

    private final VehicleRepository vehicleRepository;

    public TrafficStatsController(VehicleRepository vehicleRepository) {
        this.vehicleRepository = vehicleRepository;
    }

    @GetMapping 
    public Map<String, Object> getStats() {

        List<Vehicle> vehicles = vehicleRepository.findAll();

        int totalVehicles = vehicles.size();

        double averageSpeed = vehicles.stream()
            .mapToDouble(Vehicle::getSpeedMph)
            .average()
            .orElse(0.0);

        
        long upCount = vehicles.stream()
                .filter(vehicle -> "Up".equalsIgnoreCase(vehicle.getDirection()))
                .count();

        long downCount = vehicles.stream()
                .filter(vehicle -> "Down".equalsIgnoreCase(vehicle.getDirection()))
                .count();

        long carCount = vehicles.stream()
                .filter(vehicle -> "car".equalsIgnoreCase(vehicle.getType()))
                .count();

        long truckCount = vehicles.stream()
                .filter(vehicle -> "truck".equalsIgnoreCase(vehicle.getType()))
                .count();

        long busCount = vehicles.stream()
                .filter(vehicle -> "bus".equalsIgnoreCase(vehicle.getType()))
                .count();

        long motorcycleCount = vehicles.stream()
                .filter(vehicle -> "motorcycle".equalsIgnoreCase(vehicle.getType()))
                .count();

            
        return Map.of(
            "totalVehicles", totalVehicles,
            "averageSpeed", averageSpeed,
            "upCount", upCount,
            "downCount", downCount,
            "carCount", carCount,
            "truckCount", truckCount,
            "busCount", busCount,
            "motorcycleCount", motorcycleCount
        );
    }
}