# Windows Setup Fix for Virtual Environment Error

## The Error:
```
Unable to copy 'C:\\Users\\kalai\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\venv\\scripts\\nt\\venvlauncher.exe' to 'C:\\Users\\kalai\\Downloads\\DataInsightHub\\DataInsightHub\\venv\\Scripts\\python.exe'
```

## Solutions (Try in order):

### Solution 1: Run as Administrator
1. Close VS Code
2. Right-click on VS Code icon
3. Select "Run as administrator"
4. Open your project folder
5. Try the commands again

### Solution 2: Delete existing venv folder and retry
```cmd
rmdir /s venv
python -m venv venv
```

### Solution 3: Use different folder location
```cmd
# Create venv in a different location (like C:\temp)
python -m venv C:\temp\myproject_venv

# Activate it
C:\temp\myproject_venv\Scripts\activate

# Then continue with installation
pip install streamlit pandas plotly google-genai openpyxl numpy
```

### Solution 4: Use conda instead (if installed)
```cmd
conda create -n ecommerce python=3.11
conda activate ecommerce
pip install streamlit pandas plotly google-genai openpyxl numpy
```

### Solution 5: Check Python installation
```cmd
# Check Python version
python --version

# If using Python 3.13, try with explicit version
py -3.11 -m venv venv
```

## Complete Working Commands for Windows:

```cmd
# Method 1: Simple retry with cleanup
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install streamlit pandas plotly google-genai openpyxl numpy
set GEMINI_API_KEY=your_api_key_here
python load_attached_data.py
streamlit run app.py --server.port 5000
```

```cmd
# Method 2: Using external venv location
python -m venv C:\temp\ecommerce_venv
C:\temp\ecommerce_venv\Scripts\activate
pip install streamlit pandas plotly google-genai openpyxl numpy
set GEMINI_API_KEY=your_api_key_here
python load_attached_data.py
streamlit run app.py --server.port 5000
```

## Alternative: Skip Virtual Environment (Quick Test)
```cmd
# Install directly (not recommended for production)
pip install streamlit pandas plotly google-genai openpyxl numpy
set GEMINI_API_KEY=your_api_key_here
python load_attached_data.py
streamlit run app.py --server.port 5000
```

## Notes:
- Python 3.13 sometimes has venv issues - try Python 3.11 if available
- Antivirus software can sometimes block venv creation
- Long file paths on Windows can cause issues
- Administrator privileges often resolve permission problems