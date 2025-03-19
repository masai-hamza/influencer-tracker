from datetime import datetime  
from app import db  

class Influencer(db.Model):  
    __tablename__ = "influencers"  

    unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    name = db.Column(db.String(100), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # New field  

    def __repr__(self):  
        return f"<Influencer {self.name}>"  

class IM_Tracker(db.Model):  
    __tablename__ = "im_tracker"  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    influencer_name = db.Column(db.String(100), nullable=False)  
    unique_id = db.Column(db.Integer, db.ForeignKey("influencers.unique_id"), nullable=False)  
    channel_name = db.Column(db.String(100), nullable=False)  
    profile = db.Column(db.String(100), nullable=False)  
    # activation_for = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    cohort_id = db.Column(db.Integer, nullable=True) 
    platform = db.Column(db.String(100), nullable=False)  # Dropdown  
    tentative_live_date = db.Column(db.Date, nullable=False)  
    landing_page_url = db.Column(db.String(200), nullable=False)  
    utm_source = db.Column(db.String(100), nullable=False)  
    utm_medium = db.Column(db.String(100), nullable=False)  
    utm_campaign = db.Column(db.String(100), nullable=False)  
    utm_string = db.Column(db.String(200), nullable=False)  
    cost = db.Column(db.Numeric, nullable=True)  # New field  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # New field  
    updated_at = db.Column(db.DateTime, nullable=True)  # New field  

    def __repr__(self):  
        return f"<IM_Tracker {self.influencer_name}>"  