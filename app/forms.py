from flask_wtf import FlaskForm  
from wtforms import StringField, SelectField, SubmitField, DateField  
from wtforms.validators import DataRequired, URL  

class InfluencerForm(FlaskForm):  
    influencer_name = SelectField("Influencer Name", choices=[], validators=[DataRequired()])  
    unique_id = StringField("Unique ID", render_kw={"readonly": True})  
    channel_name = StringField("Channel Name", validators=[DataRequired()])  
    profile = StringField("Influencer Profile", validators=[DataRequired()])  
    activation_for = StringField("Activation For", validators=[DataRequired()])  
    platform = StringField("Platform", validators=[DataRequired()])  
    tentative_live_date = DateField("Tentative Live Date", format="%Y-%m-%d", validators=[DataRequired()])  # DateField
    landing_page_url = StringField("Landing Page URL", validators=[DataRequired(), URL()])  
    utm_source = StringField("UTM Source", validators=[DataRequired()])
    utm_medium = StringField("UTM Medium", validators=[DataRequired()])
    utm_campaign = StringField("UTM Campaign", validators=[DataRequired()])
    submit = SubmitField("Go Live")  