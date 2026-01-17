from app.core.security import create_access_token, decode_access_token

# Replace with a REAL user_id from MongoDB
ADMIN_USER_ID = "696ba7223a81fe1f5d742fbf"

token = create_access_token(subject=ADMIN_USER_ID, role="admin")

print("\nADMIN JWT TOKEN:\n")
print(token)
print("\n")
print(decode_access_token(token))
