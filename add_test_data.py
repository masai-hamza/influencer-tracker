from app import create_app, db  
from app.models import Influencer, IM_Tracker  
from datetime import datetime  

app = create_app()  

with app.app_context():  
    # Add a test influencer  
    influencer = Influencer(name="Test Influencer", created_at=datetime.utcnow())  
    db.session.add(influencer)  
    db.session.flush()  # Get the unique_id of the newly added influencer  

    # Add a test IM_Tracker record  
    tracker = IM_Tracker(  
        influencer_name="Test Influencer",  
        unique_id=influencer.unique_id,  
        channel_name="Instagram",  
        profile="https://instagram.com/test",  
        activation_for="Product Launch",  
        platform="Instagram",  
        tentative_live_date=datetime.utcnow().date(),  
        landing_page_url="https://example.com",  
        utm_source="test_source",  
        utm_medium="test_medium",  
        utm_campaign="test_campaign",  
        utm_string="https://example.com?utm_source=test_source&utm_medium=test_medium&utm_campaign=test_campaign",  
        cost=100.50,  
        created_at=datetime.utcnow(),  
    )  
    db.session.add(tracker)  
    db.session.commit()  

    print("Test data added successfully!")  