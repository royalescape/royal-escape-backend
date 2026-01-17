from app.core.security import create_access_token, decode_access_token

# Replace with a REAL user_id from MongoDB
ADMIN_USER_ID = "696236f8cd89ef4240368335"

token = create_access_token(subject=ADMIN_USER_ID, role="admin")

print("\nADMIN JWT TOKEN:\n")
print(token)
print("\n")
print(decode_access_token(token))
