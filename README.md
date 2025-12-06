# Toronto Bike-Sharing Analytics Tool  
**Final Group Project **

Team Members: 
**Kelly Bolanos
  Sebastian Gonzalez
  Angee Morales
  Eduardo Leiva**

This project delivers an end-to-end analytics solution for the Toronto Bike-Sharing dataset, including:  
• Data loading & cleaning  
• Exploratory analytics  
• Testing using TDD  
• Streamlit dashboard  
• Deployment-ready folder structure  
• Work completed in two Agile sprints  

---

## Project Structure

```text
**toronto_bikeshare/**
├─ **data/**
│  ├─ financial_transactions_toronto_bike.csv   # The provided dataset (put it here)
│  └─ stations_coordinates.csv                  # OPTIONAL: station_id, name, lat, lon (for map)
├─ **src/**
│  ├─ __init__.py
│  ├─ data_loading.py
│  ├─ data_cleaning.py
│  ├─ analytics.py
│  ├─ plots.py
│  └─ dashboard_app.py                       
├─ **tests/**
│  ├─ test_data_loading.py
│  ├─ test_analytics.py
│  └─ test_end_to_end.py              
├─ **notebooks/**
│  └─ EDA_and_Demo.ipynb                        # created in Jupyter/Colab, not versioned here
├─ **.gitignore**
├─ **requirements.txt**
└─ **README.md**
```

## Run in Google Colab

1. Create a new Colab notebook.
2. Clone the repository:
     !git clone https://github.com/<your-repo-name>.git
      %cd <your-repo-name>
3. Install dependencies:
   !pip install -r requirements.txt
4. Open and run notebooks/eda.ipynb.




   


