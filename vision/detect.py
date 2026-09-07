from ultralytics import YOLO
import cv2
import csv
from database import SessionLocal
from models import Vehicle 

model = YOLO("yolo11n.pt")

video_path = "videos/traffic.webm"

csv_path = "traffic_data.csv"

with open(csv_path, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "vehicle_id",
        "type",
        "direction",
        "crossing_time",
        "travel_time",
        "speed_mph"
    ])

cap = cv2.VideoCapture(video_path)

db = SessionLocal()

vehicles = {} 

crossed_vehicles = set()

first_line_crossing = {}
completed_trips = set()

line_1_y = 350
line_2_y = 500

distance_feet = 30

traffic_stats = {
    "total": 0,
    "up": 0,
    "down": 0,
    "car": 0,
    "truck": 0,
    "bus": 0,
    "motorcycle": 0
}

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        break
        
    video_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

    #resize
    frame = cv2.resize(frame, (1280,720))

    results = model.track(
        frame, 
        imgsz=640,
        classes=[2, 3, 5, 7],
        persist=True,
        tracker="bytetrack.yaml",
        verbose=False
    )

    boxes = results[0].boxes

    if boxes.id is not None:
        track_ids = boxes.id.int().cpu().tolist()
        class_ids = boxes.cls.int().cpu().tolist()
        coordinates = boxes.xyxy.cpu().tolist()

        for track_id, class_id, box in zip(track_ids, class_ids, coordinates):
            class_name = model.names[class_id]
            x1, y1, x2, y2 = box

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            if track_id not in vehicles:
                vehicles[track_id] = {
                    "type": class_name,
                    "first_seen": video_time,
                    "last_seen": video_time,
                    "last_center_y": center_y,
                    "class_counts": {class_name: 1}
                }

                print(
                    f"NEW Vehicle ID: {track_id} | "
                    f"Type: {class_name} | "
                    f"First seen: {video_time:.2f}s"
                )
            else:
                previous_y = vehicles[track_id]["last_center_y"]

                vehicles[track_id]["last_seen"] = video_time
                class_counts = vehicles[track_id]["class_counts"]

                # Check if vehicle crossed line 1
                crossed_line_1 = (
                    (previous_y < line_1_y and center_y >= line_1_y)
                    or
                    (previous_y > line_1_y and center_y <= line_1_y)
                )

                # Check if vehicle crossed line 2
                crossed_line_2 = (
                    (previous_y < line_2_y and center_y >= line_2_y)
                    or
                    (previous_y > line_2_y and center_y <= line_2_y)
                )

                # Record the first line crossed
                if track_id not in first_line_crossing:
                    if crossed_line_1:
                        first_line_crossing[track_id] = {
                            "line": 1,
                            "time": video_time
                        }

                    elif crossed_line_2:
                        first_line_crossing[track_id] = {
                            "line": 2,
                            "time": video_time
                        }

                # Check if vehicle reached the opposite line
                elif track_id not in completed_trips:
                    first_line = first_line_crossing[track_id]["line"]
                    first_time = first_line_crossing[track_id]["time"]

                    if first_line == 1 and crossed_line_2:
                        direction = "Down"

                    elif first_line == 2 and crossed_line_1:
                        direction = "Up"

                    else:
                        direction = None

                    if direction is not None:
                        travel_time = video_time - first_time

                        speeds_fps = distance_feet / travel_time
                        speed_mph = speeds_fps * 0.681818

                        vehicles[track_id]["travel_time"] = travel_time
                        vehicles[track_id]["travel_direction"] = direction
                        vehicles[track_id]["speed_mph"] = speed_mph

                        completed_trips.add(track_id)

                        db_vehicle = Vehicle(
                            vehicle_id=track_id,
                            type=vehicles[track_id]["type"],
                            direction=direction,
                            crossing_time=video_time,
                            travel_time=travel_time,
                            speed_mph=speed_mph
                        )

                        db.add(db_vehicle)
                        db.commit()

                        with open(csv_path, "a", newline="") as file:
                            writer = csv.writer(file)

                            writer.writerow([
                                track_id,
                                vehicles[track_id]["type"],
                                direction,
                                round(video_time, 2),
                                round(travel_time, 2),
                                round(speed_mph, 1)
                            ])

                        print(
                            f"TRAVEL TIME | "
                            f"Vehicle ID: {track_id} | "
                            f"Type: {vehicles[track_id]['type']} | "
                            f"Direction: {direction} | "
                            f"Time: {travel_time:.2f}s | "
                            f"Est. Speed: {speed_mph:.1f} MPH"
                        )
                
                    



                if class_name in class_counts:
                    class_counts[class_name] += 1
                else:
                    class_counts[class_name] = 1

                vehicle_type = max(class_counts, key=class_counts.get)
                vehicles[track_id]["type"] = vehicle_type

                if track_id not in crossed_vehicles:
                    direction = None

                    if previous_y < 450 and center_y >= 450:
                        direction = "Down"

                    elif previous_y > 450 and center_y <= 450:
                        direction = "Up"

                    if direction is not None:
                        crossed_vehicles.add(track_id)

                        vehicles[track_id]["direction"] = direction
                        vehicles[track_id]["crossing_time"] = video_time

                        traffic_stats["total"] += 1
                        traffic_stats[direction.lower()] += 1
                        traffic_stats[vehicle_type] += 1

                        print(
                            f"CROSSED | "
                            f"Vehicle ID: {track_id} | "
                            f"Type: {vehicle_type} | "
                            f"Direction: {direction} | "
                            f"Time: {video_time:.2f}s"
                        )            

                vehicles[track_id]["last_center_y"] = center_y
    
    annotated_frame = results[0].plot()

    if boxes.id is not None:
        track_ids = boxes.id.int().cpu().tolist()
        coordinates = boxes.xyxy.cpu().tolist()

        for track_id, box in zip(track_ids, coordinates):
            if track_id in vehicles and "speed_mph" in vehicles[track_id]:
                x1, y1, x2, y2 = box

                speed_mph = vehicles[track_id]["speed_mph"]

                cv2.putText(
                    annotated_frame,
                    f"{speed_mph:.1f} MPH",
                    (int(x1), int(y2) + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

    cv2.line(
        annotated_frame,
        (0, line_1_y),
        (1280, line_1_y),
        (0, 255, 0),
        3
    )

    cv2.line(
        annotated_frame,
        (0, line_2_y),
        (1280, line_2_y),
        (0, 255, 255),
        3
    )

    cv2.putText(
        annotated_frame,
        f"Total: {traffic_stats['total']}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Up: {traffic_stats['up']} | Down: {traffic_stats['down']}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
        
    )

    cv2.putText(
        annotated_frame,
        f"Cars: {traffic_stats['car']} | Trucks: {traffic_stats['truck']}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Buses: {traffic_stats['bus']} | Motorcycles: {traffic_stats['motorcycle']}",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("Traffic Vision", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("\nVehicle Summary")
    
for track_id, data in vehicles.items():
    duration = data["last_seen"] - data['first_seen']

    print(
        f"ID: {track_id} | "
        f"Type: {data['type']} | "
        f"Duration: {duration:.2f}s"
    )