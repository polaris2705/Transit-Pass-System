-- User Profile
CREATE TABLE Users{
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
}

-- Pass Properties 
CREATE TABLE PassTypes{
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
validity_days INTEGER,
price REAL,
transport_modes TEXT,
max_trips_per_day INTEGER
}

-- A User's Purchased Pass
CREATE TABLE UserPasses{
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
pass_type_id INTEGER,
pass_code TEXT UNIQUE,
purchase_date TIMESTAMP,
expiry_date TIMESTAMP,
status TEXT,
FOREIGN KEY user_id REFERENCES Users(id),
FOREIGN KEY pass_type_id REFERENCES PassTypes(id)
}

-- Validated Trips 
CREATE TABLE Trips{
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_pass_id INTEGER,
    validated_by INTEGER,
    transport_mode TEXT,
    route_info TEXT,
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY user_pass_id REFERENCES UserPasses(id),
    FOREIGN KEY validated_by REFERENCES Users(id)
}

-- Transport Modes
CREATE TABLE TansportModes{
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE
}