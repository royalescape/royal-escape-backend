# royal-escape-backend
Python backend service for RE
Create a Postman Environment named Royal Escape-Local:

{
  "base_url": "http://localhost:8000",
  "user_jwt": "",
  "admin_jwt": "",
  "pot_id": ""
}

Recommended Testing Flow

🔹 Admin

Create pot → copy pot_id

Activate pot

Wait for entries

Close pot manually (status = closed)

Declare winner

🔹 User

View pots

View pot

Enter pot

Check entries


🔐 JWT Reminder

User JWT → role = user

Admin JWT → role = admin

Admin-only routes will 403 if role is wrong (as expected).