users collection

{
"_id": ObjectId,
"phone": "+9199XXXXXXX",
"email": "user@email.com",
"name": "John Doe",
"address": {
"line1": "Street",
"city": "Pune",
"state": "MH",
"pincode": "411028"
},
"is_verified": true,
"created_at": ISODate,
"updated_at": ISODate
}


user_wallets
{
"_id": ObjectId,
"user_id": ObjectId,
"balance": 1250.50,
"currency": "INR",
"updated_at": ISODate
}

user_transactions

{
"_id": ObjectId,
"user_id": ObjectId,
"type": "credit | debit",
"amount": 200,
"source": "wallet | pot_entry | winning",
"reference_id": ObjectId,
"created_at": ISODate
}

user_entries

{
"_id": ObjectId,
"user_id": ObjectId,
"pot_id": ObjectId,
"entry_count": 3,
"created_at": ISODate
}

user_winnings
{
"_id": ObjectId,
"user_id": ObjectId,
"pot_id": ObjectId,
"amount": 5000,
"won_at": ISODate
}



# db.users.createIndex({ phone: 1 }, { unique: true })
# db.users.createIndex({ email: 1 }, { unique: true, sparse: true })
# db.user_wallets.createIndex({ user_id: 1 }, { unique: true })
# db.user_entries.createIndex({ user_id: 1, pot_id: 1 })