# CPT Analysis Report Generator

A Streamlit web application that generates comprehensive PDF reports from CPT (Current Procedural Terminology) healthcare data.

## Features

- **Rate Analysis**: Statistical analysis with percentiles and distribution charts
- **Billing Class Analysis**: Breakdown by billing categories 
- **Negotiated Type Analysis**: Contract type distributions
- **Complete Geographic Distribution**: Analysis of all cities with providers
- **Taxonomy Analysis**: Provider specialty classifications
- **PDF Export**: Professional PDF reports with charts and tables

## Quick Start

### For macOS Users (Recommended):
```bash
python3 setup_mac.py
```
This automatically creates a virtual environment, installs dependencies, and starts the app.

### For Manual Setup:

#### 1. Install Python
Make sure you have Python 3.8 or higher installed on your system.

#### 2. Create Virtual Environment (macOS/Linux)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the Application
```bash
streamlit run app.py
```

This will start the web application and automatically open it in your browser at `http://localhost:8501`

### Running After Initial Setup:
Once you've run the setup script once, you can start the app again anytime with:
```bash
python3 run.py
```

## Usage

### Option 1: Upload CSV File
1. Click "Browse files" and select your cleaned CPT CSV file
2. Preview your data to ensure it loaded correctly
3. Click "Generate Custom Report" to create the PDF

### Option 2: Use Existing File
1. Check the box "Use existing file: cpt_27130_EMPLOYER_360-orthopedics_cleaned.csv"
2. Click "Generate Report from Existing File"
3. Download the generated PDF report

## Expected CSV Format

Your CSV file should contain the following columns:

- `billing_code`: CPT codes (e.g., "27130")
- `negotiated_rate`: Numeric rates 
- `billing_class`: Billing classifications
- `negotiated_type`: Contract types
- `city`: Provider cities
- `taxonomy_classification`: Provider specialties

### Sample CSV Structure:
```csv
billing_code,negotiated_rate,billing_class,negotiated_type,city,taxonomy_classification
27130,1500.00,Outpatient,Fee Schedule,New York,Orthopedic Surgery
27130,1200.00,Inpatient,Bundled Payment,Los Angeles,Orthopedic Surgery
```

## Troubleshooting

### Common Issues:

1. **Module not found errors**: 
   - Run `pip install -r requirements.txt` again
   - Make sure you're in the correct directory

2. **Port already in use**:
   - Run `streamlit run app.py --server.port 8502` to use a different port

3. **CSV file errors**:
   - Ensure your CSV has the expected column names
   - Check that numeric columns contain valid numbers

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify your CSV file format matches the expected structure
3. Try using a different browser if the web interface doesn't load

## Generated Report Contents

The PDF report includes:
- ✅ Rate Analysis - Statistics, percentiles, distribution chart
- ✅ Billing Class Analysis - Breakdown and rate comparisons
- ✅ Negotiated Type Analysis - Contract type distributions  
- ✅ Complete Geographic Distribution - ALL cities with providers
- ✅ Taxonomy Analysis - Provider specialties and classifications

## Requirements

- Python 3.8+
- All packages listed in `requirements.txt`
- Web browser for accessing the Streamlit interface 