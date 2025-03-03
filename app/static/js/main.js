document.addEventListener("DOMContentLoaded", () => {
    const influencerDropdown = document.getElementById("influencer-name");
    const newInfluencerInput = document.getElementById("new-influencer");
    
    influencerDropdown.addEventListener("change", () => {
        if (influencerDropdown.value === "new") {
            newInfluencerInput.style.display = "block";
        } else {
            newInfluencerInput.style.display = "none";
        }
    });

    document.getElementById("influencer-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = {
            influencer_name: influencerDropdown.value === "new" ? newInfluencerInput.value : influencerDropdown.value,
            is_new: influencerDropdown.value === "new",
            channel_name: document.getElementById("channel-name").value,
            influencer_profile: document.getElementById("influencer-profile").value,
            activation_for: document.getElementById("activation-for").value,
            platform: document.getElementById("platform").value,
            tentative_live_date: document.getElementById("tentative-live-date").value,
            landing_page_url: document.getElementById("landing-page-url").value
        };
        const response = await fetch("/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        document.getElementById("utm-string").textContent = result.utm_string;
    });
});