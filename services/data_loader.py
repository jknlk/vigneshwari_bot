import pandas as pd
import os
from typing import Dict, Any
from services.database_service import DatabaseService

class DataLoader:
    def __init__(self):
        """Initialize data loader"""
        pass
    
    def load_uploaded_data(self, files: Dict[str, Any], db_service: DatabaseService) -> None:
        """Load uploaded Excel files into database"""
        try:
            # Process Ad Sales and Metrics
            if 'ad_sales' in files:
                ad_sales_df = pd.read_excel(files['ad_sales'])
                ad_sales_df = self.clean_dataframe(ad_sales_df)
                db_service.create_table_from_dataframe(ad_sales_df, 'ad_sales_metrics')
            
            # Process Total Sales and Metrics
            if 'total_sales' in files:
                total_sales_df = pd.read_excel(files['total_sales'])
                total_sales_df = self.clean_dataframe(total_sales_df)
                db_service.create_table_from_dataframe(total_sales_df, 'total_sales_metrics')
            
            # Process Eligibility Table
            if 'eligibility' in files:
                eligibility_df = pd.read_excel(files['eligibility'])
                eligibility_df = self.clean_dataframe(eligibility_df)
                db_service.create_table_from_dataframe(eligibility_df, 'eligibility_table')
            
            print("All files processed and loaded into database successfully!")
            
        except Exception as e:
            raise Exception(f"Error loading uploaded data: {str(e)}")
    
    def load_sample_data(self, db_service: DatabaseService) -> None:
        """Load sample data from CSV files into database"""
        try:
            sample_data_dir = 'sample_data'
            
            if not os.path.exists(sample_data_dir):
                raise Exception("Sample data directory not found. Please generate sample data first.")
            
            # Load each CSV file
            csv_files = {
                'ad_sales_metrics.csv': 'ad_sales_metrics',
                'total_sales_metrics.csv': 'total_sales_metrics', 
                'eligibility_table.csv': 'eligibility_table'
            }
            
            for filename, table_name in csv_files.items():
                filepath = os.path.join(sample_data_dir, filename)
                if os.path.exists(filepath):
                    df = pd.read_csv(filepath)
                    db_service.create_table_from_dataframe(df, table_name)
                    print(f"Loaded {filename} into {table_name}")
            
            print("Sample data loaded successfully!")
            
        except Exception as e:
            raise Exception(f"Error loading sample data: {str(e)}")
    
    def validate_data_structure(self, df: pd.DataFrame, expected_columns: list) -> bool:
        """Validate that dataframe has expected structure"""
        try:
            df_columns = [col.lower().replace(' ', '_') for col in df.columns]
            expected_columns_lower = [col.lower().replace(' ', '_') for col in expected_columns]
            
            missing_columns = set(expected_columns_lower) - set(df_columns)
            
            if missing_columns:
                print(f"Warning: Missing columns: {missing_columns}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating data structure: {str(e)}")
            return False
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize dataframe"""
        try:
            # Remove completely empty rows and columns
            df = df.dropna(how='all').dropna(axis=1, how='all')
            
            # Standardize column names
            df.columns = [
                col.strip().lower()
                .replace(' ', '_')
                .replace('(', '')
                .replace(')', '')
                .replace('-', '_')
                .replace('.', '_')
                for col in df.columns
            ]
            
            # Convert numeric columns
            for col in df.columns:
                if df[col].dtype == 'object':
                    # Try to convert to numeric
                    numeric_series = pd.to_numeric(df[col], errors='coerce')
                    if not pd.isna(numeric_series).all():
                        df[col] = numeric_series
            
            # Fill NaN values appropriately
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64']:
                    df[col] = df[col].fillna(0)
                else:
                    df[col] = df[col].fillna('Unknown')
            
            return df
            
        except Exception as e:
            raise Exception(f"Error cleaning dataframe: {str(e)}")
