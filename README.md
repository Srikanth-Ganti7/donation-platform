# Donation Platform Backend

A comprehensive FastAPI-based donation platform backend with SQLite database, intelligent point calculation system, and gamified user rankings. Built for hackathon with complete API documentation and testing utilities.

## 🏗️ Architecture Overview

### **Core Components**
- **FastAPI Backend** - High-performance async web framework
- **SQLite Database** - Lightweight relational database with SQLAlchemy ORM
- **Pydantic Schemas** - Data validation and serialization
- **Automatic API Documentation** - Interactive Swagger UI and ReDoc

### **Key Features**
- ✅ **Smart Point System** - Dynamic scoring based on item urgency and donation frequency
- ✅ **User Rankings** - Gamified progression system (Bronze → Silver → Gold → Platinum → Diamond)
- ✅ **Real-time Tracking** - Complete donation history with timestamps and locations
- ✅ **Pre-populated Needs** - System starts with 6 predefined urgent item categories
- ✅ **Frequency Bonuses** - Rewards for consistent donors
- ✅ **RESTful API** - Clean, documented endpoints for all operations

## Setup Instructions

### **🪟 Windows Users**

1. **First-time setup (run once):**
   ```bash
   setup.bat
   ```
   *This will create the virtual environment and install all dependencies*

2. **Run the server:**
   ```bash
   run_server.bat              # Recommended - one-click start
   ```

3. **Alternative methods:**
   ```bash
   activate_env.bat             # Activate environment manually, then: python main.py
   .\.venv\Scripts\python.exe main.py    # Direct execution
   ```

### **🐧🍎 Linux/macOS Users**

1. **First-time setup (run once):**
   ```bash
   chmod +x setup.sh run_server.sh   # Make scripts executable
   ./setup.sh
   ```

2. **Run the server:**
   ```bash
   ./run_server.sh              # One-click start
   ```

3. **Alternative methods:**
   ```bash
   source .venv/bin/activate    # Activate environment manually
   python main.py               # Then run server
   ```

### **🌍 Universal Method (Any OS)**

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# OR Activate (Linux/macOS)  
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

