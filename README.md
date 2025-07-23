HEAD

# E-Commerce AI Data Analysis Tool

An AI-powered data analysis platform that converts natural language questions into SQL queries and provides business insights with visualizations.

## Features

- 🤖 Natural language to SQL query conversion using Google Gemini AI
- 📊 Automatic chart generation and downloadable visualizations
- 💡 AI-generated business insights and recommendations
- 🗄️ SQLite database with your real e-commerce data
- 📈 Support for ad sales, total sales, and product eligibility analysis

## Setup Instructions for Visual Studio Code

### Prerequisites

- Python 3.11 or higher
- Visual Studio Code
- Git (optional)

### 1. Clone or Download the Project

```bash
# If using Git
git clone <your-repo-url>
cd <project-folder>

# Or download and extract the project files
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install required packages
pip install streamlit pandas plotly google-genai openpyxl numpy
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Get your free Gemini API key from: https://aistudio.google.com/apikey

### 5. Load Your Data

```bash
# Load the attached Excel files into database
python load_attached_data.py
```

### 6. Run the Application

```bash
# Start the Streamlit app
streamlit run app.py --server.port 5000
```

### 7. Access the Application

Open your browser and go to: `http://localhost:5000`

## Usage

1. **Login**: Use any username/password to access the dashboard
2. **Data Management**: Your real Excel data is automatically loaded
3. **Query Interface**: Ask questions in natural language like:
   - "What is my total sales?"
   - "Calculate the RoAS (Return on Ad Spend)"
   - "Which product had the highest CPC?"
4. **View Results**: Get SQL queries, data tables, charts, and business insights
5. **Download**: Save charts as HTML files

## Project Structure

```
├── app.py                     # Main Streamlit application
├── services/                  # Core business logic
│   ├── ai_service.py         # Gemini AI integration
│   ├── database_service.py   # SQLite database operations
│   ├── data_loader.py        # Excel file processing
│   └── visualization_service.py # Chart generation
├── utils/                     # Utilities
│   └── sample_data_generator.py
├── attached_assets/           # Your Excel data files
├── .streamlit/               # Streamlit configuration
└── load_attached_data.py     # Data loading script
```

## Troubleshooting

### Common Issues:

1. **Import Error**: Make sure virtual environment is activated
2. **API Key Error**: Verify GEMINI_API_KEY is set correctly
3. **Port Already in Use**: Change port number in streamlit command
4. **Data Not Loading**: Run `python load_attached_data.py` first

### VS Code Setup:

1. **Python Interpreter**: Press `Ctrl+Shift+P` → "Python: Select Interpreter" → Choose your venv
2. **Terminal**: Use VS Code integrated terminal (`Ctrl+``)
3. **Extensions**: Install Python and Streamlit extensions for better support

## Commands Quick Reference

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install streamlit pandas plotly google-genai openpyxl numpy

# Load data
python load_attached_data.py

# Run app
streamlit run app.py --server.port 5000
```

## Data Schema

Your loaded data includes:

- **ad_sales_metrics**: 3,696 records with ad performance data
- **total_sales_metrics**: 702 records with sales performance
- **eligibility_table**: 4,381 records with product eligibility info

## Support

# For issues or questions, check the application logs in your terminal or VS Code output panel.

# vigneshwarii

35ae3ef41e55eac18f00175bec2b13f82420b00a
