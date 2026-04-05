# GIX Purchase Request Tracker

A Streamlit web app built for TECHIN 510 Week 1 that helps GIX students 
submit purchase requests and helps coordinator Dorothy track and manage 
orders — replacing the current Google Form + Excel workflow.

## Features

- Students can submit purchase requests with item details, supplier, price, and product link
- Coordinator can view all requests in a filterable, searchable table
- Real-time search across student name, item name, and class name
- Filter by supplier (Amazon / non-Amazon) and instructor approval status
- Coordinator can update fulfillment status (Pending / Ordered / Delivered / Back-ordered / Returned)
- Summary metrics: total requests, total estimated cost, pending fulfillments

## How to Run

### Prerequisites
- Python 3.11+
- Git

### Steps

1. Clone the repository
   git clone https://github.com/Xin-414/TECHIN510_Lab1.git
   cd TECHIN510_Lab1

2. Create and activate a virtual environment

   Windows:
   python -m venv .venv
   .venv\Scripts\activate

   macOS/Linux:
   python3 -m venv .venv
   source .venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Run the app
   streamlit run app.py

5. Open your browser at http://localhost:8501

## Project Structure

techin510-week1/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
├── .gitignore        # Files excluded from Git
├── README.md         # This file
└── requests.csv      # Auto-generated when first request is submitted

## Developer

- Name: Xin Luo
- Course: TECHIN 510 · University of Washington Global Innovation Exchange (GIX)