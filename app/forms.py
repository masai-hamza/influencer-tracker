from flask_wtf import FlaskForm  
from wtforms import StringField, SelectField, SubmitField, DateField, DecimalField
from wtforms.validators import DataRequired, URL, NumberRange  

class InfluencerForm(FlaskForm):  
    influencer_name = SelectField("Influencer Name", choices=[], validators=[DataRequired()])  
    unique_id = StringField("Unique ID", render_kw={"readonly": True})  
    channel_name = SelectField(  
        "Channel Name",  
        choices=[("Instagram", "Instagram"), ("Youtube", "Youtube"), ("LinkedIn", "LinkedIn"), ("Telegram", "Telegram"), ("Whatsapp", "Whatsapp")],  
        validators=[DataRequired()]  
    )    
    profile = StringField("Influencer Profile", validators=[DataRequired()])  
    activation_for = StringField("Activation For", validators=[DataRequired()])  
    platform = SelectField(  
        "Platform",  
        choices=[("Story", "Story"), ("Reel", "Reel"), ("Both", "Both"), ("Other", "Other")],  
        validators=[DataRequired()]  
    )
    cost = DecimalField("Cost", validators=[NumberRange(min=0)], places=2)  
    tentative_live_date = DateField("Tentative Live Date", format="%Y-%m-%d", validators=[DataRequired()])  # DateField
    landing_page_url = StringField("Landing Page URL", validators=[DataRequired(), URL()])  
    utm_source = StringField("UTM Source", validators=[DataRequired()])
    utm_medium = StringField("UTM Medium", validators=[DataRequired()])
    utm_campaign = StringField("UTM Campaign", validators=[DataRequired()])
    submit = SubmitField("Go Live")  

class UpdateLiveDateForm(FlaskForm):  
    influencer_name = SelectField("Influencer Name", choices=[], validators=[DataRequired()])  # Dropdown populated dynamically  
    live_date = SelectField("Existing Live Date", choices=[], validators=[DataRequired()])  # Populated dynamically  
    new_date = DateField("New Tentative Live Date", validators=[DataRequired()])  # Date input  
    update = SubmitField("Update Live Date")  