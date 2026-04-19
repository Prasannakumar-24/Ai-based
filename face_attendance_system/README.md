# Face Recognition Attendance System

A comprehensive face recognition-based attendance system built with Python, featuring real-time face detection, automated attendance marking, and a modern GUI interface.

## Features

- 🖥️ **Modern GUI**: Clean CustomTkinter interface with intuitive controls
- 📸 **Face Registration**: Capture and store face images from webcam
- 🔍 **Real-time Recognition**: Automatic face detection and recognition using DeepFace
- 📊 **Attendance Tracking**: Automatic attendance marking with duplicate prevention
- 💾 **MySQL Database**: Robust data storage with proper relationships
- 📈 **Statistics Dashboard**: View registered users and daily attendance counts
- 🛡️ **Error Handling**: Comprehensive error handling for camera and database issues

## Technology Stack

- **Python 3.8+**
- **DeepFace**: Advanced face recognition library
- **OpenCV**: Computer vision and camera handling
- **CustomTkinter**: Modern GUI framework
- **MySQL**: Relational database management
- **Pillow**: Image processing

## Project Structure

```
face_attendance_system/
├── main.py                 # Main application entry point
├── database.py            # MySQL database operations
├── face_recognition.py    # Face recognition logic with DeepFace
├── gui.py                 # CustomTkinter GUI interface
├── requirements.txt       # Python dependencies
├── database_schema.sql    # MySQL database schema
├── faces/                 # Directory for stored face images
└── README.md             # This file
```

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Webcam/camera device
- MySQL Server 8.0 or higher

### Software Dependencies
- MySQL Server (install from https://dev.mysql.com/downloads/mysql/)
- Python packages (installed via pip)

## Installation & Setup

### Step 1: Clone/Download the Project
```bash
# Navigate to your desired directory
cd /path/to/your/projects

# Create project directory
mkdir face_attendance_system
cd face_attendance_system
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note**: DeepFace requires additional system dependencies. On Windows, you may need to install:
```bash
pip install cmake dlib
```

### Step 3: Setup MySQL Database

#### Option A: Using MySQL Command Line
```sql
# Login to MySQL
mysql -u root -p

# Run the schema file
source database_schema.sql
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Open and run `database_schema.sql`

### Step 4: Configure Database Connection

Edit `database.py` and update the database credentials:
```python
self.host = 'localhost'
self.user = 'your_mysql_username'  # Default: 'root'
self.password = 'your_mysql_password'  # Default: '' (empty for no password)
self.database = 'face_attendance_system'
```

## Usage

### Running the Application
```bash
python main.py
```

### How to Use

#### 1. Register a New User
1. Click **"Register User"** button
2. Enter unique User ID and Full Name
3. Click **"Start Face Capture"**
4. Look at the camera and wait for automatic face capture (10 images)
5. Press 'q' to stop early if needed

#### 2. Start Attendance Monitoring
1. Click **"Start Attendance"** button
2. The system will begin real-time face recognition
3. Recognized faces will automatically mark attendance
4. Press 'q' in the camera window to stop monitoring

#### 3. View Attendance Records
1. Click **"View Attendance"** button to refresh records
2. View recent attendance in the table below
3. Statistics show registered users and today's attendance count

## Key Features Explained

### Face Recognition
- Uses DeepFace with VGG-Face model for accurate recognition
- Compares live camera feed against stored face images
- Configurable similarity threshold (default: 0.6)

### Duplicate Prevention
- Prevents multiple attendance marks for the same person on the same day
- 30-second cooldown between recognitions for the same person

### Error Handling
- Camera access errors
- Database connection issues
- Face detection failures
- File system errors

## Configuration

### Face Recognition Settings
Edit `face_recognition.py` to adjust:
```python
self.recognition_threshold = 0.6  # Face matching confidence threshold
self.cooldown_seconds = 30        # Minimum seconds between recognitions
```

### Camera Settings
The system automatically detects and uses the default camera. For multiple cameras:
```python
cap = cv2.VideoCapture(0)  # Change 0 to 1, 2, etc. for different cameras
```

## Troubleshooting

### Common Issues

#### 1. Camera Not Working
- Ensure camera permissions are granted
- Check if camera is being used by another application
- Try different camera index in code

#### 2. DeepFace Installation Issues
```bash
# Install system dependencies (Windows)
pip install cmake
pip install dlib --verbose

# Alternative: Use conda
conda install -c conda-forge dlib
```

#### 3. MySQL Connection Errors
- Verify MySQL server is running
- Check database credentials in `database.py`
- Ensure database and tables exist

#### 4. GUI Not Starting
- Ensure all dependencies are installed
- Check Python version (3.8+ required)
- Try running with `python3` instead of `python`

### Performance Tips
- Close other camera-using applications
- Ensure good lighting for face recognition
- Register users with clear, well-lit face images
- Use SSD storage for better performance

## Database Schema

### Tables

#### `users`
- `id`: Auto-increment primary key
- `user_id`: Unique user identifier
- `name`: Full name of the user
- `face_image_path`: Path to representative face image
- `created_at`: Registration timestamp

#### `attendance`
- `id`: Auto-increment primary key
- `user_id`: Foreign key to users table
- `name`: User's name at time of attendance
- `check_in_time`: Timestamp of attendance
- `date`: Date of attendance (for duplicate prevention)

## Security Considerations

- Store face images securely
- Use strong MySQL passwords
- Regularly backup database
- Consider encryption for sensitive data
- Implement user authentication for admin functions

## Future Enhancements

- [ ] Multi-camera support
- [ ] Web-based interface
- [ ] Attendance reports and analytics
- [ ] Mobile app integration
- [ ] Advanced face anti-spoofing
- [ ] Time zone support
- [ ] Bulk user import/export

## License

This project is open-source. Feel free to modify and distribute.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify all prerequisites are met
3. Ensure proper database setup
4. Check camera permissions and availability

---

**Built with ❤️ using Python, DeepFace, and modern computer vision techniques**