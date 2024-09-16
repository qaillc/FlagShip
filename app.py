import streamlit as st
import os
import requests
from openai import OpenAI
import time
from PIL import Image
import random 


# Initialize session state variables
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # Default to the first tab
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False  # Initialize simulation to be stopped


# Directory where patient text files are stored
patient_dir = './patients/'

@st.cache_data
def load_patient_files():
    return sorted([f for f in os.listdir(patient_dir) if f.startswith('patient') and f.endswith('.txt')])

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

# Full-screen layout
st.set_page_config(layout="wide")


def patient_file_viewer():
    st.title("Patient File Viewer")

    patient_files = load_patient_files()

    # Dropdown to select patient file
    selected_file = st.selectbox("Select a patient file", patient_files)

    # Display file content when a file is selected
    if selected_file:
        file_path = os.path.join(patient_dir, selected_file)
        data = read_file(file_path)
        st.text_area(f"Data from {selected_file}", data, height=300)

    # Optional: Add a search functionality
    search_term = st.text_input("Search in files (optional)")
    if search_term:
        st.subheader("Search Results")
        for file in patient_files:
            file_path = os.path.join(patient_dir, file)
            content = read_file(file_path)
            if search_term.lower() in content.lower():
                st.write(f"Found in {file}:")
                st.text(content[:200] + "..." if len(content) > 200 else content)




# Paths to icons (change paths if needed)
icon_dir = './icons/'  # Folder for icons (btr, sm, wrs)
patient_dir = './patients/'  # Folder for patient files

# Map possibilities to corresponding icon prefixes
icon_mapping = {
    "1": "btr",  # Possibility 1 -> btr icons
    "2": "sm",   # Possibility 2 -> sm icons
    "3": "wrs"   # Possibility 3 -> wrs icons
}

# Function to load icons based on possibility and month
def load_icon(possibility, month):
    icon_prefix = icon_mapping.get(possibility, "btr")
    icon_path = os.path.join(icon_dir, f'{icon_prefix}{str(month).zfill(2)}.png')
    return Image.open(icon_path)

