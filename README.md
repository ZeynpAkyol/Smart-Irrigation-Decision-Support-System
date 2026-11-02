🌾 Smart Irrigation Decision Support System

This project is a Streamlit-based Decision Support System that combines Machine Learning and live weather data (via the OpenWeatherMap API) to calculate optimal water usage for agricultural lands, provide cost-efficiency analytics, and maintain an irrigation history log in a local database.

🚀 Key Features

🤖 AI-Powered Predictions: Utilizes a RandomForestRegressor model to estimate water requirements per square meter based on soil moisture, ambient temperature, sunlight/cloud cover, and crop type.

🌍 Live Weather Integration: Automatically fetches real-time temperature and cloudiness data for a selected city via the OpenWeatherMap API to compute light conditions dynamically.

💰 Financial & Operational Analytics: Calculates total water requirements based on field size (in Dunams/Hectares), estimates water savings compared to traditional methods (assuming a ~40% efficiency gain), and provides operational cost predictions as well as 120-day seasonal savings forecasts.

💾 Database History Log: Integrated with SQLite to automatically persist all irrigation calculations with timestamps, crop types, and environmental parameters. Logs can be reviewed or cleared directly from the app interface.

🛠️ Tech Stack

UI Framework: Streamlit

Machine Learning: Scikit-Learn (RandomForestRegressor), NumPy

Data Processing: Pandas

Database: SQLite3

API Integration: OpenWeatherMap API (requests)

📁 Project Structure

├── app.py                   # Main Streamlit application code
├── veri_uretici.py            # Synthetic dataset generator script
├── bitki_verisi.csv         # Crop and irrigation dataset (Generated automatically)
├── sulama_gecmisi.db        # SQLite database for irrigation history (Generated automatically)
└── README.md                # Project documentation


⚙️ Installation & Usage

1. Install Dependencies

Install all required Python libraries using pip:

pip install streamlit pandas numpy scikit-learn requests


2. Generate the Dataset

Before launching the app, run the dataset generator script once to create the bitki_verisi.csv file required for model training:

python veri_uretici.py


3. Run the Application

Once the CSV file is generated, launch the Streamlit app with:

streamlit run app.py


Note: The SQLite database file (sulama_gecmisi.db) will be created automatically upon the first run.

🌿 Supported Crop Types

The system features tailored water usage coefficients for 10 different crops:

Tomato, Pepper, Strawberry, Lavender, Cactus

Corn, Sunflower, Rose, Orchid, Olive Tree

📝 License

This project is open-source and intended for educational and developmental purposes.
