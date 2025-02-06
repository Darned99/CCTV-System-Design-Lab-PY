import cv2
import datetime
import numpy as np
from pathlib import Path
from cctv_project import CameraMonitor

def combine_frames(frames, grid_size=(2, 2)):
    rows, cols = grid_size
    blank_frame = np.zeros_like(frames[0])  # Placeholder for missing frames

    # Ensure we have enough frames to fill the grid
    while len(frames) < rows * cols:
        frames.append(blank_frame)

    # Resize frames for consistent grid layout
    frame_height, frame_width = frames[0].shape[:2]
    resized_frames = [cv2.resize(frame, (frame_width, frame_height)) for frame in frames]

    # Split frames into rows
    grid_rows = [np.hstack(resized_frames[i * cols:(i + 1) * cols]) for i in range(rows)]

    # Combine rows into final grid
    grid = np.vstack(grid_rows)
    return grid

def main():
    num_cameras = int(input("Enter the number of cameras to initialize: "))

    # Example camera sources:
    # 0,  # Local camera
    # 1,  # Local camera
    # 'rtsp://admin:hikvision0987@192.168.1.67:554/Streaming/Channels/2',  # RTSP stream
    # 'rtsp://admin:hikvision0987@192.168.1.68:554/Streaming/Channels/2',  # RTSP stream

    camera_sources = []
    for i in range(num_cameras):
        camera_id = input(f"Enter the camera ID {i+1} (e.g., 0, 1, or RTSP stream URL): ")
        if camera_id.isdigit():
            camera_sources.append(int(camera_id))
        else:
            camera_sources.append(camera_id)

    # Initialize camera instances
    camera_monitors = [CameraMonitor(source) for source in camera_sources]

    try:
        print("Starting camera monitoring. Press '1' for motion detection, '2' for continuous recording, 'q' to quit.")
        while True:
            frames = []

            for monitor in camera_monitors:
                # process_frame method handles frames and recording
                frame = monitor.process_frame()
                if frame is not None:
                    frames.append(frame)

            if frames:
                # Display the grid as a single window
                combined_frame = combine_frames(frames, grid_size=(2, 2))
                cv2.imshow("Camera Grid", combined_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('1'):
                print("Switched to motion detection mode.")
                for monitor in camera_monitors:
                    monitor.set_mode(1)
            elif key == ord('2'):
                print("Switched to continuous recording mode.")
                for monitor in camera_monitors:
                    monitor.set_mode(2)
            elif key == ord('q'):
                break

    finally:
        print("Stopping monitoring and releasing resources...")
        for monitor in camera_monitors:
            frame = monitor.process_frame()
            if frame is not None:
                frames.append(frame)
        else:
            print(f"Camera {monitor.camera_id} did not return a frame.")

if __name__ == "__main__":
    main()
