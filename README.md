# ItemsAPI

ItemsAPI is a FastAPI-based application that provides country-specific data and comparisons. It currently supports retrieving data for all available countries and **fetching** details for a single country.

**Hosted API Documentation:** [ItemsAPI doc](https://itemsapi.abdulhafizdada.com/docs)

## Endpoints

- **GET /**  
  Returns a simple welcome message and a **list** of countries available.

- **GET /countries**  
  Retrieves data for all available countries in the database.

- **GET /countries/{country}**  
  Retrieves data for a specific country.

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL (via Supabase)
- **ORM:** SQLAlchemy
- **Deployment:** Hosted on Heroku
