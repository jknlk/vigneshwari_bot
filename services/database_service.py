import sqlite3
import pandas as pd
from typing import Dict, List, Any, Optional
import os

class DatabaseService:
    def __init__(self, db_path: str = "ecommerce.db"):
        """Initialize database service"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database connection"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON")
                print(f"Database initialized: {self.db_path}")
        except Exception as e:
            raise Exception(f"Failed to initialize database: {str(e)}")
    
    def create_table_from_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
        """Create table from pandas dataframe"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Table '{table_name}' created with {len(df)} rows")
        except Exception as e:
            raise Exception(f"Failed to create table {table_name}: {str(e)}")
    
    def execute_query(self, query: str) -> Optional[Dict[str, Any]]:
        """Execute SQL query and return results"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                
                # For SELECT queries
                if query.strip().upper().startswith('SELECT'):
                    columns = [description[0] for description in cursor.description]
                    data = cursor.fetchall()
                    return {
                        'columns': columns,
                        'data': data,
                        'row_count': len(data)
                    }
                else:
                    # For other queries (INSERT, UPDATE, DELETE)
                    conn.commit()
                    return {
                        'affected_rows': cursor.rowcount,
                        'message': f"Query executed successfully. {cursor.rowcount} rows affected."
                    }
                    
        except Exception as e:
            raise Exception(f"Database query error: {str(e)}")
    
    def get_table_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all tables in the database"""
        try:
            tables_info = {}
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                tables = cursor.fetchall()
                
                for (table_name,) in tables:
                    # Get column information
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns_info = cursor.fetchall()
                    
                    columns = []
                    for col in columns_info:
                        columns.append({
                            'name': col[1],
                            'type': col[2],
                            'not_null': bool(col[3]),
                            'primary_key': bool(col[5])
                        })
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    
                    tables_info[table_name] = {
                        'columns': columns,
                        'row_count': row_count
                    }
            
            return tables_info
            
        except Exception as e:
            raise Exception(f"Failed to get table information: {str(e)}")
    
    def get_schema_description(self) -> str:
        """Get a description of the database schema for AI context"""
        try:
            tables_info = self.get_table_info()
            schema_desc = "Database Schema:\n\n"
            
            for table_name, info in tables_info.items():
                schema_desc += f"Table: {table_name}\n"
                schema_desc += f"Rows: {info['row_count']}\n"
                schema_desc += "Columns:\n"
                
                for col in info['columns']:
                    schema_desc += f"  - {col['name']} ({col['type']})\n"
                schema_desc += "\n"
            
            return schema_desc
            
        except Exception as e:
            return f"Error getting schema: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                return True
        except Exception:
            return False
    
    def close(self):
        """Close database connection (not needed for sqlite3 with context manager)"""
        pass
