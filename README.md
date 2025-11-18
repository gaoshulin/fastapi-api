# FastAPI MVC Project

A complete FastAPI project with MVC architecture, including database models, controllers, services, middleware, and proper error handling.

## Project Structure

```
.
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── app/
│   ├── __init__.py
│   ├── config/            # Configuration files
│   │   ├── __init__.py
│   │   ├── settings.py    # Application settings
│   │   └── database.py    # Database configuration
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   └── user.py        # User and Item models
│   ├── schemas/           # Pydantic models for validation
│   │   ├── __init__.py
│   │   ├── user.py        # User and Item schemas
│   │   └── common.py      # Common response schemas
│   ├── controllers/       # API endpoints
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   └── item_controller.py
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── middleware/        # Custom middleware
│   │   ├── __init__.py
│   │   ├── logging.py           # Request logging
│   │   ├── auth_middleware.py   # Authentication middleware
│   │   └── error_handler.py     # Error handling
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   └── exceptions.py  # Custom exceptions
│   └── routers/           # Route configuration
│       └── __init__.py
├── tests/                 # Test files
└── migrations/            # Database migrations
```

## Features

- **MVC Architecture**: Clean separation of concerns
- **Database Models**: SQLAlchemy models with relationships
- **Request/Response Validation**: Pydantic schemas
- **Error Handling**: Custom exceptions and middleware
- **Logging**: Request/response logging middleware
- **CORS**: Cross-origin resource sharing support
- **Pagination**: Built-in pagination support
- **Environment Configuration**: Environment-based settings

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

5. Update the `.env` file with your configuration

## Running the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - Login user (returns JWT token)

### Users
- `GET /api/v1/users/` - Get all users (paginated)
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/users/` - Create new user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Items
- `GET /api/v1/items/` - Get all items (paginated)
- `GET /api/v1/items/{id}` - Get item by ID
- `GET /api/v1/items/owner/{owner_id}` - Get items by owner
- `POST /api/v1/items/` - Create new item
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

## Configuration

The application uses environment variables for configuration. Key settings:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for security
- `DEBUG`: Debug mode (True/False)
- `HOST`: Server host
- `PORT`: Server port
- `LOG_LEVEL`: Logging level

## Error Handling

The application includes comprehensive error handling:
- Custom exceptions for different error types
- Centralized error middleware
- Consistent error response format
- Proper HTTP status codes

## Security

- Password hashing with bcrypt
- CORS configuration
- Environment-based configuration
- Input validation with Pydantic