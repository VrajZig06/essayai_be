# LLM Essay Evaluation API

A comprehensive FastAPI-based system for AI-powered essay evaluation with user authentication, email verification, and detailed analytics dashboard.

## 🚀 Features

- **🔐 User Authentication** with JWT tokens
- **📧 Email Verification** using Brevo API
- **🤖 AI Essay Evaluation** powered by Groq LLM
- **📊 User Dashboard** with comprehensive statistics
- **📝 Essay History** with pagination
- **🔒 Password Reset** functionality
- **📈 Performance Analytics** and breakdown
- **📋 Complete API Documentation**

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Email Service**: Brevo (Sendinblue)
- **AI/ML**: Groq LLM with LangChain
- **Database Migrations**: Alembic
- **API Documentation**: Swagger/OpenAPI

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Brevo API key for email services
- Groq API key for AI evaluation

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd LLM API
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file with the following variables:

```env
# Database
DB_URL = 'postgresql://postgres:password@localhost:5432/essay_eval_project'

# JWT Configuration
JWT_SECRET = "your_secure_jwt_secret_key"
JWT_ALGORITHM = "HS256"

# Brevo Email Service
BREVO_API_KEY = "your_brevo_api_key"
BREVO_SENDER_EMAIL = "your_sender_email@example.com"
BREVO_SENDER_NAME = "Your App Name"

# Groq API (Optional - can use mock LLM)
GROQ_SECRET_KEY = "your_groq_api_key"
```

### 5. Database Setup

```bash
# Create database migrations
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Start the Server

```bash
uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/backend/api/v1
```

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Authentication APIs

### User Registration
```http
POST /users/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "type": "e",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### User Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### Email Verification
```http
POST /auth/verify-email
Content-Type: application/json

{
  "token": "verification_token_from_email"
}
```

### Forgot Password
```http
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "john.doe@example.com"
}
```

### Reset Password
```http
POST /auth/reset-password
Content-Type: application/json

{
  "token": "reset_token_from_email",
  "new_password": "newsecurepassword123"
}
```

### Change Password
```http
POST /auth/change-password
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

## 📝 Essay Management APIs

### Submit Essay for Evaluation
```http
POST /essays/submit
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "essay_text": "Your essay content here...",
  "title": "Essay Title (optional)"
}
```

### Get Essay History
```http
GET /essays/history?limit=10&offset=0
Authorization: Bearer <jwt_token>
```

### Get User Dashboard
```http
GET /essays/dashboard
Authorization: Bearer <jwt_token>
```

## 🤖 AI Evaluation System

### Evaluation Criteria
The AI evaluates essays based on three criteria:

1. **Clarity of Thoughts** (1-10 points)
   - Organization and structure
   - Logical flow and coherence
   - Clear articulation of ideas

2. **Language Quality** (1-10 points)
   - Grammar and spelling
   - Vocabulary usage
   - Sentence structure and style

3. **Depth of Analysis** (1-10 points)
   - Critical thinking
   - Multiple perspectives
   - Comprehensive coverage

### Performance Levels
- **Exceptional**: 27-30 points
- **Excellent**: 21-26 points
- **Good**: 15-20 points
- **Needs Improvement**: 9-14 points
- **Poor**: 3-8 points

## 📊 Dashboard Features

### User Statistics
- Total essays submitted
- Average score across all essays
- Highest and lowest scores
- Performance breakdown by category

### Recent Essays
- Last 5 essay submissions
- Quick score overview
- Direct access to detailed feedback

### Performance Analytics
- Score distribution chart
- Category-wise performance
- Progress tracking over time

## 🧪 Testing with Postman

A complete Postman collection is provided:

1. Import `Postman_Collection_Essay_APIs.json` into Postman
2. Set environment variables:
   - `base_url`: `http://localhost:8000`
   - `jwt_token`: Get from login response
3. Test all endpoints in sequence

## 📁 Project Structure

```
LLM API/
├── app/
│   ├── config/
│   │   └── settings.py
│   ├── db/
│   │   ├── models/
│   │   │   ├── user_model.py
│   │   │   └── essay_model.py
│   │   ├── base.py
│   │   └── session.py
│   ├── middleware/
│   ├── repositories/
│   │   ├── base_repo.py
│   │   ├── user_repo.py
│   │   └── essay_repo.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   ├── auth_routes.py
│   │   └── essay_routes.py
│   ├── schema/
│   │   ├── user_schema.py
│   │   └── essay_schema.py
│   ├── services/
│   │   ├── user_service.py
│   │   ├── essay_service.py
│   │   └── email_service.py
│   └── utils/
│       ├── jwt.py
│       ├── messages.py
│       └── response.py
├── alembic/
├── venv/
├── essay_reports/
├── main.py
├── llm.py
├── requirements.txt
├── .env
├── alembic.ini
├── README.md
├── Complete_API_List.md
└── Postman_Collection_Essay_APIs.json
```

## 🔧 Development

### Adding New Features

1. **Database Models**: Add to `app/db/models/`
2. **API Endpoints**: Add to `app/routes/`
3. **Business Logic**: Add to `app/services/`
4. **Database Operations**: Add to `app/repositories/`
5. **Schemas**: Add to `app/schema/`

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

2. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure database exists

3. **Email Service Not Working**
   - Verify Brevo API key
   - Check sender email configuration
   - Ensure API quota is available

4. **AI Evaluation Not Working**
   - Check Groq API key (if using real LLM)
   - System falls back to mock LLM if API fails

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support and questions:

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 Documentation: [Project Wiki](https://github.com/your-repo/wiki)

## 🎯 Roadmap

- [ ] Multi-language support for essays
- [ ] Advanced AI models integration
- [ ] Real-time collaboration features
- [ ] Mobile app development
- [ ] Analytics and reporting dashboard
- [ ] Integration with learning management systems

---

**Built with ❤️ using FastAPI and modern Python technologies**
