from app.database import engine
from sqlmodel import SQLModel
from app import models 

def reset_database():
    print("🗑️  Dropping all tables...")
    # Use CASCADE to drop tables even if they have dependent objects (foreign keys)
    with engine.begin() as connection:
        connection.exec_driver_sql("DROP TABLE IF EXISTS votes CASCADE")
        connection.exec_driver_sql("DROP TABLE IF EXISTS follows CASCADE")
        connection.exec_driver_sql("DROP TABLE IF EXISTS posts CASCADE")
        connection.exec_driver_sql("DROP TABLE IF EXISTS users_v2 CASCADE")
    
    print("✨  Creating new tables...")
    SQLModel.metadata.create_all(engine)
    
    print("✅  Database has been reset!")

if __name__ == "__main__":
    reset_database()