# Netflix Advanced Analytics Dashboard

A comprehensive Streamlit dashboard for analyzing Netflix data with interactive visualizations and advanced analytics.

## Features

- **Interactive Filters**: Filter by type, year range, and countries
- **Advanced KPI Cards**: Key performance indicators and metrics
- **Interactive Charts**: Using Plotly Express for dynamic visualizations
- **Data Exploration**: Explore Netflix content with advanced analytics
- **Download Functionality**: Export filtered data as CSV

## Quick Start

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

### Streamlit Cloud Deployment (Recommended)

#### Method 1: Direct GitHub Integration
1. **Push to GitHub**
   - Create a new repository on GitHub
   - Upload all files including:
     - `app.py` (main application)
     - `requirements.txt`
     - `netflix_cleaned.csv`
     - `.gitignore`
     - `.streamlit/` folder

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your GitHub repository
   - Set main file path to `app.py`
   - Click "Deploy"

#### Method 2: Manual Upload
1. Zip your project files
2. Upload directly to Streamlit Cloud

## GitHub Repository Structure

```
netflix-analytics-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── netflix_cleaned.csv   # Netflix dataset
├── .gitignore            # Git ignore file
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## Data Requirements

Ensure `netflix_cleaned.csv` is present in the repository root. The file should contain Netflix titles data with columns like:
- title, type, release_year, duration, rating, country, etc.

## Dependencies

All required packages are listed in `requirements.txt`:
- streamlit==1.46.1
- pandas==2.3.0
- plotly==6.2.0
- numpy==2.3.1

## Troubleshooting

- **File not found errors**: Ensure `netflix_cleaned.csv` is in the same directory as `app.py`
- **Memory issues**: For large datasets, consider using data sampling or caching
- **Deployment issues**: Check that all dependencies are correctly specified in `requirements.txt`

## Live Demo

Once deployed, your app will be accessible at: `https://your-app-name.streamlit.app`

## Support

For issues or questions, please open an issue on GitHub or contact the repository maintainer.
