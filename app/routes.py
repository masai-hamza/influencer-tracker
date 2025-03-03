from flask import Blueprint, render_template, request, redirect, url_for, flash  
from app import db  
from app.models import Influencer, IM_Tracker  
from app.forms import InfluencerForm  
import uuid  

main = Blueprint("main", __name__)  

# Function to generate the UM String  
def generate_um_string(influencer_name, landing_page_url,utm_source,utm_medium,utm_campaign):  
    """  
    Generate a UM String based on the influencer name and landing page URL.  
    Modify this function in the future as needed.  
    """  
    return f"{landing_page_url.lower()}?utm_source={utm_source.lower()}&utm_medium={utm_medium.lower()}&utm_campaign={utm_campaign.lower()}"
  

@main.route("/", methods=["GET", "POST"])  
def home():  
    form = InfluencerForm()  
    form.influencer_name.choices = [(i.unique_id, i.name) for i in Influencer.query.all()]  # Use unique_id as the key  

    # Check if the user is adding a new influencer  
    is_adding_new = request.args.get("add_new", "false").lower() == "true"  
    um_string = None  # To display the UM String on the UI  

    if request.method == "POST":  
        if is_adding_new:  # Adding a new influencer  
            # Collect data from the form  
            name = request.form.get("influencer_name")  
            channel_name = request.form.get("channel_name")  
            profile = request.form.get("profile")  
            activation_for = request.form.get("activation_for")  
            platform = request.form.get("platform")  
            tentative_live_date = form.tentative_live_date.data  # This will be a datetime.date object    
            landing_page_url = request.form.get("landing_page_url")  
            utm_source = form.utm_source.data
            utm_medium = form.utm_medium.data 
            utm_campaign = form.utm_campaign.data 

            if not name or not channel_name or not profile:  
                flash("All fields are required to add a new influencer.", "danger")  
                return redirect(url_for("main.home", add_new="true"))  

            # Add the new influencer to the Influencer table  
            new_influencer = Influencer(  
                name=name,  
                channel_name=channel_name,  
                profile=profile  
            )  
            db.session.add(new_influencer)  
            db.session.flush()  # Flush to get the auto-generated unique_id  
            db.session.commit()

            # Generate UM String  
            um_string = generate_um_string(name, landing_page_url,utm_source,utm_medium,utm_campaign)  

            # Add the data to the IM_Tracker table  
            new_tracker = IM_Tracker(  
                influencer_name=name,  
                unique_id=new_influencer.unique_id,  # Use the auto-generated unique_id  
                channel_name=channel_name,  
                profile=profile,  
                activation_for=activation_for,  
                platform=platform,  
                tentative_live_date=tentative_live_date,  
                landing_page_url=landing_page_url, 
                utm_source = utm_source,
                utm_medium =  utm_medium,
                utm_campaign = utm_campaign, 
                utm_string=um_string  
            )  
            db.session.add(new_tracker)  
            db.session.commit()  

            flash("New influencer added and campaign created successfully!", "success")  
            return render_template("home.html", form=form, is_adding_new=is_adding_new, um_string=um_string)  

        else:  # Selecting an existing influencer  
            influencer_id = form.influencer_name.data  
            influencer = Influencer.query.get(influencer_id)  

            if not influencer:  
                flash("Please select a valid influencer.", "danger")  
                return redirect(url_for("main.home"))  

            # Collect other data from the form  
            activation_for = form.activation_for.data  
            platform = form.platform.data  
            tentative_live_date = form.tentative_live_date.data  
            landing_page_url = form.landing_page_url.data 
            utm_source = form.utm_source.data
            utm_medium = form.utm_medium.data 
            utm_campaign = form.utm_campaign.data 

            # Generate UM String  
            um_string = generate_um_string(influencer.name, landing_page_url,utm_source,utm_medium,utm_campaign)  

            # Add the data to the IM_Tracker table  
            new_tracker = IM_Tracker(  
                influencer_name=influencer.name,  
                unique_id=influencer.unique_id,  
                channel_name=influencer.channel_name,  
                profile=influencer.profile,  
                activation_for=activation_for,  
                platform=platform,  
                tentative_live_date=tentative_live_date,  
                landing_page_url=landing_page_url,  
                utm_source = utm_source,
                utm_medium =  utm_medium,
                utm_campaign = utm_campaign,
                utm_string=um_string  
            )  
            db.session.add(new_tracker)  
            db.session.commit()  

            flash("Campaign created successfully!", "success")  
            return render_template("home.html", form=form, is_adding_new=is_adding_new, um_string=um_string)  

    # Pre-fill the form for "Select Existing Influencer"  
    if not is_adding_new and form.influencer_name.data:  
        influencer = Influencer.query.get(form.influencer_name.data)  
        if influencer:  
            form.unique_id.data = influencer.unique_id  
            form.channel_name.data = influencer.channel_name  
            form.profile.data = influencer.profile  

    return render_template("home.html", form=form, is_adding_new=is_adding_new, um_string=um_string)  

@main.route("/get_influencer/<int:influencer_id>", methods=["GET"])  
def get_influencer(influencer_id):  
    """  
    Fetch influencer details by ID and return them as JSON.  
    """  
    influencer = Influencer.query.get(influencer_id)  
    if influencer:  
        return {  
            "unique_id": influencer.unique_id,  
            "channel_name": influencer.channel_name,  
            "profile": influencer.profile  
        }  
    return {"error": "Influencer not found"}, 404  