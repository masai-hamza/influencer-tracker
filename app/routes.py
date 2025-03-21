from flask import Blueprint, render_template, request, redirect, url_for, flash  
from app import db  
from app.models import Influencer, IM_Tracker  
from app.forms import InfluencerForm, UpdateLiveDateForm
import uuid  
from datetime import datetime
from sqlalchemy import text
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

    # Fetch cohort_name and cohort_id from the Onwards DB  
    onwards_cohorts = []  
    engine = db.get_engine(bind="onwards")  
    with engine.connect() as connection:  # Use a connection object  
        result = connection.execute(text("""SELECT
  `cohorts`.`name` AS `name`,
  `cohorts`.`id` AS `cohort_id`
FROM
  `cohorts`
WHERE
  (`cohorts`.`track_id` NOT IN (1, 2, 3, 4, 5, 6, 8, 9, 11, 13, 23, 24, 43, 49, 74))
  AND 
  (`cohorts`.`name` NOT IN (
      'iit-guwahati ai-ml', 
      'IIM Sirmaur', 
      'iim-mumbai', 
      'iim sirmaur digital marketing ', 
      'IIM Mumbai', 
      'Minor in Artificial Intelligence & Data Science'
  ))
GROUP BY
  `cohorts`.`name`, `cohorts`.`id`
ORDER BY
  `cohorts`.`name` ASC, `cohorts`.`id` ASC;
"""))
    onwards_cohorts = result.fetchall()   
    # Populate the dropdown with cohort_name options and store cohort_id as values  
    # form.course.choices = [(str(c[1]), c[0]) for c in onwards_cohorts]
    form.course.choices = [(c[0], c[0]) for c in onwards_cohorts]  # Use cohort `name` as the value and label    

    if request.method == "POST":  
        if is_adding_new:  # Adding a new influencer  
            # Collect data from the form  
            name = request.form.get("influencer_name")
            channel_name = form.channel_name.data 
            # channel_name = request.form.get("channel_name")  
            profile = request.form.get("profile")   
            print(f"Collected data: Name={name}, Channel={channel_name}, Profile={profile}")
            # activation_for = request.form.get("activation_for")
            course = form.course.data  
            # platform = request.form.get("platform")
            platform = form.platform.data
            tentative_live_date = form.tentative_live_date.data  # This will be a datetime.date object    
            landing_page_url = request.form.get("landing_page_url")  
            utm_source = form.utm_source.data
            utm_medium = form.utm_medium.data 
            utm_campaign = form.utm_campaign.data
            cost = form.cost.data
            print("Fetching cohort_id for the selected course...")  # Debug 
            # Fetch cohort_name using cohort_id  
            engine = db.get_engine(bind="onwards") 
            print(f"Course selected from form: {course}")  
            with engine.connect() as connection:  
                selected_cohort = connection.execute(
                text("SELECT id as cohort_id FROM cohorts WHERE name = :id"),  
                {"id": course} 
            ).fetchone()  
            print(f"Selected Cohort: {selected_cohort}")  # Debug 
            course_id = selected_cohort[0] if selected_cohort else None 
            if not course_id:
                print("Invalid course selection!")  # Debug
                flash("Invalid course selection. Please select a valid course.", "danger")  
                return redirect(url_for("main.home")) 
            if not name or not channel_name or not profile:  
                flash("All fields are required to add a new influencer.", "danger")  
                return redirect(url_for("main.home", add_new="true"))  
            # Add the new influencer  
            print("Inserting new influencer...")  # Debug 
            try:  
                # Add the new influencer to the Influencer table  
                new_influencer = Influencer(  
                    name=name,  
                    created_at=datetime.now()  
                )  
                db.session.add(new_influencer)  
                db.session.flush()  # Flush to get the auto-generated unique_id  
                db.session.commit()  # Attempt to save the new data
                print(f"Generated Influencer ID: {new_influencer.unique_id}")  # Debug   
            except Exception as e:  
                db.session.rollback()  # Roll back the transaction if something goes wrong  
                print(f"Error while adding influencer: {e}")  # Log the error for debugging  
                flash("An error occurred while adding the influencer.", "danger")  
                return redirect(url_for("main.home", add_new="true"))  
            # Add the data to the IM_Tracker table  
            print("Adding data to IM_Tracker...")  # Debug
            # Generate UM String  
            um_string = generate_um_string(name, landing_page_url,utm_source,utm_medium,utm_campaign)  

            # Add the data to the IM_Tracker table  
            try:  
                # Add the data to the IM_Tracker table  
                new_tracker = IM_Tracker(  
                    influencer_name=name,  
                    unique_id=new_influencer.unique_id,  # Use the auto-generated unique_id  
                    channel_name=channel_name,  
                    profile=profile,  
                    course=course,   
                    cohort_id=course_id,   
                    platform=platform,  
                    tentative_live_date=tentative_live_date,  
                    landing_page_url=landing_page_url,   
                    cost=cost,  
                    utm_source=utm_source,  
                    utm_medium=utm_medium,  
                    utm_campaign=utm_campaign,   
                    utm_string=um_string,  
                    created_at=datetime.now()  
                )  
                db.session.add(new_tracker)  
                db.session.commit() 
                print("Data committed to the database successfully!")  # Debug  
            except Exception as e:  
                db.session.rollback()  # Rollback if something goes wrong  
                print(f"Error while adding tracker entry: {e}")  # Log the error  
                flash("An error occurred while creating the campaign.", "danger")  
                return redirect(url_for("main.home"))  

            flash("New influencer added and campaign created successfully!", "success")  
            return render_template("home.html", form=form, is_adding_new=is_adding_new, um_string=um_string)  

        else:  # Selecting an existing influencer  
            influencer_id = form.influencer_name.data  
            influencer = Influencer.query.get(influencer_id)  

            if not influencer:  
                flash("Please select a valid influencer.", "danger")  
                return redirect(url_for("main.home"))  

            # Collect other data from the form
            channel_name=form.channel_name.data  
            profile=form.profile.data
            activation_for = form.activation_for.data  
            platform = form.platform.data  
            tentative_live_date = form.tentative_live_date.data  
            landing_page_url = form.landing_page_url.data 
            utm_source = form.utm_source.data
            utm_medium = form.utm_medium.data 
            utm_campaign = form.utm_campaign.data
            cost = form.cost.data
            # Generate UM String  
            um_string = generate_um_string(influencer.name, landing_page_url,utm_source,utm_medium,utm_campaign)  

            # Add the data to the IM_Tracker table  
            new_tracker = IM_Tracker(  
                influencer_name=influencer.name,  
                unique_id=influencer.unique_id,  
                channel_name=channel_name,  
                profile=profile,  
                activation_for=activation_for,  
                platform=platform,  
                tentative_live_date=tentative_live_date,  
                landing_page_url=landing_page_url,  
                utm_source = utm_source,
                utm_medium =  utm_medium,
                utm_campaign = utm_campaign,
                utm_string=um_string,
                cost = cost,
                created_at=datetime.now()
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
            # form.channel_name.data = influencer.channel_name  
            # form.profile.data = influencer.profile  

    return render_template("home.html", form=form, is_adding_new=is_adding_new, um_string=um_string)  

@main.route("/get_influencer/<int:influencer_id>", methods=["GET"])  
def get_influencer(influencer_id):  
    """  
    Fetch influencer details by ID and return them as JSON.  
    """  
    influencer = Influencer.query.get(influencer_id)  
    if influencer:  
        return {  
            "unique_id": influencer.unique_id
            # "channel_name": influencer.channel_name,  
            # "profile": influencer.profile  
        }  
    return {"error": "Influencer not found"}, 404 


@main.route("/update_live_date", methods=["GET", "POST"])  
def update_live_date():  
    form = UpdateLiveDateForm()  
    # Populate the influencer dropdown  
    form.influencer_name.choices = [(i.unique_id, i.name) for i in Influencer.query.all()]  

    if request.method == "POST":  
        influencer_id = form.influencer_name.data  
        new_date = form.new_date.data  
        live_date = form.live_date.data  

        # Update the live date in the IM_Tracker table  
        tracker = IM_Tracker.query.filter_by(unique_id=influencer_id, tentative_live_date=live_date).first()  
        if tracker:  
            tracker.tentative_live_date = new_date  
            tracker.updated_at = datetime.now()  
            db.session.commit()  
            flash("Tentative live date updated successfully!", "success")  
        else:  
            flash("No matching record found.", "danger")  
        return redirect(url_for("main.update_live_date"))  

    return render_template("update_live_date.html", form=form)

@main.route("/get_live_dates/<int:influencer_id>", methods=["GET"])  
def get_live_dates(influencer_id):  
    """  
    Fetch tentative live dates for the given influencer where tentative_live_date >= today().  
    """  
    today = datetime.utcnow().date()  
    live_dates = IM_Tracker.query.filter(  
        IM_Tracker.unique_id == influencer_id,  
        IM_Tracker.tentative_live_date >= today  
    ).all()  

    # Return the live dates as a list of strings  
    return {"live_dates": [str(ld.tentative_live_date) for ld in live_dates]}  