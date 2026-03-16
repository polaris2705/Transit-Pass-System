# Transit-Pass-System


## Overview
An application aimed at creating a digital transit pass system for urban public transportation management.  

A web-based pass system that allows users to register, log in, view trips, and validate passes. Admins can monitor passes and view analytics. The system consists of a **Streamlit frontend**, a **FastAPI backend**, and a **MySQL database**.

---

## Tech Stack
- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Database:** MySQL  
- **Deployment:** Render (frontend and backend deployed separately)  

---

## Setup Instructions

## 1. Clone the Repository
```bash
git clone https://github.com/polaris2705/Transit-Pass-System.git
cd Transit-Pass-System
```

### Local Setup

#### Backend
1. Navigate to backend folder:

```bash
cd Backend
```
2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the backend locally:
```bash
uvicorn app.main:app --reload
```
This starts the backend at http://localhost:8000


Frontend

1. Navigate to frontend folder:
```bash
cd Frontend
```
2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the frontend locally:
```bash
streamlit run streamlit_app.py
```
Note: The frontend is configured to use the deployed backend by default. For local testing, you can set the `API_URL` environment variable to your local backend URL (http://localhost:8000).
```bash
export API_URL=http://localhost:8000   # Linux/Mac
set API_URL=http://localhost:8000      # Windows
```
---

## Deployed Application

Frontend URL: https://transit-pass-system-frontend.onrender.com/

Backend URL: https://transit-pass-system.onrender.com/

On Render free-tier, the backend may take a few seconds to wake if idle. Refresh the frontend if the first request fails.

## Using the Deployed Application

1. Open the deployed frontend.
2. Log in using one of the accounts below.
3. The interface will display features based on the user's role.

For example:

- **Commuter** – purchase and view transit passes
- **Validator** – validate commuter passes
- **Admin** – manage pass types and monitor system activity

### Demo Accounts (Seeded Users)

To simulate a real transit system, the database is automatically seeded with system users when the application starts.  
These accounts allow testing of validator and admin functionality without manual setup.

The following credentials can be used to log in through the deployed application.

| User ID | Role | Email                 | Password | Purpose                                       |
|---------|-----|-----------------------|-----|-----------------------------------------------|
| 1       | Validator | validator@transit.com | validator123 | Validate commuter passes during trips         |
| 2       | Admin        | admin@transit.com     | admin123 | Manage pass types and view system statistics  |


Alternately, register with your Name, E-mail, Mobile and Password to login as a new commuter.

Refresh page to 'logout'

Imp: Register and validate pass before logging in as admin


---

## API Documentation

### Access Swagger UI
- FastAPI interactive API docs at:
  - **Swagger UI:** https://transit-pass-system.onrender.com/docs
- You can visit this URL in a browser to explore all endpoints, see request/response schemas, and test APIs interactively.
### OpenAPI testing
OpenAPI JSON specification is included in this repository under:

docs/openapi.json

---

## Using the `x-user-id` Header

Several endpoints require the request header: x-user-id

This header simulates authenticated users in the system.

### How to Obtain a User ID

1. Register a user using:
POST /api/auth/register
Example request body:

```json
{
  "name": "Test User",
  "mobile": "9999999999",
  "email": "test@example.com",
  "password": "password123"
}
```
2. The response will return the created user:
```json{
  "id": 5,
  "name": "Test User",
  "mobile": "9999999999",
  "email": "test@example.com",
  "role": "Commuter",
  "created_at": "2026-03-15T17:57:16.930Z"
}
```
3. Use the returned id as the header value in protected endpoints.

Example:
```
x-user-id: 5
```

## Seeded System Users

To simulate a realistic transit system, the database is automatically seeded during application startup.

The following system roles are pre-created:

**Validator**: 	Used to validate transit passes during trips

**Admin**:	    Used for managing pass types and viewing system statistics

These users allow testing of validator and administrative endpoints without manually creating those roles.

Example

When testing pass validation:
```
POST /api/validate
```
Include the follwing validator ID in the request header:
```
x-user-id: 1
```


---

### Key Endpoints (Summary)

#### Authentication
- `POST /api/auth/register` – register a new user  
- `POST /api/auth/login` – login user/admin  

#### Passes
- `GET /api/passes/types` – get available pass types  
- `POST /api/passes/purchase` – purchase a pass  
- `GET /api/passes/my-passes` – get user’s passes  
- `GET /api/passes/{pass_code}` – get details of a specific pass  

#### Validation
- `POST /api/validate` – validate a pass (admin or authorized personnel)  

#### Trips
- `GET /api/trips/history` – get trip history for logged-in user  

#### Admin
- `GET /api/admin/dashboard` – get dashboard stats  
- `GET /api/admin/pass-types` – list pass types  
- `POST /api/admin/pass-types` – create pass type  
- `PUT /api/admin/pass-types/{pass_type_id}` – update pass type  
- `DELETE /api/admin/pass-types/{pass_type_id}` – delete pass type  

---

## Assumptions

1. Users must register before accessing trips or passes
2. Admin dashboard displays stats after passes are purchases and successfully validated
2. Admins have privileges to view analytics, create/update pass types, and validate passes 
3. Expired passes are automatically flagged and cannot be used for validation 
4. Timestamps for trips, passes, and validations are stored in UTC
5. Each user can only hold one active pass of a given type at a time 
6. Frontend defaults to the deployed backend URL; local testing requires setting `API_URL` manually 
7. The deployed backend may take a few seconds to wake up if idle (Render free-tier)  

## Known Limitations

1. Backend sleep delay: On Render free-tier, the backend may need a few seconds to respond after being idle; first requests may fail.  
2. Minimal error handling for invalid inputs
3. Admin dashboard displays stats after passes are purchases and successfully validated
4. No email verification or password reset implemented for user accounts 
5. Frontend is a single-page Streamlit interface. Multi-page navigation is not implemented 
6. Local testing requires a running MySQL server with correct `DATABASE_URL`  
7. System designed for small-scale use. Not robust enough to deal with high traffic
8. Payment is simulated