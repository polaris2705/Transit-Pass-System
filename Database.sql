-- Users
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mobile VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Commuter','Validator','Admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transport Modes
CREATE TABLE TransportModes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE
);

-- Pass Types
CREATE TABLE PassTypes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    validity_days INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    transport_modes TEXT,
    max_trips_per_day INT
);

-- Purchased Passes
CREATE TABLE UserPasses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pass_type_id INT NOT NULL,
    pass_code VARCHAR(100) UNIQUE,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (pass_type_id) REFERENCES PassTypes(id)
);

-- Trip Validations
CREATE TABLE Trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_pass_id INT NOT NULL,
    validated_by INT,
    transport_mode VARCHAR(50),
    route_info TEXT,
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_pass_id) REFERENCES UserPasses(id),
    FOREIGN KEY (validated_by) REFERENCES Users(id)
);