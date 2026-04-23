# Complete LLM Essay Evaluation API Documentation

## 🌐 Base URL
```
http://localhost:8000/backend/api/v1
```

## 🔐 Authentication APIs

### 1. User Registration
**POST** `/users/`

Register a new user account with email verification.

**Request Body:**
```json
{
  "first_name": "Test",
  "last_name": "User", 
  "type": "e",
  "email": "test@yopmail.com",
  "password": "testpass123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "user registration successfully",
  "data": {
    "first_name": "Test",
    "last_name": "User",
    "email": "test@yopmail.com",
    "type": "e"
  }
}
```

### 2. User Login
**POST** `/auth/login`

Login user with email and password to get JWT token.

**Request Body:**
```json
{
  "email": "test@yopmail.com",
  "password": "testpass123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "first_name": "Test",
      "last_name": "User",
      "email": "test@yopmail.com",
      "type": "e"
    }
  }
}
```

### 3. Forgot Password
**POST** `/auth/forgot-password`

Send password reset link to user's email.

**Request Body:**
```json
{
  "email": "test@yopmail.com"
}
```

### 4. Reset Password
**POST** `/auth/reset-password`

Reset user password using reset token.

**Request Body:**
```json
{
  "token": "reset_token_here",
  "new_password": "newpassword123"
}
```

### 5. Email Verification
**POST** `/auth/verify-email`

Verify user email using verification token.

**Request Body:**
```json
{
  "token": "verification_token_here"
}
```

### 6. Change Password
**POST** `/auth/change-password`

Change user password (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

## 📝 Essay Management APIs

### 7. Submit Essay for Evaluation
**POST** `/essays/submit`

Submit essay for AI-powered evaluation using Groq LLM.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "essay_text": "Indian politics is one of the most complex and vibrant political systems in the world. As the largest democracy, India operates under a constitutional framework that ensures representation, rights, and governance for over a billion people...",
  "title": "Indian Democracy: Challenges and Resilience"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Essay submitted and evaluated successfully",
  "data": {
    "id": "essay_id_here",
    "user_id": "user_id_here",
    "title": "Indian Democracy: Challenges and Resilience",
    "essay_text": "Indian politics is one of the most complex...",
    "clarity_of_thoughts_score": 8,
    "clarity_of_thoughts_feedback": "The essay demonstrates excellent clarity with well-organized ideas and logical flow...",
    "language_quality_score": 7,
    "language_quality_feedback": "Language is generally good with proper grammar and vocabulary...",
    "depth_analysis_score": 8,
    "depth_analysis_feedback": "The analysis shows good depth with multiple perspectives considered...",
    "overall_score": 23,
    "overall_feedback": "Overall, this is a well-structured essay with strong arguments and good coverage of the topic...",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

### 8. Get Essay History
**GET** `/essays/history`

Get user's essay submission history with pagination.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `limit` (optional): Number of essays to return (default: 50, max: 100)
- `offset` (optional): Number of essays to skip (default: 0)

**Example:**
```
GET /essays/history?limit=10&offset=0
```

**Response:**
```json
{
  "success": true,
  "data": {
    "essays": [
      {
        "id": "essay_id_1",
        "user_id": "user_id_here",
        "title": "Essay Title 1",
        "essay_text": "Essay content here...",
        "clarity_of_thoughts_score": 8,
        "clarity_of_thoughts_feedback": "Feedback text...",
        "language_quality_score": 7,
        "language_quality_feedback": "Feedback text...",
        "depth_analysis_score": 8,
        "depth_analysis_feedback": "Feedback text...",
        "overall_score": 23,
        "overall_feedback": "Overall feedback...",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      }
    ],
    "total_essays": 25
  }
}
```

### 9. Get User Dashboard
**GET** `/essays/dashboard`

Get user dashboard with comprehensive statistics and recent essays.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "stats": {
      "total_essays": 25,
      "average_score": 21.5,
      "highest_score": 28,
      "lowest_score": 15,
      "total_clarity_score": 200,
      "total_language_score": 175,
      "total_depth_score": 190,
      "recent_essays": [
        {
          "id": "recent_essay_id",
          "title": "Recent Essay Title",
          "overall_score": 24,
          "created_at": "2024-01-15T10:30:00Z"
        }
      ]
    },
    "performance_breakdown": {
      "exceptional": {
        "count": 5,
        "percentage": 20.0
      },
      "excellent": {
        "count": 8,
        "percentage": 32.0
      },
      "good": {
        "count": 10,
        "percentage": 40.0
      },
      "needs_improvement": {
        "count": 2,
        "percentage": 8.0
      },
      "poor": {
        "count": 0,
        "percentage": 0.0
      }
    }
  }
}
```

## 📊 Score Categories

### Performance Levels:
- **Exceptional**: 27-30 points
- **Excellent**: 21-26 points  
- **Good**: 15-20 points
- **Needs Improvement**: 9-14 points
- **Poor**: 3-8 points

### Evaluation Criteria:
1. **Clarity of Thoughts** (1-10 points): Organization, logical flow, coherence
2. **Language Quality** (1-10 points): Grammar, spelling, vocabulary, sentence structure
3. **Depth of Analysis** (1-10 points): Critical thinking, multiple perspectives, comprehensive coverage

## 🔧 Setup Instructions

### 1. Environment Variables
Update `.env` file:
```env
DB_URL = 'postgresql://postgres:password@localhost:5432/essay_eval_project'
JWT_SECRET = "your_jwt_secret"
JWT_ALGORITHM = "HS256"
BREVO_API_KEY = "your_brevo_api_key"
BREVO_SENDER_EMAIL = "your_sender_email"
BREVO_SENDER_NAME = "Your App Name"
GROQ_SECRET_KEY = "your_groq_api_key"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Migration
```bash
alembic upgrade head
```

### 4. Start Server
```bash
uvicorn main:app --reload
```

## 🧪 Testing with Postman

1. Import `Postman_Collection_Essay_APIs.json`
2. Set variables:
   - `base_url`: `http://localhost:8000`
   - `jwt_token`: Get from login response
3. Test APIs in sequence:
   - Register/Login → Submit Essay → View Dashboard

## 🎯 Features Implemented

✅ **User Authentication** with JWT tokens
✅ **Email Verification** with Brevo integration
✅ **Password Reset** functionality
✅ **AI Essay Evaluation** using Groq LLM
✅ **Multi-criteria Evaluation** (Clarity, Language, Depth)
✅ **Essay History** with pagination
✅ **User Dashboard** with statistics
✅ **Performance Analytics** and breakdown
✅ **Database Storage** of all evaluations
✅ **Error Handling** and validation
✅ **Postman Collection** for easy testing

## 🚀 Ready to Use

Your complete LLM essay evaluation system is now fully operational with:
- **8 API Endpoints** covering authentication and essay management
- **AI-Powered Evaluation** with detailed feedback
- **Comprehensive Dashboard** with analytics
- **Email Integration** for user verification
- **Database Persistence** for all data
- **Postman Collection** for immediate testing

**Server Status**: 🟢 Running on http://localhost:8000
