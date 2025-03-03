from app import db  

class Influencer(db.Model):  
    __tablename__ = "influencers"  

    unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing primary key  
    name = db.Column(db.String(100), nullable=False)  
    channel_name = db.Column(db.String(100), nullable=False)  
    profile = db.Column(db.String(100), nullable=False)  

    def __repr__(self):  
        return f"<Influencer {self.name}>"  

class IM_Tracker(db.Model):  
    __tablename__ = "im_tracker"  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    influencer_name = db.Column(db.String(100), nullable=False)  
    unique_id = db.Column(db.Integer, db.ForeignKey("influencers.unique_id"), nullable=False)  # Foreign key  
    channel_name = db.Column(db.String(100), nullable=False)  
    profile = db.Column(db.String(100), nullable=False)  
    activation_for = db.Column(db.String(100), nullable=False)  
    platform = db.Column(db.String(100), nullable=False)  
    tentative_live_date = db.Column(db.Date, nullable=False)  
    landing_page_url = db.Column(db.String(200), nullable=False) 
    utm_source = db.Column(db.String(100), nullable=False)
    utm_medium = db.Column(db.String(100), nullable=False)
    utm_campaign = db.Column(db.String(100), nullable=False)
    utm_string = db.Column(db.String(200), nullable=False)  

    def __repr__(self):  
        return f"<IM_Tracker {self.influencer_name}>"