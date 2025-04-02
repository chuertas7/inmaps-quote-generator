import streamlit as st

# Page configuration
st.set_page_config(page_title="InMaps Quote Generator", layout="centered")
st.title("InMaps Quote Request Form")

st.write("Please enter the event details below to receive a custom quote for our indoor navigation services.")

# SECTION: User Input
st.header("Client and Event Information")

# Inputs
events_per_year = st.number_input("Expected Number of Events per Year", min_value=1, step=1)
venue_size = st.number_input("Average Venue Size (m²)", min_value=1000, step=100)
attendees = st.number_input("Average Number of Attendees", min_value=100, step=50)

st.header("Features and Customizations")
features_selected = st.multiselect(
    "Select Desired Features",
    ["navigation", "analytics", "engagement"]
)
customizations = st.multiselect(
    "Select Customization Options",
    ["branding", "api_integration", "beacon_repositioning"]
)
support_level = st.radio("Select Support Level", ["standard", "premium"])
contract_years = st.slider("Select Contract Length (Years)", 1, 3, 1)


# QUOTE CALCULATION FUNCTION
def generate_inmaps_quote(inputs):
    hardware_cost_per_beacon = 39
    beacon_markup = 1
    beacons_per_m2 = 1 / 259.8  # 1 beacon per 259.8 meters squared
    installation_cost_per_event = 2000
    support_costs = {"standard": 1000, "premium": 3000}
    customization_costs = {
        "branding": 5000,
        "api_integration": 4000,
        "beacon_repositioning": 2000
    }
    feature_costs = {
        "navigation": 2000,
        "analytics": 3500,
        "engagement": 4500
    }
    profit_margin = 1.4  # 40%

    events = inputs["expected_events_per_year"]
    venue_size = inputs["avg_venue_size_m2"]
    features = inputs["features_selected"]
    customizations = inputs["customizations"]
    support = inputs["support_expectation"]
    contract_years = inputs["contract_length_years"]

    avg_beacons = venue_size * beacons_per_m2
    total_beacons = avg_beacons * events
    hardware_cost = total_beacons * hardware_cost_per_beacon * beacon_markup
    installation_cost = installation_cost_per_event * events
    software_cost = sum(feature_costs.get(f, 0) for f in features)
    customization_cost = sum(customization_costs.get(c, 0) for c in customizations)
    support_cost = support_costs.get(support, 0)

    total_internal_cost = (
        hardware_cost + installation_cost + software_cost + customization_cost + support_cost
    )
    final_price = total_internal_cost * profit_margin

    return {
        "annual_quote": round(final_price / contract_years),
        "monthly_quote": round(final_price / contract_years / 12, 2),
        "cost_estimate": round(total_internal_cost),
        "breakdown": {
            "hardware": round(hardware_cost),
            "installation": round(installation_cost),
            "software": round(software_cost),
            "customization": round(customization_cost),
            "support": round(support_cost),
        }
    }

if st.button("Generate Quote"):
    user_inputs = {
        "expected_events_per_year": events_per_year,
        "avg_venue_size_m2": venue_size,
        "avg_attendees": attendees,
        "features_selected": features_selected,
        "customizations": customizations,
        "support_expectation": support_level,
        "contract_length_years": contract_years
    }

    result = generate_inmaps_quote(user_inputs)

    st.subheader("Quote Summary")
    st.write(f"**Annual Quote:** ${result['annual_quote']}")
    st.write(f"**Monthly Equivalent:** ${result['monthly_quote']}")
    st.write("---")

    st.subheader("Cost Breakdown")
    for item, value in result["breakdown"].items():
        st.write(f"{item.capitalize()} Cost: ${value}")

    st.caption("This quote includes a 40% profit margin.")

