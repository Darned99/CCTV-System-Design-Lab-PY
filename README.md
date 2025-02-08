# Comprehensive Documentation of the CCTV System

## Table of Contents
1. Introduction to the Project
   - Project Objectives
   - Brief Description of the System’s Functionality
2. Project Repository
   - Project Structure
3. Project Assumptions
   - Key System Requirements
   - Development Environment Description
   - Technologies and Libraries Used
4. System Block Diagram
   - Components and Their Functions
   - Dependencies Between System Modules
5. Data Flow
   - Step-by-Step Processing of Information Within the System
   - Algorithms Used for Motion Detection and Recording
6. Technical Specification of Components
   - Hardware (Cameras, Switches, Processing Units)
   - Software (Libraries, Development Tools)
7. System Implementation
   - Core Modules and Their Roles
   - Explanation of Critical Parts of the Code
8. User Guide
   - How to Run the System
   - Instructions for Using GUI Application
9. Brief Presentation
   - GUI
   - Appearance of the Grid
   - System Logs

## 1. Introduction to the Project
### Project Objectives
The goal of this project is to develop a scalable CCTV system that provides:
- Real-time video surveillance
- Motion detection and automated recording
- Local storage for captured footage

### Brief Description of the System’s Functionality
The system uses two cameras connected to a laptop for live monitoring and motion detection. When motion is detected, recording is triggered and saved locally. The user can view combined camera feeds and manage recordings through a basic GUI.

## 2. Project Repository
### Project Structure
The repository is organized as follows:
- `src/`: Contains the source code for the CCTV system, including motion detection and video recording logic.
- `docs/`: Holds documentation files such as system design, user guides, and technical specifications.
- `README.md`: Provides an overview of the project, setup instructions, and usage guidelines.

[GitHub Repository](https://github.com/Darned99/CCTV-System-Design-Lab-PY)

## 3. Project Assumptions
### Key System Requirements
- **Cameras**: Two cameras with at least 720p resolution for live monitoring and recording.
- **Processing Unit**: A laptop capable of real-time processing.
- **Power Supply**: Reliable power source for uninterrupted operation.
- **Storage**: At least 10 GB of available space for saving recorded videos in MP4 format.

### Development Environment Description
- **Programming Language**: Python 3.8 or later
- **IDE**: Visual Studio Code with Python extensions or PyCharm
- **Platform**: Windows system for compatibility with OpenCV library

### Technologies and Libraries Used
- **OpenCV**: For video capture, motion detection, and image processing
- **Haar Cascade Classifiers**: For detecting faces and bodies in the video feed
- **Datetime and OS Modules**: For timestamping recordings and managing storage
- **VideoWriter**: For saving video recordings in MP4 format

## 4. System Block Diagram
### System Components and Their Functions
- **Camera Module (IP Camera):**
  - Captures real-time video footage
  - Compatible with USB webcams or IP cameras using RTSP streams
  - Each camera is initialized with an ID or RTSP URL
- **Processing Unit (Workstation):**
  - Analyzes video frames from both cameras using pre-trained Haar cascades for face and body detection
  - Operates in two modes:
    - **Motion detection mode**: Triggers recording when motion is detected
    - **Continuous recording mode**: Records video continuously
  - Handles frame resizing and merging for GUI display  
- **Storage Module:**
  - Saves all recordings in a local folder named `Videos`
  - File naming format: `camera_id_date_hour.mp4`
- **GUI Application (User Interface):**
  - Displays live video feeds from all connected cameras in a 2x2 grid
  - Allows mode switching using keyboard inputs:
    - `1` for motion detection mode
    - `2` for continuous recording mode
    - `q` to exit the program

## 5. Data Flow
1. Each camera captures video frames and sends them to the processing unit.
2. Frames are converted to grayscale for motion analysis. Haar Cascade classifiers detect faces and bodies.
3. If motion is detected in **Mode 1**, recording is triggered and continues for a predefined duration after motion stops.
4. In **Mode 2**, the system records continuously without motion detection.
5. All video streams are displayed in separate OpenCV windows for live monitoring.
6. The program can be terminated manually by pressing the `q` key, which releases all resources.

## 6. Technical Specification of Components
### Hardware
- **Cameras**: USB webcams or IP cameras (RTSP supported).
- **Example RTSP URL**: `rtsp://username:password@192.168.1.67:554/Streaming/Channels/2`

### Software
- **Motion Detection Algorithm**:
  - Haar Cascade Classifiers:
    - `haarcascade_frontalface_default.xml` (for face detection)
    - `haarcascade_fullbody.xml` (for body detection)
  - **Resolution**: Frames processed with at least 480p resolution, 720p recommended
- **File Management**:
  - Videos saved in MP4 format using OpenCV's `VideoWriter`

## 7. System Implementation
### Core Modules and Their Roles
- **CameraMonitor Class (`cctv_project.py`)**:
  - Manages cameras, motion detection, and recording.
  - Supports two modes:
    - **Motion Detection Mode**: Detects faces and bodies using Haar Cascade and triggers recording.
    - **Continuous Recording Mode**: Records video streams without analysis.
  - Saves recordings in the `Videos` folder with timestamps.
- **Main Script (`run_cameras.py`)**:
  - Initializes cameras (local or RTSP) and manages their operation.
  - Enables dynamic switching between modes via keyboard inputs (`1`, `2`).
  - Displays live camera feeds in OpenCV windows.

## 8. User Guide
### Installation Requirements
1. Ensure Python 3.8 or later is installed.
2. Install required dependencies using:
   ```sh
   pip install opencv-python
   pip install numpy
   ```
3. Connect cameras (USB or IP) and ensure they are operational.

### Running the System
1. Navigate to the project folder and execute:
   ```sh
   python src/run_cameras.py
   ```
2. Enter the number of cameras and provide their identifiers (`0, 1` for USB or RTSP URL for IP cameras).

### Instructions for Using GUI Application
- The system displays a grid view for all camera feeds.
- Use the following keyboard commands:
  - `1` – Enable motion detection mode (default mode)
  - `2` – Enable continuous recording mode
  - `q` – Exit the application and release resources
- Recorded videos are stored in the `Videos/` directory, and after **7 days**, they are automatically deleted.

### Troubleshooting
- **If an IP camera does not load**, test its stream manually.
- **If recordings are not saved**, check the `Videos/` directory permissions.
- **If recordings are saved but are damaged**, try changing the width and height settings in the `CameraMonitor` class located in `cctv_project.py`.
- **Debugging logs** are printed in the terminal for further issue diagnosis.

## 9. Brief presentation
###The following are important elements of the system during commissioning such as: 
1. GUI with the grid of 2x2
![image](https://github.com/user-attachments/assets/e8ddf156-7c66-48bc-a1c0-20f3c3812479)
2. Saved video files in the Videos directory
![image](https://github.com/user-attachments/assets/4754f471-a5dc-4b5a-bc6e-f5551078c3bf)
![image](https://github.com/user-attachments/assets/824e9f86-998a-4f1d-a22b-e049810baf8b)
3. Display of system logs
![image](https://github.com/user-attachments/assets/c080d698-9250-4035-a757-06d6b4b6fa34)




