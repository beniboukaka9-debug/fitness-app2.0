# 💪 Fitness App 2.0 - Complete Fitness Tracking & Workout Generator

A cross-platform fitness application with real-time step tracking, GPS-based running mode, and AI-powered personalized workouts.

## 🎯 Features

### 1. Real-Time Step Counter & Running Mode
- Built-in pedometer using phone accelerometer
- Live step count display with distance estimation
- GPS-enabled "Run" mode with real-time pace tracking
- Automatic activity logging and history

### 2. Personalized Workout Recommendations
- Initial questionnaire (fitness level, target areas, equipment, duration)
- AI-powered workout generator based on recent activity
- Flexible exercise selection with animated GIFs
- Built-in timer and rest period management

### 3. Adaptive Lifestyle Management
- Dynamic daily step goals based on user average
- Drag-and-drop weekly planner
- Contextual notifications and encouragement
- Consistency-focused reward system

### 4. Semi-Liquid Glass UI Design
- Glassmorphism theme with blurred backgrounds
- Liquid-like animations and elastic transitions
- Gooey button effects and wave animations
- Clean typography with optimal contrast

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Local database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Scikit-learn** - ML for workout recommendations

### Frontend (Mobile)
- **Flutter** - Cross-platform mobile development
- **Provider** - State management
- **Geolocator** - GPS tracking
- **Pedometer** - Step counting
- **SQLite** - Local storage

## 📁 Project Structure

```
fitness-app2.0/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── database/
│   │   └── config.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── mobile/
│   ├── lib/
│   ├── android/
│   ├── ios/
│   └── pubspec.yaml
└── .github/workflows/
    └── build_apk.yml
```

## 🚀 Getting Started

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup PostgreSQL locally
# Create database
createdb fitness_app

# Run FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Mobile Setup

```bash
cd mobile
flutter pub get
flutter run
```

## 📱 APK Download

The APK is automatically built and available for download:
- Navigate to **Actions** tab on GitHub
- Select the latest workflow run
- Download the APK from **Artifacts**

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- Environment variables for sensitive data
- CORS configuration for API security

## 📊 API Endpoints

### Users
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update profile

### Activities
- `POST /api/v1/activities/` - Log activity
- `GET /api/v1/activities/today` - Get today's activities
- `GET /api/v1/activities/week` - Get weekly summary

### Workouts
- `GET /api/v1/workouts/recommend` - Get personalized recommendation
- `POST /api/v1/workouts/` - Start workout session
- `PUT /api/v1/workouts/{id}` - Update workout

## 🎨 Design System

- **Colors**: Semi-transparent glass effect with soft shadows
- **Typography**: Clean, modern fonts with excellent readability
- **Animations**: Smooth transitions, elastic effects, wave ripples
- **Spacing**: Consistent padding and margins

## 📝 License

MIT License - Feel free to use and modify!

---

**Made with ❤️ for fitness enthusiasts**
