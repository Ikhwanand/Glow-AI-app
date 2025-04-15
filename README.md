# Skin Doctor App

A comprehensive web application for skin health analysis and tracking, combining AI-powered diagnostics with personal skincare management.

## ✨ Key Features

- **AI-Powered Skin Analysis**
  - Upload facial images for instant skin condition assessment
  - Get personalized recommendations based on analysis
  - Track skin health progress over time

- **Personal Skin Journal**
  - Log daily skin conditions and routines
  - Track lifestyle factors affecting skin health
  - Visualize progress with charts and metrics

- **Product Management**
  - Catalog your skincare products
  - Receive AI-generated product recommendations
  - Track product effectiveness

- **Profile Management**
  - Secure user profiles with personal skin profiles
  - Customizable skin type and concern tracking
  - Profile image and personal details management

## 🛠️ Tech Stack

### Frontend
- React 18 with Vite
- Tailwind CSS for styling
- React Hook Forms for form management
- Axios for API communication
- Framer Motion for animations

### Backend
- FastAPI (Python 3.12+)
- SQLAlchemy ORM
- JWT Authentication
- Python-JOSE for security
- Uvicorn ASGI server

### AI Components
- Gemini for AI model
- Agno for AI Agent framework

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js v18+
- npm or yarn
- PostgreSQL (or your preferred database)

### Installation

#### Backend Setup
1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run development server:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Set VITE_API_URL to your backend URL
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

## 🔧 Project Structure

```
skin-doctor-app/
├── backend/
│   ├── app/               # Backend application
│   │   ├── api/           # API endpoints
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── main.py        # FastAPI app entry
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment template
│
├── frontend/
│   ├── src/               # Frontend source
│   │   ├── components/    # React components
│   │   ├── pages/         # Application pages
│   │   ├── services/      # API services
│   │   └── App.jsx       # Main app component
│   ├── vite.config.js    # Vite configuration
│   └── .env.example      # Frontend environment
│
├── README.md             # Project documentation
└── pyproject.toml        # Python project config
```

## 🌐 API Documentation
The backend API is documented using Swagger UI. After starting the backend server, access the docs at:
```
http://localhost:8000/docs
```

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact
For questions or support, please contact: [aldirizaldy977@gmail.com](mailto:aldirizaldy977@gmail.com)

