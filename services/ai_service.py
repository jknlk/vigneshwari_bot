import os
import json
from google import genai
from google.genai import types
import pandas as pd
from typing import Optional

class AIService:
    def __init__(self):
        """Initialize AI service with Gemini API"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"
    
    def generate_sql_query(self, question: str, schema_context: str = "") -> str:
        """Convert natural language question to SQL query"""
        try:
            # Define the database schema context based on actual loaded data
            schema_info = """
            Database Schema (Real E-commerce Data):
            
            Table: ad_sales_metrics (3696 rows)
            - Contains product-level advertising sales and metrics data
            - Columns: date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold
            
            Table: total_sales_metrics (702 rows)
            - Contains product-level total sales performance metrics
            - Columns: date, item_id, total_sales, total_units_ordered
            
            Table: eligibility_table (4381 rows)
            - Contains product eligibility information for advertising
            - Columns: eligibility_datetime_utc, item_id, eligibility, message
            
            Important Notes:
            - item_id is the product identifier across all tables
            - All monetary values (ad_sales, ad_spend, total_sales) are in currency units
            - RoAS (Return on Ad Spend) = ad_sales / ad_spend
            - CPC = Cost Per Click = ad_spend / clicks
            - CTR = Click Through Rate = clicks / impressions
            - Use appropriate JOINs on item_id to combine data from multiple tables
            - eligibility column: 1 = eligible, 0 = not eligible
            - Always use proper SQL syntax for SQLite
            """
            
            prompt = f"""
            You are an expert SQL query generator for e-commerce data analysis.
            
            {schema_info}
            
            Question: {question}
            
            Generate a SQL query that answers this question. Follow these rules:
            1. Use only the tables and columns mentioned in the schema
            2. Write clean, efficient SQL for SQLite
            3. Use proper JOINs when data from multiple tables is needed
            4. Include appropriate WHERE, GROUP BY, ORDER BY clauses as needed
            5. For calculations like RoAS, use the formula: ad_revenue / ad_spend
            6. Return only the SQL query, no explanations
            7. Ensure the query will return meaningful results
            
            SQL Query:
            """
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            sql_query = response.text.strip() if response.text else ""
            
            # Clean up the response - remove any markdown formatting
            if sql_query.startswith('```sql'):
                sql_query = sql_query[6:]
            if sql_query.endswith('```'):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
            
        except Exception as e:
            raise Exception(f"Failed to generate SQL query: {str(e)}")
    
    def generate_business_insights(self, question: str, data: pd.DataFrame) -> str:
        """Generate business insights from query results"""
        try:
            # Convert DataFrame to string representation for the AI
            data_summary = f"Data shape: {data.shape}\n"
            data_summary += f"Columns: {list(data.columns)}\n"
            data_summary += f"Sample data:\n{data.head().to_string()}\n"
            
            if len(data) > 0:
                data_summary += f"\nBasic statistics:\n{data.describe().to_string()}"
            
            prompt = f"""
            You are a business analyst expert specializing in e-commerce data analysis.
            
            Question asked: {question}
            
            Query Results:
            {data_summary}
            
            Please provide actionable business insights based on this data. Include:
            1. Key findings from the data
            2. Business implications
            3. Recommendations for improvement
            4. Any trends or patterns observed
            5. Potential areas of concern or opportunity
            
            Keep the insights practical and focused on e-commerce business metrics.
            Format the response in a clear, structured manner.
            """
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            return response.text or "Unable to generate insights at this time."
            
        except Exception as e:
            return f"Error generating business insights: {str(e)}"
    
    def suggest_visualization_type(self, question: str, data: pd.DataFrame) -> str:
        """Suggest appropriate visualization type based on question and data"""
        try:
            data_info = f"Columns: {list(data.columns)}, Rows: {len(data)}"
            
            prompt = f"""
            Based on this e-commerce data question and the resulting data structure, suggest the most appropriate visualization type.
            
            Question: {question}
            Data structure: {data_info}
            
            Choose from: bar, line, pie, scatter, histogram, box, area
            Return only the visualization type name, no explanation.
            """
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            viz_type = response.text.strip().lower() if response.text else 'bar'
            valid_types = ['bar', 'line', 'pie', 'scatter', 'histogram', 'box', 'area']
            
            return viz_type if viz_type in valid_types else 'bar'
            
        except Exception:
            return 'bar'  # Default fallback
    
    def test_api_connection(self) -> bool:
        """Test connection to Gemini API"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Hello, respond with 'API Working'"
            )
            return response.text and "API Working" in response.text
        except Exception:
            return False
