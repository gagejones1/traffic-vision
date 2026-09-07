package com.trafficvision.backend;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity 
@Table(name = "vehicles")
public class Vehicle {

    @Id 
    private Integer id;

    private Integer vehicleId;
    private String type;
    private String direction;
    private Double crossingTime;
    private Double travelTime;
    private Double speedMph;


    public Integer getId() {
        return id;
    }

    public Integer getVehicleId() {
        return vehicleId;
    }

    public String getType() {
        return type;
    }

    public String getDirection() {
        return direction;
    }

    public Double getCrossingTime() {
        return crossingTime;
    }

    public Double getTravelTime() {
        return travelTime;
    }

    public Double getSpeedMph() {
        return speedMph;
    }
}