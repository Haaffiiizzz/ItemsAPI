# from sqlalchemy.orm import Session
# from database import engine, SessionLocal
# from models import Country, Country2
# import json

# with open("countries.json", "r") as file:
#     countriesDict = json.load(file)

# session = SessionLocal()
# try:
    
#     for country_name, (currency, items) in countriesDict.items():
        
#         private_entry = Country(country=country_name, items={"currency": currency, "prices": items})
#         session.add(private_entry)
        
        
#         public_entry = Country2(country=country_name, items={"currency": currency, "prices": items})
#         session.add(public_entry)
    
    
#     session.commit()
#     print("Data successfully added to the database.")
# except Exception as e:
#     # Rollback in case of an error
#     session.rollback()
#     print(f"An error occurred: {e}")
# finally:
#     # Close the session
#     session.close()
