# E-Commerce AI Data Analysis Agent

## Overview

This is a Streamlit-based AI-powered data analysis platform designed for e-commerce analytics. The application allows users to upload e-commerce data, analyze it using natural language queries powered by Google's Gemini AI, and generate visualizations automatically. The system focuses on analyzing advertising performance, sales metrics, and product eligibility data.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a service-oriented architecture with clear separation of concerns:

- **Frontend**: Streamlit web application with login functionality
- **Backend Services**: Modular services for database operations, AI processing, data loading, and visualization
- **Data Storage**: SQLite database for structured data storage
- **AI Integration**: Google Gemini API for natural language to SQL conversion
- **Visualization**: Plotly for interactive chart generation

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point and UI orchestration
- **Features**: User authentication, service initialization, main dashboard
- **Architecture Decision**: Uses Streamlit session state for service persistence

### 2. Database Service (`services/database_service.py`)
- **Purpose**: Handles all database operations and SQL execution
- **Technology**: SQLite for local data storage
- **Key Features**: Dynamic table creation from DataFrames, query execution with result formatting
- **Rationale**: SQLite chosen for simplicity and no external dependencies

### 3. AI Service (`services/ai_service.py`)
- **Purpose**: Natural language processing and SQL query generation
- **Technology**: Google Gemini 2.5 Flash model
- **Key Features**: Context-aware SQL generation with predefined schema understanding
- **Architecture Decision**: Uses structured prompts with schema context for accurate query generation

### 4. Data Loader (`services/data_loader.py`)
- **Purpose**: Handles data ingestion from Excel files and sample data
- **Features**: Column standardization, multi-file processing
- **Design Pattern**: Supports both uploaded files and pre-generated sample data

### 5. Visualization Service (`services/visualization_service.py`)
- **Purpose**: Automatic chart generation based on query results
- **Technology**: Plotly for interactive visualizations
- **Key Features**: Intelligent chart type selection based on question context and data structure
- **Supported Charts**: Bar, pie, line, scatter, histogram

### 6. Sample Data Generator (`utils/sample_data_generator.py`)
- **Purpose**: Generates realistic e-commerce sample data for testing
- **Features**: Creates three main datasets - ad sales metrics, total sales metrics, and product eligibility
- **Design Approach**: Generates correlated realistic data with proper business logic

## Data Flow

1. **User Input**: Natural language questions through Streamlit interface
2. **AI Processing**: Gemini API converts questions to SQL queries using schema context
3. **Data Retrieval**: Database service executes SQL and returns structured results
4. **Visualization**: Automatic chart generation based on question intent and data characteristics
5. **Display**: Results presented in Streamlit interface with both tabular and visual formats

## External Dependencies

### Core Technologies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **SQLite**: Embedded database (via Python sqlite3)
- **Plotly**: Interactive visualization library
- **NumPy**: Numerical computing support

### AI Integration
- **Google Generative AI**: Natural language to SQL conversion
- **Environment Variables**: GEMINI_API_KEY required for AI functionality

### Data Processing
- **Excel Support**: Built-in pandas Excel reading capabilities
- **CSV Support**: Standard pandas CSV processing

## Deployment Strategy

### Local Development
- **Database**: SQLite file-based storage (`ecommerce.db`)
- **Configuration**: Environment variables for API keys
- **Data Persistence**: Local file system for uploaded data and database

### Key Architectural Decisions

1. **SQLite vs. PostgreSQL**: 
   - **Chosen**: SQLite for simplicity and no server setup
   - **Rationale**: Suitable for single-user analysis scenarios, easy deployment
   - **Trade-off**: Limited concurrent users but simplified setup

2. **Gemini vs. Other AI Models**:
   - **Chosen**: Google Gemini 2.5 Flash
   - **Rationale**: Good balance of performance and cost for SQL generation
   - **Alternative**: Could support OpenAI GPT models with similar integration

3. **Streamlit vs. FastAPI+React**:
   - **Chosen**: Streamlit for rapid development
   - **Rationale**: Built-in UI components and session management
   - **Trade-off**: Less customization but faster development

4. **Service Architecture**:
   - **Pattern**: Separate services for distinct responsibilities
   - **Benefits**: Modular, testable, maintainable code
   - **Implementation**: Session state management for service instances

### Security Considerations
- Simple username/password authentication (development-level)
- API key management through environment variables
- SQL injection protection through parameterized queries (implicit in pandas/sqlite integration)

### Scalability Notes
- Current architecture suitable for single-user or small team usage
- Database can be upgraded to PostgreSQL for multi-user scenarios
- Services are designed to be easily replaceable or enhanced