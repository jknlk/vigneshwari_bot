import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional
import numpy as np

class VisualizationService:
    def __init__(self):
        """Initialize visualization service"""
        pass
    
    def create_visualization(self, question: str, data: pd.DataFrame) -> Optional[go.Figure]:
        """Create appropriate visualization based on question and data"""
        try:
            if data.empty:
                return None
            
            # Determine visualization type based on question keywords and data structure
            viz_type = self._determine_viz_type(question, data)
            
            if viz_type == 'pie':
                chart = self._create_pie_chart(data)
            elif viz_type == 'line':
                chart = self._create_line_chart(data)
            elif viz_type == 'scatter':
                chart = self._create_scatter_plot(data)
            elif viz_type == 'histogram':
                chart = self._create_histogram(data)
            else:
                chart = self._create_bar_chart(data)
            
            return chart
                
        except Exception as e:
            print(f"Error creating visualization: {str(e)}")
            return None
    
    def _determine_viz_type(self, question: str, data: pd.DataFrame) -> str:
        """Determine the best visualization type based on question and data"""
        question_lower = question.lower()
        
        # Keywords that suggest specific chart types
        if any(word in question_lower for word in ['distribution', 'frequency', 'histogram']):
            return 'histogram'
        elif any(word in question_lower for word in ['trend', 'over time', 'timeline', 'monthly', 'daily']):
            return 'line'
        elif any(word in question_lower for word in ['share', 'proportion', 'percentage', 'breakdown']):
            return 'pie'
        elif any(word in question_lower for word in ['correlation', 'relationship', 'vs', 'versus']):
            return 'scatter'
        else:
            return 'bar'
    
    def _create_bar_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create a bar chart"""
        try:
            # Find the most appropriate columns for x and y
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            non_numeric_cols = data.select_dtypes(exclude=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 1:
                y_col = numeric_cols[0]
                
                if len(non_numeric_cols) >= 1:
                    x_col = non_numeric_cols[0]
                elif len(numeric_cols) >= 2:
                    x_col = numeric_cols[1]
                else:
                    x_col = data.columns[0]
                
                # Limit data points for better visualization
                plot_data = data.head(20)
                
                fig = px.bar(
                    plot_data, 
                    x=x_col, 
                    y=y_col,
                    title=f"{y_col} by {x_col}",
                    template="plotly_white"
                )
                
                fig.update_layout(
                    xaxis_tickangle=-45,
                    height=500,
                    showlegend=False
                )
                
                return fig
            
            return None
            
        except Exception as e:
            print(f"Error creating bar chart: {str(e)}")
            return None
    
    def _create_pie_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create a pie chart"""
        try:
            # Find categorical and numeric columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            non_numeric_cols = data.select_dtypes(exclude=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 1 and len(non_numeric_cols) >= 1:
                labels_col = non_numeric_cols[0]
                values_col = numeric_cols[0]
                
                # Group by category and sum values
                grouped_data = data.groupby(labels_col)[values_col].sum().reset_index()
                
                # Limit to top 10 categories
                grouped_data = grouped_data.nlargest(10, values_col)
                
                fig = px.pie(
                    grouped_data,
                    values=values_col,
                    names=labels_col,
                    title=f"Distribution of {values_col} by {labels_col}",
                    template="plotly_white"
                )
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=500)
                
                return fig
                
            return None
            
        except Exception as e:
            print(f"Error creating pie chart: {str(e)}")
            return None
    
    def _create_line_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create a line chart"""
        try:
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
                
                # Sort by x column for proper line connection
                plot_data = data.sort_values(by=x_col).head(50)
                
                fig = px.line(
                    plot_data,
                    x=x_col,
                    y=y_col,
                    title=f"{y_col} Trend",
                    template="plotly_white"
                )
                
                fig.update_layout(height=500)
                
                return fig
                
            return None
            
        except Exception as e:
            print(f"Error creating line chart: {str(e)}")
            return None
    
    def _create_scatter_plot(self, data: pd.DataFrame) -> go.Figure:
        """Create a scatter plot"""
        try:
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
                
                plot_data = data.head(100)  # Limit points for performance
                
                fig = px.scatter(
                    plot_data,
                    x=x_col,
                    y=y_col,
                    title=f"{y_col} vs {x_col}",
                    template="plotly_white"
                )
                
                fig.update_layout(height=500)
                
                return fig
                
            return None
            
        except Exception as e:
            print(f"Error creating scatter plot: {str(e)}")
            return None
    
    def _create_histogram(self, data: pd.DataFrame) -> go.Figure:
        """Create a histogram"""
        try:
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 1:
                col = numeric_cols[0]
                
                fig = px.histogram(
                    data,
                    x=col,
                    title=f"Distribution of {col}",
                    template="plotly_white"
                )
                
                fig.update_layout(height=500)
                
                return fig
                
            return None
            
        except Exception as e:
            print(f"Error creating histogram: {str(e)}")
            return None
    
    def create_custom_chart(self, chart_type: str, data: pd.DataFrame, x_col: str = None, y_col: str = None) -> Optional[go.Figure]:
        """Create a custom chart with specified parameters"""
        try:
            if chart_type == 'bar' and x_col and y_col:
                fig = px.bar(data, x=x_col, y=y_col, template="plotly_white")
            elif chart_type == 'line' and x_col and y_col:
                fig = px.line(data, x=x_col, y=y_col, template="plotly_white")
            elif chart_type == 'scatter' and x_col and y_col:
                fig = px.scatter(data, x=x_col, y=y_col, template="plotly_white")
            elif chart_type == 'pie' and x_col and y_col:
                fig = px.pie(data, names=x_col, values=y_col, template="plotly_white")
            else:
                return None
            
            fig.update_layout(height=500)
            return fig
            
        except Exception as e:
            print(f"Error creating custom chart: {str(e)}")
            return None
