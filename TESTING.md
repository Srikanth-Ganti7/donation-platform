# API Testing Commands

## Quick Start
1. Start the server: `python main.py`
2. Server will be available at: http://localhost:8000
3. Interactive docs: http://localhost:8000/docs

## curl Testing Commands

### Health Check
```bash
curl -X GET "http://localhost:8000/ping"
```
Expected response: `{"message":"pong"}`

### Create Users
```bash
# Create first user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson"}'

# Create second user  
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob Smith"}'
```

### View Current Needs
```bash
curl -X GET "http://localhost:8000/needs/"
```

### Make Donations

#### Test Case 1: Regular donation (clothing - medium urgency)
```bash
curl -X POST "http://localhost:8000/donate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "item_type": "clothing", 
    "location": "New York, NY"
  }'
```
Expected: ~120 points (100 × 1.2 urgency × 1.0 frequency)

#### Test Case 2: High urgency donation (food)
```bash
curl -X POST "http://localhost:8000/donate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "item_type": "food",
    "location": "Los Angeles, CA" 
  }'
```
Expected: 150 points (100 × 1.5 urgency × 1.0 frequency)

#### Test Case 3: Critical urgency donation (medical supplies)
```bash
curl -X POST "http://localhost:8000/donate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "item_type": "medical_supplies",
    "location": "Chicago, IL"
  }'
```
Expected: 200 points (100 × 2.0 urgency × 1.0 frequency)

#### Test Case 4: Multiple donations for frequency bonus
```bash
# Make 5 more donations to trigger frequency bonus
for i in {1..5}; do
  curl -X POST "http://localhost:8000/donate" \
    -H "Content-Type: application/json" \
    -d "{
      \"user_id\": 1,
      \"item_type\": \"books\",
      \"location\": \"Location $i\"
    }"
done
```

#### Test Case 5: Donation with frequency bonus
```bash
curl -X POST "http://localhost:8000/donate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "item_type": "books",
    "location": "Miami, FL"
  }'
```
Expected: 121 points (100 × 1.1 urgency × 1.1 frequency)

### View User Details
```bash
# Get specific user
curl -X GET "http://localhost:8000/users/1"

# Get all users
curl -X GET "http://localhost:8000/users/"
```

### View Donations
```bash
# Get all donations
curl -X GET "http://localhost:8000/donations/"

# Get donations for specific user
curl -X GET "http://localhost:8000/donations/user/1"
```

## PowerShell Testing Script

Create a file called `test_api.ps1` and run these commands:

```powershell
# Test the donation platform API

Write-Host "🚀 Testing Donation Platform API" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Health check
Write-Host "`n1. Testing health endpoint..." -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "http://localhost:8000/ping" -Method Get
Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Cyan

# Create user
Write-Host "`n2. Creating user..." -ForegroundColor Yellow
$userBody = @{
    name = "Test User PowerShell"
} | ConvertTo-Json

$user = Invoke-RestMethod -Uri "http://localhost:8000/users/" -Method Post -Body $userBody -ContentType "application/json"
Write-Host "User created: $($user | ConvertTo-Json)" -ForegroundColor Cyan
$userId = $user.id

# Make donation
Write-Host "`n3. Making donation..." -ForegroundColor Yellow
$donationBody = @{
    user_id = $userId
    item_type = "food"
    location = "PowerShell Test Location"
} | ConvertTo-Json

$donation = Invoke-RestMethod -Uri "http://localhost:8000/donate" -Method Post -Body $donationBody -ContentType "application/json"
Write-Host "Donation result: $($donation | ConvertTo-Json)" -ForegroundColor Cyan

# Get updated user
Write-Host "`n4. Getting updated user..." -ForegroundColor Yellow
$updatedUser = Invoke-RestMethod -Uri "http://localhost:8000/users/$userId" -Method Get
Write-Host "Updated user: $($updatedUser | ConvertTo-Json)" -ForegroundColor Cyan

Write-Host "`n✅ All tests completed successfully!" -ForegroundColor Green
```

## Expected Results Summary

| Test Case | Item Type | Urgency | Frequency Bonus | Expected Points |
|-----------|-----------|---------|-----------------|-----------------|
| 1 | clothing | 1.2× | 1.0× | 120 |
| 2 | food | 1.5× | 1.0× | 150 |  
| 3 | medical_supplies | 2.0× | 1.0× | 200 |
| 4 | books (after 5+ donations) | 1.1× | 1.1× | 121 |

## Database Verification

Check the SQLite database directly:
```bash
# Install SQLite (if not installed)
# On Windows: Download from https://sqlite.org/download.html

# View tables
sqlite3 donation_platform.db ".tables"

# View all users
sqlite3 donation_platform.db "SELECT * FROM users;"

# View all donations  
sqlite3 donation_platform.db "SELECT * FROM donations;"

# View needs configuration
sqlite3 donation_platform.db "SELECT * FROM needs;"

# Complex query: User donations with points
sqlite3 donation_platform.db "
SELECT 
  u.name,
  u.points,
  u.rank,
  u.donations_count,
  d.item_type,
  d.location,
  d.points_awarded,
  d.timestamp
FROM users u
JOIN donations d ON u.id = d.user_id
ORDER BY d.timestamp DESC;
"
```