# Function to parse patient data from text file
def parse_patient_data(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract the patient ID, possibility, and projection
    patient_id = content.split("Patient ID: ")[1].split("\n")[0].strip()
    possibility = content.split("Possibility: ")[1].split()[0].strip()
    projection = content.split("Projection: ")[1].split("\n")[0].strip()
    
    # Extract month data
    months_data = {}
    for i in range(1, 13):
        month_str = f"Month {i}"
        if month_str in content:
            month_data = content.split(month_str)[1].split("Month")[0]
            months_data[i] = month_data.strip()
    
    return patient_id, possibility, projection, months_data

# Load patient files from directory
def load_patient_files():
    return sorted([f for f in os.listdir(patient_dir) if f.startswith('patient') and f.endswith('.txt')])

# Function to display a patient case dynamically
def display_patient(patient_file, container):
    # Parse patient data
    file_path = os.path.join(patient_dir, patient_file)
    patient_id, possibility, projection, months_data = parse_patient_data(file_path)
    
    # Loop through months 1 to 12 every 5 seconds
    for month in range(1, 13):
        if not st.session_state.simulation_running:
            break  # Stop the simulation if the flag is False
        with container.container():  # Use the container to replace content dynamically
            # Create columns with specified widths (1/3 for icon, 2/3 for month data)
            cols = st.columns([1, 2])  # 1/3 width for icon, 2/3 for month data

            # Left column for icons (1/3 of the screen)
            with cols[0]:
                icon = load_icon(possibility, month)
                st.image(icon, use_column_width=False, width=150)  # Reduced the icon size

            # Right column for text data (2/3 of the screen)
            with cols[1]:
                # Display Patient_ID, Possibility, and Projection above month data
                st.subheader(f"Patient ID: {patient_id}")
                st.write(f"Possibility: {possibility}")
                st.write(f"Projection: {projection}")
                st.subheader(f'Month {month}')
                st.write(months_data.get(month, "No data available"))

        # Wait for 5 seconds before changing to the next month
        time.sleep(5)

# Main app loop
def main():
    # Load patient files
    patient_files = load_patient_files()

    # Create a single placeholder for displaying the patient data
    current_patient_container = st.empty()

    
    while st.session_state.simulation_running:
        # Randomly select a patient file
        selected_file = random.choice(patient_files)

        # Display the selected patient data for 12 months, replacing the previous patient
        display_patient(selected_file, current_patient_container)

        # After 12 months, the new patient data will replace the previous one
        current_patient_container.empty()  # Clears the current container before the next patient is displayed







# Title of the App
st.title('Flagship "Many Eyes" 30 Agent Propagation')

# Tabs for horizontal menu
tabs = st.tabs(["Introduction","MindsDB Diagnosis", "30 Agent Propagation", "Agent Counseling", "Strawberry Raw Data"])

# Control the tab state and animation
current_tab = 2  # This refers to "30 Agent Propagation"


# Optional: Add content for other tabs
with tabs[0]:

    if st.session_state.active_tab != current_tab:
        st.session_state.simulation_running = False

    # Set page title
    st.title("MindsDB Hackathon Submission")
    
    # Display your message
    st.write("Here's our MindsDB submission. The team was absolutely incredible. I am so impressed by the many talented people I have met during these Hackathons - Team Lead Mike Lively.")
    
    # Embed the video
    video_url = "https://www.youtube.com/watch?v=Xjj1SqIkBy0"
    st.video(video_url)

with tabs[1]:
    st.write("MindsDB Used to Propose Precision Treatment.")
    if st.session_state.active_tab != current_tab:
        st.session_state.simulation_running = False

    # Retrieve API keys and credentials from environment variables
    minds_api_key = os.getenv('MINDSDB_API_KEY')
    supabase_password = os.getenv('SUPABASE_PASSWORD')
    minds_name = 'precision_medicine_mind'  # Change if needed to avoid conflict
    
    # Check if environment variables are loaded correctly
    if not minds_api_key:
        st.error("MindsDB API key is missing. Please check your environment variables.")
    if not supabase_password:
        st.error("Supabase password is missing. Please check your environment variables.")
    
    # Headers for MindsDB API
    headers = {
        'Authorization': f'Bearer {minds_api_key}',
        'Content-Type': 'application/json'
    }
    
    # Configuration for Supabase PostgreSQL Database
    supabase_config = {
        "description": "Your Supabase Database",
        "type": "postgres",
        "connection_args": {
            "user": "postgres.mgvepfrmsojwkoudycez",
            "password": supabase_password,
            "host": "aws-0-ap-southeast-1.pooler.supabase.com",
            "port": "6543",
            "database": "postgres"
        },
        "tables": ["Precision_medicine"]  # Replace with your table name
    }

    # Payload for creating a Mind
    payload = {
        "name": minds_name,
        "data_source_configs": [supabase_config]
    }
    
    # Function to create a Mind using a POST request
    try:
        #st.write("Sending POST request to create the Mind...")
    
        response = requests.post(
            url='https://llm.mdb.ai/minds',
            json=payload,
            headers=headers
        )
        
        # Check if the response was successful
        if response.status_code == 201:
            st.success(f"Mind '{minds_name}' created successfully!")
            st.write(response.json())
        else:
            #st.error(f"Error creating Mind: {response.status_code} - {response.text}")
            st.success("Mind already exists")
    
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    # Configuration for OpenAI
    openai_client = OpenAI(
        api_key=minds_api_key,
        base_url='https://llm.mdb.ai/'
    )
    
    # Streamlit app
    st.title("Precision Medicine with MindsDB")

    # Patient number input
    patient_number = st.text_input("Enter patient number (1 to 30) for precision care analysis:")
    
    # Query the Mind if button is pressed
    if st.button('Get Recommendations'):
        if patient_number:
            try:
                # Prepare payload for querying the Mind
                query_payload = {
                    "model": minds_name,
                    "messages": [
                        {"role": "user", "content": f"Analyze precision care recommendations for patient number: {patient_number}"}
                    ]
                }
    
                # Send the query request
                query_response = requests.post(
                    url='https://llm.mdb.ai/chat/completions',
                    json=query_payload,
                    headers=headers
                )
    
                if query_response.status_code == 200:
                    completion = query_response.json()
                    st.write("Recommendation:", completion['choices'][0]['message']['content'])
                else:
                    st.error(f"Error querying the Mind: {query_response.status_code} - {query_response.text}")
    
            except Exception as e:
                st.error(f"Error querying the Mind: {e}")
        else:
            st.error("Please enter a patient number.")

    st.write("""
    Example Patient 30
    Recommendation: The data for patient number 30 (Patient_ID: P030) is as follows:

Age: 69
Gender: Male
Disease Type: Alzheimer’s
Stage: Severe
Age of Onset: 60
APOE4 Status: 0
LRRK2 Status: N/A
Cognitive Score: 13
Motor Score: N/A
Smoking History: No
Physical Activity: Moderate
Sleep Patterns: Normal
Family History: Yes
Comorbidities: Diabetes
Treatment: Donepezil
Treatment Response: Stabilized
Side Effects: Fatigue
Analysis of Precision Care Recommendations:
Disease Management:

The patient is diagnosed with severe Alzheimer’s disease, which requires comprehensive management strategies.
The treatment with Donepezil has resulted in a stabilized condition, indicating a positive response to the medication.
Comorbidities:

The patient has diabetes, which needs to be managed alongside Alzheimer’s. Coordination between neurologists and endocrinologists is essential.
Lifestyle Factors:

The patient has a moderate level of physical activity and normal sleep patterns, which are beneficial for overall health and cognitive function.
No smoking history, which is positive as smoking can exacerbate cognitive decline.

Family History: A positive family history of Alzheimer’s suggests a genetic predisposition, which may be relevant for family counseling and genetic testing.
Side Effects:

The patient experiences fatigue as a side effect of Donepezil. Monitoring and managing this side effect is important to maintain the patient’s quality of life.

Recommendations:

Continued Monitoring: Regular follow-ups to monitor the progression of Alzheimer’s and adjust treatment as necessary.
Monitoring blood glucose levels and managing diabetes effectively.
Supportive Therapies:

Cognitive rehabilitation and memory exercises to support cognitive function.
Physical therapy to maintain mobility and physical health.
Side Effect Management:

Addressing fatigue through lifestyle modifications, such as ensuring adequate rest and possibly adjusting medication timing.
Family Support:

Providing support and education to the patient’s family about Alzheimer’s disease and its management.
Genetic counseling for family members if they are concerned about their risk.
Holistic Approach:

A multidisciplinary approach involving neurologists, endocrinologists, physical therapists, and mental health professionals to provide comprehensive care.
By following these recommendations, the patient can receive personalized and effective care tailored to their specific needs and conditions.
    
    
    
    """)


    
with tabs[2]:
    st.write("")


    # Set active tab to 2 if on this tab
    st.session_state.active_tab = 2

    # Start the animation if Tab 2 is active
    if st.session_state.active_tab == 2:
        st.session_state.simulation_running = True
    else:
        st.session_state.simulation_running = False

    # Run the main app loop if simulation is running
    if st.session_state.simulation_running:
        main()
    

    
# Put the present application in the "Strawberry Raw Data" tab
with tabs[3]:
    st.write("Content for Agent Counseling goes here.")
    if st.session_state.active_tab != current_tab:
        st.session_state.simulation_running = False


# Put the present application in the "Strawberry Raw Data" tab
with tabs[4]:
    # Initialize the session state if it doesn't exist
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = True


    patient_file_viewer()
