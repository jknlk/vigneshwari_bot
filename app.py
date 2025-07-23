import streamlit as st
import pandas as pd
import os
import google.generativeai as genai






from dotenv import load_dotenv
load_dotenv()
from services.database_service import DatabaseService
from services.ai_service import AIService
from services.visualization_service import VisualizationService
from services.data_loader import DataLoader
from utils.sample_data_generator import SampleDataGenerator

# Page configuration
st.set_page_config(
    page_title="E-Commerce Data Analysis AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_services():
    """Initialize all services"""
    if 'db_service' not in st.session_state:
        st.session_state.db_service = DatabaseService()
    if 'ai_service' not in st.session_state:
        st.session_state.ai_service = AIService()
    if 'viz_service' not in st.session_state:
        st.session_state.viz_service = VisualizationService()
    if 'data_loader' not in st.session_state:
        st.session_state.data_loader = DataLoader()

def login_page():
    """Simple login interface"""
    st.title("🤖 E-Commerce AI Data Agent")
    st.subheader("Welcome to Vigneshwari's AI-Powered Analytics Platform")
    
    with st.form("login_form"):
        st.write("### Sign In")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Sign In", use_container_width=True)
        
        if submit_button:
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Please enter both username and password")

def data_upload_section():
    """Data upload and processing section"""
    st.header("📊 Data Management")
    
    # Check if sample data should be generated
    if st.button("Generate Sample Data for Demo", use_container_width=True):
        with st.spinner("Generating sample e-commerce data..."):
            try:
                generator = SampleDataGenerator()
                generator.generate_sample_files()
                st.success("Sample data generated successfully!")
                st.session_state.data_loaded = False  # Reset to reload data
            except Exception as e:
                st.error(f"Error generating sample data: {str(e)}")
    
    st.write("---")
    
    # File upload section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Product-Level Ad Sales and Metrics**")
        ad_sales_file = st.file_uploader("Upload Ad Sales Data", type=['xlsx'], key="ad_sales")
    
    with col2:
        st.write("**Product-Level Total Sales and Metrics**")
        total_sales_file = st.file_uploader("Upload Total Sales Data", type=['xlsx'], key="total_sales")
    
    with col3:
        st.write("**Product-Level Eligibility Table**")
        eligibility_file = st.file_uploader("Upload Eligibility Data", type=['xlsx'], key="eligibility")
    
    # Process uploaded files
    if st.button("Process Uploaded Data", use_container_width=True):
        if ad_sales_file and total_sales_file and eligibility_file:
            with st.spinner("Processing uploaded data..."):
                try:
                    # Save uploaded files temporarily
                    files = {
                        'ad_sales': ad_sales_file,
                        'total_sales': total_sales_file,
                        'eligibility': eligibility_file
                    }
                    
                    # Load data into database
                    st.session_state.data_loader.load_uploaded_data(files, st.session_state.db_service)
                    st.session_state.data_loaded = True
                    st.success("Data processed and loaded into database successfully!")
                    
                except Exception as e:
                    st.error(f"Error processing data: {str(e)}")
        else:
            st.warning("Please upload all three Excel files before processing.")
    
    # Check for existing real data or sample data
    if not st.session_state.get('data_loaded', False):
        # First check if we have real data in the database
        try:
            tables = st.session_state.db_service.get_table_info()
            if tables and len(tables) > 0:
                st.session_state.data_loaded = True
                st.info(f"Real e-commerce data loaded! Found {len(tables)} tables with data.")
            elif os.path.exists('sample_data'):
                with st.spinner("Loading sample data..."):
                    st.session_state.data_loader.load_sample_data(st.session_state.db_service)
                    st.session_state.data_loaded = True
                    st.info("Sample data loaded successfully!")
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")

def query_interface():
    """Natural language query interface"""
    st.header("🔍 Ask Questions About Your Data")
    
    if not st.session_state.get('data_loaded', False):
        st.warning("Please load data first using the Data Management section.")
        return
    
    # Example questions
    with st.expander("💡 Example Questions"):
        example_questions = [
            "What is my total sales?",
            "Calculate the RoAS (Return on Ad Spend)",
            "Which product had the highest CPC (Cost Per Click)?",
            "Show me the top 5 products by revenue",
            "What is the average conversion rate?",
            "Which products are eligible for advertising?",
            "What is the total ad spend across all products?"
        ]
        
        for i, question in enumerate(example_questions):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {question}")
            with col2:
                if st.button("Ask", key=f"example_{i}"):
                    st.session_state.current_question = question
    
    # Query input
    question = st.text_input(
        "Ask a question about your e-commerce data:",
        placeholder="e.g., What is the total sales for all products?",
        value=st.session_state.get('current_question', '')
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("🚀 Ask Question", use_container_width=True)
    with col2:
        if st.session_state.get('last_sql'):
            st.code(st.session_state.last_sql, language='sql')
    
    if ask_button and question:
        with st.spinner("Analyzing your question and generating response..."):
            try:
                # Generate SQL query using AI
                sql_query = st.session_state.ai_service.generate_sql_query(question)
                st.session_state.last_sql = sql_query
                
                # Execute query
                results = st.session_state.db_service.execute_query(sql_query)
                
                if results:
                    # Display results
                    st.subheader("📋 Query Results")
                    
                    # Show SQL query
                    with st.expander("🔍 Generated SQL Query"):
                        st.code(sql_query, language='sql')
                    
                    # Display results as dataframe
                    df = pd.DataFrame(results['data'], columns=results['columns'])
                    st.dataframe(df, use_container_width=True)
                    
                    # Generate business insights
                    insights = st.session_state.ai_service.generate_business_insights(question, df)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("💡 Business Insights")
                        st.write(insights)
                    
                    with col2:
                        # Generate and display visualization if applicable
                        chart = st.session_state.viz_service.create_visualization(question, df)
                        if chart:
                            st.subheader("📊 Visualization")
                            st.plotly_chart(chart, use_container_width=True)
                            
                            # Download button for chart
                            chart_html = chart.to_html()
                            st.download_button(
                                label="💾 Download Chart",
                                data=chart_html,
                                file_name=f"chart_{question[:20].replace(' ', '_')}.html",
                                mime="text/html"
                            )
                    
                    # Store results for potential follow-up questions
                    st.session_state.last_results = df
                    st.session_state.last_question = question
                    
                else:
                    st.warning("No results found for your query.")
                    
            except Exception as e:
                st.error(f"Error processing your question: {str(e)}")
                st.write("Please try rephrasing your question or check if the data contains the information you're looking for.")

def database_overview():
    """Show database schema and sample data"""
    st.header("🗄️ Database Overview")
    
    if not st.session_state.get('data_loaded', False):
        st.warning("Please load data first using the Data Management section.")
        return
    
    try:
        # Show table information
        tables = st.session_state.db_service.get_table_info()
        
        for table_name, info in tables.items():
            with st.expander(f"📋 Table: {table_name}"):
                st.write(f"**Columns:** {len(info['columns'])}")
                st.write(f"**Rows:** {info['row_count']}")
                
                # Show column information
                col_df = pd.DataFrame(info['columns'])
                st.dataframe(col_df, use_container_width=True)
                
                # Show sample data
                if st.button(f"Show Sample Data for {table_name}", key=f"sample_{table_name}"):
                    sample_data = st.session_state.db_service.execute_query(f"SELECT * FROM {table_name} LIMIT 5")
                    if sample_data:
                        sample_df = pd.DataFrame(sample_data['data'], columns=sample_data['columns'])
                        st.dataframe(sample_df, use_container_width=True)
                        
    except Exception as e:
        st.error(f"Error loading database overview: {str(e)}")

def main():
    """Main application"""
    initialize_services()
    
    # Check if logged in
    if not st.session_state.get('logged_in', False):
        login_page()
        return
    
    # Sidebar navigation
    st.sidebar.title(f"👋 Welcome, {st.session_state.get('username', 'User')}!")
    
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Data Management", "🔍 Query Interface", "🗄️ Database Overview"]
    )
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # API Key configuration
    with st.sidebar.expander("⚙️ Configuration"):
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=os.getenv("GEMINI_API_KEY", ""),
            help="Enter your Gemini API key for AI functionality"
        )
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
    
    # Main content based on selected page
    if page == "📊 Data Management":
        data_upload_section()
    elif page == "🔍 Query Interface":
        query_interface()
    elif page == "🗄️ Database Overview":
        database_overview()

if __name__ == "__main__":
    main()

