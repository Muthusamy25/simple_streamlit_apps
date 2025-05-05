import phonenumbers
from phonenumbers import geocoder, carrier
import folium
from opencage.geocoder import OpenCageGeocode
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

# App Title
st.title("📱 Mobile Number Tracker")

# Phone number input
number = st.text_input("Enter the phone number with country code (e.g., +14155552671)")

if number:
    try:
        # Parse the phone number
        phoneNumber = phonenumbers.parse(number)

        # Validate the phone number
        if not phonenumbers.is_valid_number(phoneNumber):
            st.error("Invalid phone number. Please check the input.")
        else:
            # Get location and carrier
            yourLocation = geocoder.description_for_number(phoneNumber, "en")
            yourServiceProvider = carrier.name_for_number(phoneNumber, "en")

            st.success(f"📍 Location: {yourLocation}")
            st.info(f"📡 Service Provider: {yourServiceProvider}")

            # OpenCage API
            key = "87e07a01f5024c6da75c04b5779f9afc"  # Replace with your key if needed
            geocoder_api = OpenCageGeocode(key)
            results = geocoder_api.geocode(yourLocation)

            if results:
                lat = results[0]['geometry']['lat']
                lng = results[0]['geometry']['lng']

                st.map(pd.DataFrame([[lat, lng]], columns=['lat', 'lon']))  # Quick map

                # Interactive map with marker using folium
                myMap = folium.Map(location=[lat, lng], zoom_start=9)
                folium.Marker([lat, lng], popup=yourLocation).add_to(myMap)

                # Show the folium map inside Streamlit
                st_folium(myMap, width=700, height=500)
            else:
                st.error("❌ Could not geocode the location.")

    except phonenumbers.phonenumberutil.NumberParseException:
        st.error("⚠️ Unable to parse phone number. Make sure it starts with + and country code.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
