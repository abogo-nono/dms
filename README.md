# Diet Management System (DMS) 🍽️🥗

The Diet Management System is a comprehensive Flask-based REST API that helps users track their dietary habits, manage food information, and monitor nutritional intake. The system provides features for logging food consumption, tracking allergies, generating meal suggestions, and analyzing nutritional data.

## ✨ Features

- **👤 User Management**: Create, update, and manage user profiles
- **🍔 Food Database**: Maintain a catalog of foods with descriptions and images
- **🥕 Ingredient Tracking**: Track ingredients used in each food
- **📊 Nutrition Information**: Store and retrieve nutritional data for foods
- **📝 Food Logging**: Allow users to log what they eat and view consumption history
- **⚠️ Allergy Management**: Track food allergies and provide warnings when attempting to consume allergenic foods
- **🎲 Menu Suggestions**: Generate random meal suggestions based on user's allergy information

## 🛠️ Technology Stack

- **🐍 Backend**: Python 3.11+ with Flask
- **🗄️ Database**: PostgreSQL (development/production) or SQLite (testing)
- **📚 API Documentation**: Swagger/OpenAPI via Flasgger
- **🐳 Containerization**: Docker and Docker Compose
- **🔄 ORM**: SQLAlchemy with Flask-SQLAlchemy
- **🔀 Database Migrations**: Alembic with Flask-Migrate

## 🚀 Installation

### 💻 Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/abogo-nono/dms
   cd dms
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (or create a .env file):
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SQLALCHEMY_DATABASE_URI=sqlite:///dms_db.db  # For local development
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

### 🐳 Docker Development Setup

1. Clone the repository and navigate to the project directory

2. Create a .env file based on .env.example or use the existing one

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. The API will be available at http://localhost:8000
   
5. Access the Swagger documentation at http://localhost:8000/api/docs/

### 🚢 Production Deployment

For production deployment, use the production Docker Compose file:

```bash
FLASK_ENV=production docker-compose -f docker-compose.prod.yml up -d
```

Make sure to set secure database credentials in your production environment.

## 📁 Project Structure

```
.
├── app/                        # Main application package
│   ├── __init__.py             # Application factory
│   ├── docs/                   # Swagger/OpenAPI documentation
│   ├── models/                 # Database models
│   ├── resources/              # API resources/endpoints
│   ├── entrypoint.sh           # Docker entrypoint script
│   └── routes.py               # API route registration
├── migrations/                 # Database migration files
├── static/                     # Static files (e.g., uploaded images)
├── .dockerignore               # Files to exclude from Docker build
├── .env                        # Environment variables (don't commit to version control)
├── .env.example                # Example environment variables
├── docker-compose.prod.yml     # Production Docker Compose configuration
├── docker-compose.yml          # Development Docker Compose configuration
├── Dockerfile                  # Docker build instructions
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── run.py                      # Application entry point
```

## 🔌 API Endpoints

The DMS API provides the following main endpoints:

### 👤 Person Endpoints

- `GET /people` - List all people
- `POST /people` - Create a new person
- `GET /people/{person_id}` - Get a specific person
- `PUT /people/{person_id}` - Update a person
- `DELETE /people/{person_id}` - Delete a person
- `GET /people/{person_id}/food_history` - Get a person's food consumption history
- `GET /people/{person_id}/allergies` - Get a person's allergies
- `GET /people/{person_id}/menu_suggestions` - Get menu suggestions for a person

### 🍔 Food Endpoints

- `GET /foods` - List all foods
- `POST /foods` - Create a new food
- `GET /foods/{food_id}` - Get a specific food
- `PUT /foods/{food_id}` - Update a food
- `DELETE /foods/{food_id}` - Delete a food
- `GET /foods/{food_id}/calories` - Get calories for a food
- `GET /foods/{food_id}/ingredients` - List ingredients for a food

### 🥕 Ingredient Endpoints

- `GET /ingredients` - List all ingredients
- `POST /ingredients` - Create a new ingredient
- `GET /ingredients/{ingredient_id}` - Get a specific ingredient
- `PUT /ingredients/{ingredient_id}` - Update an ingredient
- `DELETE /ingredients/{ingredient_id}` - Delete an ingredient

### 🔗 Food Ingredient Endpoints

- `GET /food_ingredients` - List all food-ingredient relationships
- `POST /food_ingredients` - Create a new food-ingredient relationship
- `GET /food_ingredients/{food_ingredient_id}` - Get a specific food-ingredient relationship
- `PUT /food_ingredients/{food_ingredient_id}` - Update a food-ingredient relationship
- `DELETE /food_ingredients/{food_ingredient_id}` - Delete a food-ingredient relationship

### 📊 Nutrition Info Endpoints

- `GET /nutrition_info` - List all nutrition information
- `POST /nutrition_info` - Create new nutrition information
- `GET /nutrition_info/{nutrition_info_id}` - Get specific nutrition information
- `PUT /nutrition_info/{nutrition_info_id}` - Update nutrition information
- `DELETE /nutrition_info/{nutrition_info_id}` - Delete nutrition information

### 📝 Food Log Endpoints

- `POST /food_log` - Log food consumption
- `GET /people/{person_id}/food_history` - Get a person's food consumption history

### ⚠️ Allergy Endpoints

- `GET /allergies` - List all allergies
- `POST /allergies` - Record a new allergy
- `GET /allergies/{allergy_id}` - Get a specific allergy
- `PUT /allergies/{allergy_id}` - Update an allergy
- `DELETE /allergies/{allergy_id}` - Delete an allergy

## 🗃️ Database Schema

The application uses the following database models:

- **👤 Person**: Stores user information
- **🍔 Food**: Stores food items with descriptions and images
- **🥕 Ingredient**: Stores basic ingredients
- **🔗 FoodIngredient**: Maps ingredients to foods with quantities
- **📊 NutritionInfo**: Stores nutritional information for foods
- **📝 FoodLog**: Records when a person consumes a food
- **⚠️ Allergy**: Records food allergies for people

## 🧪 Using the API

### Example: Creating a Person

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"John Doe","gender":"Male","age":30}' http://localhost:8000/people
```

### Example: Logging Food Consumption

```bash
curl -X POST -H "Content-Type: application/json" -d '{"person_id":1,"food_id":1,"notes":"Lunch"}' http://localhost:8000/food_log
```

### Example: Getting Menu Suggestions

```bash
curl http://localhost:8000/people/1/menu_suggestions
```

## 📚 API Documentation

The API is documented using Swagger/OpenAPI. You can access the Swagger UI at:

```
http://localhost:8000/api/docs/
```

## 👨‍💻 Development

### Adding New Features

1. Create or modify model(s) in the models directory 📋
2. Create or update database migrations:
   ```bash
   flask db migrate -m "Description of changes"
   ```
3. Create or update resource(s) in the resources directory 🔧
4. Register new routes in routes.py 🔌
5. Update Swagger documentation in docs 📝

### Running Tests

Testing functionality is not yet implemented. Future versions will include a test suite. 🧪

## 🤝 Contributing

1. Fork the repository 🍴
2. Create a feature branch (`git checkout -b feature/amazing-feature`) 🌿
3. Commit your changes (`git commit -m 'Add some amazing feature'`) ✅
4. Push to the branch (`git push origin feature/amazing-feature`) 🚀
5. Open a Pull Request 📩

## 📄 License

This project is licensed under the MIT License. ⚖️

---

Built with ❤️ for better nutrition management and dietary health tracking.