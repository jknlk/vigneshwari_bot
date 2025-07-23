import os
import pandas as pd
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AIService:
    def __init__(self):
        """Initialize AI service with Gemini API"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Choose model: "gemini-1.5-pro" or "gemini-1.5-flash"
        self.model_name = "gemini-1.5-flash"
        self.model = genai.GenerativeModel(model_name=self.model_name)

    def generate_sql_query(self, question: str, schema_context: str = "") -> str:
        """Convert natural language question to SQL query"""
        try:
            schema_info = """
            Database Schema (Real E-commerce Data):

            Table: ad_sales_metrics (3696 rows)
            - Columns: date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold

            Table: total_sales_metrics (702 rows)
            - Columns: date, item_id, total_sales, total_units_ordered

            Table: eligibility_table (4381 rows)
            - Columns: eligibility_datetime_utc, item_id, eligibility, message

            Notes:
            - item_id is the product identifier across all tables
            - RoAS = ad_sales / ad_spend
            - CPC = ad_spend / clicks
            - CTR = clicks / impressions
            - Use proper SQL for SQLite and JOINs where required
            """

            prompt = f"""
            You are an expert SQL query generator for e-commerce data analysis.

            {schema_info}

            Question: {question}

            Generate a SQL query that answers this question.
            Follow these rules:
            - Use only the tables and columns above
            - SQLite syntax only
            - Use correct JOINs, WHERE, GROUP BY, etc.
            - No explanation, return only SQL query

            SQL Query:
            """

            response = self.model.generate_content(prompt)
            sql_query = response.text.strip() if response.text else ""

            # Remove markdown formatting if any
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]

            return sql_query.strip()

        except Exception as e:
            raise Exception(f"Failed to generate SQL query: {str(e)}")

    def generate_business_insights(self, question: str, data: pd.DataFrame) -> str:
        """Generate business insights from query results"""
        try:
            data_summary = f"Data shape: {data.shape}\n"
            data_summary += f"Columns: {list(data.columns)}\n"
            data_summary += f"Sample data:\n{data.head().to_string()}\n"

            if len(data) > 0:
                data_summary += f"\nBasic statistics:\n{data.describe().to_string()}"

            prompt = f"""
            You are a business analyst expert specializing in e-commerce data.

            Question: {question}

            Query Results:
            {data_summary}

            Provide:
            - Key insights
            - Business implications
            - Recommendations
            - Trends or concerns
            """

            response = self.model.generate_content(prompt)
            return response.text or "Unable to generate insights at this time."

        except Exception as e:
            return f"Error generating business insights: {str(e)}"

    def suggest_visualization_type(self, question: str, data: pd.DataFrame) -> str:
        """Suggest appropriate visualization type based on question and data"""
        try:
            data_info = f"Columns: {list(data.columns)}, Rows: {len(data)}"

            prompt = f"""
            Based on this e-commerce question and data structure, suggest a visualization type.

            Question: {question}
            Data: {data_info}

            Choose one: bar, line, pie, scatter, histogram, box, area.
            Return only the name.
            """

            response = self.model.generate_content(prompt)
            viz_type = response.text.strip().lower() if response.text else 'bar'
            valid_types = ['bar', 'line', 'pie', 'scatter', 'histogram', 'box', 'area']

            return viz_type if viz_type in valid_types else 'bar'

        except Exception:
            return 'bar'

    def test_api_connection(self) -> bool:
        """Test connection to Gemini API"""
        try:
            response = self.model.generate_content("Say 'API Working'")
            return response.text and "API Working" in response.text
        except Exception:
            return False