### **🌐 Access the API:**
- **Server**: Automatically finds available port (usually http://localhost:8000)
- **Interactive API docs**: http://localhost:PORT/docs ← **Start here!**
- **Alternative docs**: http://localhost:PORT/redoc  
- **Health check**: http://localhost:PORT/ping

*The server will display the actual URLs when it starts*

## 🔌 API Endpoints

### Health Check
- **GET /ping** - System health check endpoint
  - Returns: `{"message": "pong"}`

### User Management
- **POST /users/** - Create a new user
  - Body: `{"name": "string"}`
  - Returns: Complete user object with initial stats
- **GET /users/{user_id}** - Get specific user by ID
- **GET /users/** - Get all users (supports pagination: `?skip=0&limit=100`)

### Donation System
- **POST /donate** - Submit a donation (⭐ **Main endpoint**)
  - Body: `{"user_id": int, "item_type": "string", "location": "string"}`
  - Returns: `{"user_id": int, "points_awarded": int, "total_points": int}`
- **GET /donations/** - Get all donations (supports pagination)
- **GET /donations/user/{user_id}** - Get donations by specific user

### Needs Management
- **POST /needs/** - Create a new urgent need
  - Body: `{"item_type": "string", "urgency_level": "string", "multiplier": float}`
- **GET /needs/** - View all current needs with multipliers

### 🎯 Pre-populated Needs (Available on Startup)
The system automatically creates these urgent needs:

| Item Type | Urgency Level | Point Multiplier | Use Case |
|-----------|---------------|------------------|----------|
| **food** | high | 1.5× | Emergency food relief |
| **medical_supplies** | critical | 2.0× | Life-saving medical equipment |
| **clothing** | medium | 1.2× | Winter clothing, work attire |
| **books** | medium | 1.1× | Educational materials |
| **toys** | low | 1.0× | Children's comfort items |
| **electronics** | low | 1.0× | Communication devices |

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

**Scenario 1: New User First Donation (Clothing)**
1. Create user: `{"name": "Test User"}`
2. Make donation: `{"user_id": 1, "item_type": "clothing", "location": "Chicago"}`
3. **Expected Result**: 120 points (100 base × 1.2 urgency × 1.0 frequency)

**Scenario 2: High Urgency Item (Food)**
1. Make donation: `{"user_id": 1, "item_type": "food", "location": "Miami"}`
2. **Expected Result**: 150 points (100 base × 1.5 urgency × 1.0 frequency)

**Scenario 3: Critical Urgency Item (Medical Supplies)**
1. Make donation: `{"user_id": 1, "item_type": "medical_supplies", "location": "Seattle"}`
2. **Expected Result**: 200 points (100 base × 2.0 urgency × 1.0 frequency)

**Scenario 4: Unknown Item Type**
1. Make donation: `{"user_id": 1, "item_type": "furniture", "location": "Boston"}`
2. **Expected Result**: 100 points (100 base × 1.0 default × 1.0 frequency)

**Scenario 5: Frequency Bonus Trigger**
1. Make 5+ donations with same user
2. Next donation should have **1.1× frequency bonus**
3. Example: `{"user_id": 1, "item_type": "books", "location": "Austin"}`
4. **Expected Result**: 121 points (100 × 1.1 urgency × 1.1 frequency)

**Scenario 6: Rank Progression**
- Watch user rank change as points accumulate:
  - 0-499 points: **Bronze** 🥉
  - 500-1999 points: **Silver** 🥈  
  - 2000-4999 points: **Gold** 🥇
  - 5000-9999 points: **Platinum** 💎
  - 10000+ points: **Diamond** 💎✨

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

## 💾 Database Schema

### Users Table (`users`)
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `id` | Integer | Primary key, auto-increment | - |
| `name` | String | User's display name | - |
| `points` | Integer | Total lifetime points earned | 0 |
| `rank` | String | Current rank badge | "Bronze" |
| `donations_count` | Integer | Total number of donations made | 0 |

### Donations Table (`donations`)
| Column | Type | Description | Default |
|--------|------|-------------|---------|
| `id` | Integer | Primary key, auto-increment | - |
| `user_id` | Integer | Foreign key to users.id | - |
| `item_type` | String | Type of item donated | - |
| `location` | String | Where donation was made | - |
| `timestamp` | DateTime | When donation was recorded | `datetime.utcnow()` |
| `points_awarded` | Integer | Points given for this donation | - |

### Needs Table (`needs`)
| Column | Type | Description | Constraint |
|--------|------|-------------|------------|
| `id` | Integer | Primary key, auto-increment | - |
| `item_type` | String | Type of item needed | Unique |
| `urgency_level` | String | Priority level (low/medium/high/critical) | - |
| `multiplier` | Float | Point multiplier for this item type | - |

### 🔗 Database Relationships
- **Users** ↔ **Donations**: One-to-Many (User can have multiple donations)
- **Needs**: Standalone reference table for calculating point multipliers

## 🧮 Point Calculation System

### **Formula**: `Final Points = Base Points × Urgency Multiplier × Frequency Bonus`

### **1. Base Points**
- **Fixed**: 100 points per donation
- Applied to every donation regardless of type

### **2. Urgency Multiplier** (Based on Current Needs)
| Urgency Level | Multiplier | Examples |
|---------------|------------|----------|
| **Critical** | 2.0× | medical_supplies |
| **High** | 1.5× | food |
| **Medium** | 1.1× - 1.2× | clothing (1.2×), books (1.1×) |
| **Low** | 1.0× | toys, electronics |
| **Unknown Item** | 1.0× | Any item not in needs table |

### **3. Frequency Bonus** (Based on User's Donation History)
| Donation Count | Bonus Multiplier | Status |
|----------------|------------------|---------|
| 1-4 donations | 1.0× | New Donor |
| 5-9 donations | 1.1× | Regular Donor |
| 10-19 donations | 1.2× | Committed Donor |
| 20-49 donations | 1.5× | Champion Donor |
| 50+ donations | 2.0× | Legend Donor |

### **4. Calculation Examples**

| Scenario | Item | User Donations | Base | Urgency | Frequency | **Final Points** |
|----------|------|----------------|------|---------|-----------|------------------|
| New user, food | food | 0 | 100 | 1.5× | 1.0× | **150** |
| Regular, medical | medical_supplies | 7 | 100 | 2.0× | 1.1× | **220** |
| Champion, clothing | clothing | 25 | 100 | 1.2× | 1.5× | **180** |
| Legend, books | books | 60 | 100 | 1.1× | 2.0× | **220** |

## 🏆 Rank Progression System

| Rank | Point Range | Badge | Unlock Message |
|------|-------------|-------|----------------|
| 🥉 **Bronze** | 0 - 499 | Newcomer | "Welcome to the platform!" |
| 🥈 **Silver** | 500 - 1,999 | Contributor | "Making a difference!" |
| 🥇 **Gold** | 2,000 - 4,999 | Champion | "Community champion!" |
| 💎 **Platinum** | 5,000 - 9,999 | Hero | "True hero of giving!" |
| 💎✨ **Diamond** | 10,000+ | Legend | "Legendary philanthropist!" |

### **Rank Benefits**
- **Visual Recognition**: Badge display in user profile
- **Automatic Calculation**: Rank updates with every donation
- **Gamification**: Encourages continued participation

## 📁 Project Structure

```
donation-platform/
├── 📜 main.py                 # FastAPI application with all endpoints
├── 💾 database.py             # SQLAlchemy models and database setup
├── 📋 schemas.py              # Pydantic models for API validation
├── 📄 requirements.txt        # Python dependencies
├── 📚 README.md              # This comprehensive guide
├── 🧪 TESTING.md             # Detailed testing instructions
├── ⚡ verify_setup.py         # Setup verification script
├── 🧪 test_api.py            # API test suite
├── 🚀 setup.bat              # Windows first-time setup
├── 🚀 setup.sh               # Linux/macOS first-time setup
├── 🚀 run_server.bat         # Windows server launcher
├── 🚀 run_server.sh          # Linux/macOS server launcher
├── 🚀 run_server.ps1         # PowerShell server launcher
├── 🧪 run_tests.bat          # Windows test runner
├── 🔧 activate_env.bat       # Windows environment activator
├── 🔍 check_python.bat       # Python environment diagnostics
├── 📊 donation_platform.db   # SQLite database (auto-created)
├── 🔒 .gitignore            # Git ignore rules
└── 🗂️ .venv/                # Virtual environment (auto-created)
```

## 🛠️ Utility Scripts

### **📦 Setup Scripts**
- **`setup.bat`** (Windows) / **`setup.sh`** (Linux/macOS) - First-time setup
- **`activate_env.bat`** - Manually activate Windows environment

### **🚀 Server Management**  
- **`run_server.bat`** (Windows) / **`run_server.sh`** (Linux/macOS) - Start server
- **`run_server.ps1`** - PowerShell server launcher (Windows alternative)

### **🧪 Development & Testing**
- **`verify_setup.py`** - Verify all dependencies and setup
- **`test_api.py`** - Comprehensive API test suite
- **`run_tests.bat`** - Run all tests (Windows)
- **`check_python.bat`** - Diagnose Python environment issues (Windows)

### **🎯 Quick Commands**

**Windows:**
```bash
# First time setup
setup.bat

# Start server  
.\run_server.bat

# Run tests
.\run_tests.bat

# Check environment
.\check_python.bat
```

**Linux/macOS:**
```bash
# First time setup
./setup.sh

# Start server
./run_server.sh

# Manual setup alternative
source .venv/bin/activate
python main.py
```

**Universal (after environment activation):**
```bash
python main.py              # Start server
python test_api.py           # Run tests  
python verify_setup.py       # Verify setup
```

## 🏅 What Makes This Special

### **Production-Ready Features**
- ✅ **Input Validation** - Pydantic schemas prevent bad data
- ✅ **Error Handling** - Proper HTTP status codes and error messages
- ✅ **Database Relationships** - Foreign keys and data integrity
- ✅ **Automatic Documentation** - Interactive API docs at `/docs`
- ✅ **Type Hints** - Full typing support for better development
- ✅ **Async Support** - FastAPI's async capabilities for performance

### **Smart Business Logic**
- 🧠 **Dynamic Scoring** - Points adapt to current needs
- 🎮 **Gamification** - Ranks and bonuses encourage engagement
- 📊 **Analytics Ready** - Complete donation tracking for insights
- 🔄 **Scalable Architecture** - Easy to extend with new features

### **Developer Experience**
- 🚀 **One-Click Setup** - Batch files for easy deployment
- 🧪 **Comprehensive Testing** - Automated test suite included
- 📖 **Detailed Documentation** - Every endpoint and feature explained
- 🔧 **Debugging Tools** - Environment verification utilities

## 🌟 Next Steps / Extensions

This platform is designed to be easily extensible. Consider adding:

- **User Authentication** - JWT tokens for secure access
- **Location-Based Matching** - Connect donors with nearby needs
- **Photo Uploads** - Visual confirmation of donations  
- **Push Notifications** - Alerts for urgent needs
- **Analytics Dashboard** - Visual reporting for administrators
- **Mobile App Integration** - React Native or Flutter frontend
- **Social Features** - Share achievements, team challenges
- **Inventory Tracking** - Track actual items received

---

## 📧 Support

- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check `TESTING.md` for detailed testing
- **Setup Issues**: Run `check_python.bat` for diagnostics

Built with ❤️ for the hackathon community!
