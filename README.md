# Donation Platform Backend

This is a FastAPI-based donation platform backend with SQLite database.

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Dependencies are already installed in the virtual environment*

2. **Run the server (Option 1 - Use batch file):**
   ```bash
   run_server.bat
   ```
   *This automatically uses the correct Python environment*

3. **Run the server (Option 2 - Activate environment manually):**
   ```bash
   # Activate virtual environment
   .venv\Scripts\activate.bat
   
   # Then run server
   python main.py
   ```

4. **Run the server (Option 3 - Use full path):**
   ```bash
   C:\ganti.b\Hackathon\GWH\.venv\Scripts\python.exe main.py
   ```

5. **Access the API:**
   - Server will be available at: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Health Check
- **GET /ping** - Health check endpoint

### Users
- **POST /users/** - Create a new user
- **GET /users/{user_id}** - Get user by ID
- **GET /users/** - Get all users

### Donations
- **POST /donate** - Submit a donation (main endpoint)
- **GET /donations/** - Get all donations
- **GET /donations/user/{user_id}** - Get donations by user

### Needs
- **POST /needs/** - Create a new need
- **GET /needs/** - Get all current needs

## Testing Instructions

### 1. Using curl

**Health Check:**
```bash
curl -X GET "http://localhost:8000/ping"
```

**Create a User:**
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}'
```

**Make a Donation:**
```bash
curl -X POST "http://localhost:8000/donate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "item_type": "food",
    "location": "New York, NY"
  }'
```

**Get User Details:**
```bash
curl -X GET "http://localhost:8000/users/1"
```

**Get All Needs:**
```bash
curl -X GET "http://localhost:8000/needs/"
```

### 2. Using Postman

1. **Import the following requests:**

   **Health Check:**
   - Method: GET
   - URL: http://localhost:8000/ping

   **Create User:**
   - Method: POST
   - URL: http://localhost:8000/users/
   - Headers: Content-Type: application/json
   - Body: {"name": "Alice Smith"}

   **Make Donation:**
   - Method: POST
   - URL: http://localhost:8000/donate
   - Headers: Content-Type: application/json
   - Body: {
       "user_id": 1,
       "item_type": "medical_supplies",
       "location": "Los Angeles, CA"
     }

### 3. Testing Scenarios

**Scenario 1: New User First Donation**
1. Create user: `{"name": "Test User"}`
2. Make donation: `{"user_id": 1, "item_type": "clothing", "location": "Chicago"}`
3. Expected: 120 points (100 base × 1.2 urgency × 1.0 frequency)

**Scenario 2: High Urgency Item**
1. Make donation: `{"user_id": 1, "item_type": "food", "location": "Miami"}`
2. Expected: 150 points (100 base × 1.5 urgency × 1.0 frequency)

**Scenario 3: Critical Item**
1. Make donation: `{"user_id": 1, "item_type": "medical_supplies", "location": "Seattle"}`
2. Expected: 200 points (100 base × 2.0 urgency × 1.0 frequency)

**Scenario 4: Frequency Bonus**
1. Make 5+ donations with same user
2. Next donation should have 1.1× frequency bonus

### 4. Database Verification

The SQLite database file `donation_platform.db` will be created automatically. You can verify updates using:

**View Users Table:**
```bash
sqlite3 donation_platform.db "SELECT * FROM users;"
```

**View Donations Table:**
```bash
sqlite3 donation_platform.db "SELECT * FROM donations;"
```

**View Needs Table:**
```bash
sqlite3 donation_platform.db "SELECT * FROM needs;"
```

## Database Schema

### Users Table
- `id`: Primary key
- `name`: User's name
- `points`: Total points earned
- `rank`: Current rank (Bronze, Silver, Gold, Platinum, Diamond)
- `donations_count`: Number of donations made

### Donations Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `item_type`: Type of item donated
- `location`: Donation location
- `timestamp`: When donation was made
- `points_awarded`: Points awarded for this donation

### Needs Table
- `id`: Primary key
- `item_type`: Type of item needed
- `urgency_level`: Urgency level (low, medium, high, critical)
- `multiplier`: Point multiplier for this item type

## Point Calculation Logic

1. **Base Points:** 100 points per donation
2. **Urgency Multiplier:** Based on current needs
   - Low: 1.0×
   - Medium: 1.1× - 1.2×
   - High: 1.5×
   - Critical: 2.0×
3. **Frequency Bonus:** Based on donation count
   - 1-4 donations: 1.0×
   - 5-9 donations: 1.1×
   - 10-19 donations: 1.2×
   - 20-49 donations: 1.5×
   - 50+ donations: 2.0×

## Rank System

- **Bronze:** 0-499 points
- **Silver:** 500-1999 points
- **Gold:** 2000-4999 points
- **Platinum:** 5000-9999 points
- **Diamond:** 10000+ points
