import pandas as pd
import os
from services.database_service import DatabaseService
from services.data_loader import DataLoader

def load_attached_excel_files():
    """Load the attached Excel files into the database"""
    try:
        db_service = DatabaseService()
        data_loader = DataLoader()
        
        # File paths for attached Excel files
        file_paths = {
            'ad_sales': 'attached_assets/Product-Level Ad Sales and Metrics (mapped)_1753210886485.xlsx',
            'total_sales': 'attached_assets/Product-Level Total Sales and Metrics (mapped)_1753210886486.xlsx',
            'eligibility': 'attached_assets/Product-Level Eligibility Table (mapped)_1753210886486.xlsx'
        }
        
        # Check if files exist and load them
        for file_type, file_path in file_paths.items():
            if os.path.exists(file_path):
                print(f"Loading {file_type} data from {file_path}")
                try:
                    df = pd.read_excel(file_path)
                    print(f"Raw data shape: {df.shape}")
                    print(f"Columns: {list(df.columns)}")
                    
                    # Clean the dataframe
                    df_cleaned = data_loader.clean_dataframe(df)
                    print(f"Cleaned data shape: {df_cleaned.shape}")
                    print(f"Cleaned columns: {list(df_cleaned.columns)}")
                    
                    # Map file types to table names
                    table_mapping = {
                        'ad_sales': 'ad_sales_metrics',
                        'total_sales': 'total_sales_metrics',
                        'eligibility': 'eligibility_table'
                    }
                    
                    table_name = table_mapping[file_type]
                    db_service.create_table_from_dataframe(df_cleaned, table_name)
                    print(f"Successfully loaded {file_type} data into {table_name} table")
                    print("-" * 50)
                    
                except Exception as e:
                    print(f"Error loading {file_type}: {str(e)}")
            else:
                print(f"File not found: {file_path}")
        
        # Show database overview
        tables_info = db_service.get_table_info()
        print("\nDatabase Overview:")
        for table_name, info in tables_info.items():
            print(f"Table: {table_name} - {info['row_count']} rows")
            for col in info['columns'][:5]:  # Show first 5 columns
                print(f"  - {col['name']} ({col['type']})")
        
        print("\nData loading completed successfully!")
        
    except Exception as e:
        print(f"Error in data loading process: {str(e)}")

if __name__ == "__main__":
    load_attached_excel_files()