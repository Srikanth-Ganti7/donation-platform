# 🧪 MANUAL TESTING GUIDE
# Complete step-by-step testing of all donation platform features

## 🚀 STEP 1: Start Your Server

### Windows:
```bash
.\run_server.bat
```

### Linux/macOS:
```bash
./run_server.sh
```

### Manual:
```bash
python main.py
```

**Expected Output:**
```
🚀 Starting Donation Platform API on port 8000
📖 Interactive docs: http://localhost:8000/docs
❤️  Health check: http://localhost:8000/ping
INFO:     Started server process [xxxxx]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 🌐 STEP 2: Open Interactive Documentation

1. **Visit**: http://localhost:8000/docs
2. **You should see**: Beautiful Swagger UI with all your endpoints
3. **Test health check**: Click on `/ping` → "Try it out" → "Execute"
   - **Expected**: `{"message": "pong"}`

## 👥 STEP 3: Test User Management

### 3.1 Create Users
1. **Click**: `POST /users/` → "Try it out"
2. **Enter**: `{"name": "Alice Johnson"}`
3. **Execute** → **Expected Response**:
   ```json
   {
     "id": 1,
     "name": "Alice Johnson", 
     "points": 0,
     "rank": "Bronze",
     "donations_count": 0
   }
   ```

4. **Create more users**:
   - `{"name": "Bob Smith"}`
   - `{"name": "Charlie Brown"}`

### 3.2 Get All Users
1. **Click**: `GET /users/` → "Try it out" → "Execute"
2. **Expected**: Array with all created users

### 3.3 Get Specific User
1. **Click**: `GET /users/{user_id}` → "Try it out"
2. **Enter**: `1` (user ID)
3. **Execute** → **Expected**: Alice Johnson's details

## 🎯 STEP 4: Check Pre-populated Needs

1. **Click**: `GET /needs/` → "Try it out" → "Execute"
2. **Expected Response** (6 items):
   ```json
   [
     {"id": 1, "item_type": "food", "urgency_level": "high", "multiplier": 1.5},
     {"id": 2, "item_type": "clothing", "urgency_level": "medium", "multiplier": 1.2},
     {"id": 3, "item_type": "toys", "urgency_level": "low", "multiplier": 1.0},
     {"id": 4, "item_type": "medical_supplies", "urgency_level": "critical", "multiplier": 2.0},
     {"id": 5, "item_type": "books", "urgency_level": "medium", "multiplier": 1.1},
     {"id": 6, "item_type": "electronics", "urgency_level": "low", "multiplier": 1.0}
   ]
   ```

## 💰 STEP 5: Test Point Calculation System

### 5.1 Basic Donation (Food - High Urgency)
1. **Click**: `POST /donate` → "Try it out"
2. **Enter**:
   ```json
   {
     "user_id": 1,
     "item_type": "food",
     "location": "New York, NY"
   }
   ```
3. **Execute** → **Expected**:
   ```json
   {
     "user_id": 1,
     "points_awarded": 150,
     "total_points": 150
   }
   ```
   **Math**: 100 (base) × 1.5 (urgency) × 1.0 (frequency) = 150

### 5.2 Critical Donation (Medical Supplies)
1. **Same user, enter**:
   ```json
   {
     "user_id": 1,
     "item_type": "medical_supplies", 
     "location": "Los Angeles, CA"
   }
   ```
2. **Expected**: 200 points awarded (100 × 2.0 × 1.0)
3. **Total should be**: 350 points

### 5.3 Unknown Item Type
1. **Enter**:
   ```json
   {
     "user_id": 1,
     "item_type": "furniture",
     "location": "Chicago, IL"
   }
   ```
2. **Expected**: 100 points (default 1.0x multiplier)
3. **Total should be**: 450 points

## 🏆 STEP 6: Test Rank Progression

### 6.1 Check Current Rank
1. **Click**: `GET /users/1` → "Execute"
2. **Expected**: Still "Bronze" (450 points < 500)

### 6.2 Reach Silver Rank
1. **Make one more donation** to reach 500+ points:
   ```json
   {
     "user_id": 1,
     "item_type": "food",
     "location": "Miami, FL"
   }
   ```
2. **Check user again** → **Expected**: `"rank": "Silver"`

## 🔄 STEP 7: Test Frequency Bonus System

### 7.1 Create Fresh User
1. **Create**: `{"name": "Frequent Donor"}`
2. **Note the user ID** (probably 2)

### 7.2 Make 5 Donations
Make 5 donations with the new user:
```json
{
  "user_id": 2,
  "item_type": "books",
  "location": "Test Location 1"
}
```
**Expected per donation**: 110 points (100 × 1.1 × 1.0)

### 7.3 Test Frequency Bonus (6th Donation)
1. **Make 6th donation**:
   ```json
   {
     "user_id": 2,
     "item_type": "books", 
     "location": "Test Location 6"
   }
   ```
2. **Expected**: 121 points (100 × 1.1 × 1.1 frequency bonus)

## 📊 STEP 8: Test Donation History

### 8.1 Get All Donations
1. **Click**: `GET /donations/` → "Execute"
2. **Expected**: List of all donations made

### 8.2 Get User-Specific Donations  
1. **Click**: `GET /donations/user/{user_id}` → Enter `1` → "Execute"
2. **Expected**: Only Alice Johnson's donations

## ❌ STEP 9: Test Error Handling

### 9.1 Invalid User ID
1. **Try donation with nonexistent user**:
   ```json
   {
     "user_id": 99999,
     "item_type": "food",
     "location": "Test"
   }
   ```
2. **Expected**: 404 error with "User not found"

### 9.2 Invalid User Lookup
1. **Click**: `GET /users/99999` → "Execute"
2. **Expected**: 404 error

### 9.3 Invalid Input Data
1. **Try creating user with missing name**:
   ```json
   {
     "invalid_field": "test"
   }
   ```
2. **Expected**: 422 validation error

## 🔧 STEP 10: Test Additional Endpoints

### 10.1 Create Custom Need
1. **Click**: `POST /needs/` → "Try it out"
2. **Enter**:
   ```json
   {
     "item_type": "blankets",
     "urgency_level": "high", 
     "multiplier": 1.8
   }
   ```
3. **Test donation with new need** → Should get 180 points (100 × 1.8)

## ✅ EXPECTED RESULTS SUMMARY

| Test | Expected Result |
|------|----------------|
| Health Check | `{"message": "pong"}` |
| User Creation | Bronze rank, 0 points, 0 donations |
| Food Donation | 150 points (1.5× multiplier) |
| Medical Donation | 200 points (2.0× multiplier) |
| Unknown Item | 100 points (1.0× default) |
| Rank Change | Bronze → Silver at 500+ points |
| Frequency Bonus | 1.1× bonus after 5 donations |
| Error Handling | Proper 404/422 status codes |

## 🏁 SUCCESS CRITERIA

✅ **All endpoints respond correctly**
✅ **Point calculations match expected values**  
✅ **Rank progression works (Bronze → Silver)**
✅ **Frequency bonus applies after 5 donations**
✅ **Error handling returns proper status codes**
✅ **Database persistence (refresh page, data remains)**

## 🚨 TROUBLESHOOTING

**Server won't start?**
- Check if port 8000 is free
- Run `.\check_python.bat` (Windows) to diagnose

**API not responding?**
- Verify server is running
- Check the correct URL (port might be different)
- Try http://localhost:8001 or 8002

**Unexpected results?**
- Run automated test: `python comprehensive_test.py`
- Check server console for error messages

---

**🎉 If all tests pass, your donation platform is production-ready!**
