# config.py  
import os  

class Config: 
    SECRET_KEY = os.getenv("SECRET_KEY", "09aaa368aada176812c0443f275c915e") 
    SQLALCHEMY_DATABASE_URI = os.getenv(  
        "DATABASE_URL","postgresql://postgres:c29O5VLtglNppCqlVXus@analyticsdb.crfg8xlnzwpc.ap-south-1.rds.amazonaws.com:5432/analytics-db"
    ) 
    SQLALCHEMY_BINDS = {  # Add a bind for the second DB (Onwards DB)  
        "onwards": os.getenv(  
            "ONWARDS_DB_URL", "mysql+pymysql://readonly:qSNCYBYHjirJbOoWzpDy0YeNYjX5jUQv@masai-one-db-readonly.crfg8xlnzwpc.ap-south-1.rds.amazonaws.com:3306/masai_one"  
        )  
    }  
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event system for performance  
