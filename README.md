# 📊 CPT Analysis Report Generator

A comprehensive Streamlit web application that generates professional PDF reports from CPT (Current Procedural Terminology) healthcare data with interactive preview functionality.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 📋 **Interactive Preview**
- **👀 Preview Before Download** - See exactly what your report will contain
- **📊 Interactive Charts** - Same charts as PDF but viewable in browser
- **📈 Live Statistics** - Key metrics displayed clearly
- **✅ Quality Control** - Review and approve before generating PDF

### 📊 **Comprehensive Analysis**
- **�� Rate Analysis** - Statistical analysis with percentiles and distribution charts
- **🏥 Billing Class Analysis** - Breakdown by service types with rate comparisons
- **📋 Contract Type Analysis** - Payment method distributions
- **🌍 Geographic Distribution** - Complete city-by-city analysis with rate comparisons
- **📈 Professional Charts** - Clean, publication-ready visualizations

### 🎯 **User-Friendly Design**
- **Clean Interface** - Easy-to-understand charts and explanations
- **Professional PDFs** - Publication-ready reports
- **Sample Data Included** - Test with provided sample dataset
- **Responsive Design** - Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- macOS, Linux, or Windows

### Installation

#### macOS (Recommended)
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/cpt-analysis-report-generator.git
cd cpt-analysis-report-generator

# One-command setup (creates virtual environment and installs dependencies)
python3 setup_mac.py
```

#### Manual Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/cpt-analysis-report-generator.git
cd cpt-analysis-report-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app_improved.py
```

### Usage

1. **Start the application**
   ```bash
   ./venv/bin/python -m streamlit run app_improved.py --server.port 8503
   ```

2. **Open your browser** to `http://localhost:8503`

3. **Upload your CSV file** or use the included sample data

4. **Click "👀 Preview Report"** to see an interactive preview

5. **Click "📥 Download PDF Report"** to get your professional PDF

## 📁 File Structure

```
cpt-analysis-report-generator/
├── app_improved.py          # Main Streamlit application with preview
├── requirements.txt         # Python dependencies
├── setup_mac.py            # macOS setup script
├── sample_data.csv          # Sample CPT data for testing
├── README.md               # This file
├── run.py                  # Simple run script
└── .gitignore             # Git ignore rules
```

## 📊 Expected CSV Format

Your CSV file should contain these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `billing_code` | CPT codes | "27130" |
| `negotiated_rate` | Numeric rates | 1500.00 |
| `billing_class` | Service type | "Outpatient" |
| `negotiated_type` | Contract type | "Fee Schedule" |
| `city` | Provider location | "New York" |
| `taxonomy_classification` | Provider specialty | "Orthopedic Surgery" |

### Sample Data
```csv
billing_code,negotiated_rate,billing_class,negotiated_type,city,taxonomy_classification
27130,1500.00,Outpatient,Fee Schedule,New York,Orthopedic Surgery
27130,1200.00,Inpatient,Bundled Payment,Los Angeles,Orthopedic Surgery
```

## 📈 Generated Report Contents

The PDF report includes:

- ✅ **Rate Analysis** - Statistics, percentiles, distribution chart
- ✅ **Billing Class Analysis** - Service type breakdown and rate comparisons  
- ✅ **Contract Type Analysis** - Payment method distributions
- ✅ **Geographic Distribution** - Complete city-by-city analysis with average rates
- ✅ **Professional Formatting** - Clean, publication-ready design

## 🛠️ Technical Details

### Built With
- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Pandas](https://pandas.pydata.org/)** - Data analysis and manipulation
- **[Matplotlib](https://matplotlib.org/)** - Data visualization
- **[Seaborn](https://seaborn.pydata.org/)** - Statistical data visualization
- **[ReportLab](https://www.reportlab.com/)** - PDF generation

### Key Features
- Interactive web interface with preview functionality
- Professional PDF generation with charts and tables
- Responsive design that works on all devices
- Comprehensive data analysis and visualization
- User-friendly explanations for non-technical users

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/YOUR_USERNAME/cpt-analysis-report-generator/issues) page
2. Create a new issue with detailed information
3. Include sample data and error messages if applicable

## 📸 Screenshots

### Interactive Preview
*Preview your report before downloading with interactive charts and statistics*

### Professional PDF Output  
*Clean, publication-ready PDF reports with comprehensive analysis*

---

⭐ **If you find this project helpful, please give it a star!** ⭐
