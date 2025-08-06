import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page config
st.set_page_config(
    page_title="Netflix Advanced Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #E50914;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .section-header {
        color: #E50914;
        font-size: 1.8rem;
        margin: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_cleaned.csv")
    df['duration_clean'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['release_year'] = pd.to_datetime(df['date_added'], errors='coerce').dt.year
    df['month_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.month
    df['day_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.day
    df['country_clean'] = df['country'].str.split(',').str[0].str.strip()
    return df.dropna(subset=['release_year', 'duration_clean'])

df = load_data()

# Sidebar
st.sidebar.title("🎬 Netflix Advanced Analytics")
st.sidebar.markdown("---")

# Sidebar filters
st.sidebar.subheader("🔍 Filters")
selected_type = st.sidebar.multiselect(
    "Select Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

selected_year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (int(df['release_year'].min()), int(df['release_year'].max()))
)

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=df['country_clean'].unique(),
    default=df['country_clean'].value_counts().head(10).index.tolist()
)

# Filter data based on selections
filtered_df = df[
    (df['type'].isin(selected_type)) &
    (df['release_year'].between(selected_year_range[0], selected_year_range[1])) &
    (df['country_clean'].isin(selected_countries))
]

# Main header
st.markdown('<h1 class="main-header">🎬 Netflix Advanced Analytics Dashboard</h1>', unsafe_allow_html=True)

# Advanced KPI Cards
st.markdown("### 📊 Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🎯 Avg Duration</h3>
        <h2>{round(filtered_df['duration_clean'].mean(), 1)}</h2>
        <small>minutes/seasons</small>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🎬 Movies</h3>
        <h2>{filtered_df[filtered_df['type'] == 'Movie'].shape[0]:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📺 TV Shows</h3>
        <h2>{filtered_df[filtered_df['type'] == 'TV Show'].shape[0]:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>⭐ Ratings</h3>
        <h2>{filtered_df['rating'].nunique()}</h2>
        <small>unique</small>
    </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🌍 Countries</h3>
        <h2>{filtered_df['country_clean'].nunique()}</h2>
        <small>represented</small>
    </div>
    """, unsafe_allow_html=True)

# Advanced Analytics Sections
st.markdown("---")

# Layout for advanced charts
col1, col2 = st.columns([2, 1])

with col1:
    # Interactive scatter plot with Plotly
    st.markdown('<h3 class="section-header">📈 Interactive Release Year vs Duration</h3>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        filtered_df,
        x='release_year',
        y='duration_clean',
        color='type',
        size='duration_clean',
        hover_data=['title', 'rating', 'country_clean'],
        title='Content Duration Trends Over Time',
        labels={'duration_clean': 'Duration (min/seasons)', 'release_year': 'Release Year'}
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Type distribution pie chart
    st.markdown('<h3 class="section-header">🥧 Content Type Distribution</h3>', unsafe_allow_html=True)
    type_counts = filtered_df['type'].value_counts()
    fig_pie = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        hole=0.4,
        color_discrete_sequence=['#E50914', '#221F1F']
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

# Second row of advanced charts
col3, col4 = st.columns([1, 2])

with col3:
    # Rating distribution
    st.markdown('<h3 class="section-header">📊 Rating Distribution</h3>', unsafe_allow_html=True)
    rating_counts = filtered_df['rating'].value_counts()
    fig_rating = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        color=rating_counts.values,
        color_continuous_scale='viridis',
        labels={'x': 'Rating', 'y': 'Count'}
    )
    fig_rating.update_layout(height=350)
    st.plotly_chart(fig_rating, use_container_width=True)

with col4:
    # Advanced country analysis
    st.markdown('<h3 class="section-header">🌍 Advanced Country Analysis</h3>', unsafe_allow_html=True)
    country_stats = filtered_df.groupby('country_clean').agg({
        'title': 'count',
        'duration_clean': 'mean',
        'release_year': 'mean'
    }).reset_index()
    country_stats.columns = ['Country', 'Count', 'Avg_Duration', 'Avg_Release_Year']
    country_stats = country_stats.sort_values('Count', ascending=False).head(15)

    fig_country = px.treemap(
        country_stats,
        path=['Country'],
        values='Count',
        color='Avg_Duration',
        hover_data=['Avg_Release_Year'],
        color_continuous_scale='RdYlBu',
        title='Content Distribution by Country'
    )
    fig_country.update_layout(height=350)
    st.plotly_chart(fig_country, use_container_width=True)

# Advanced time series analysis
st.markdown("---")
st.markdown('<h3 class="section-header">📅 Content Addition Timeline</h3>', unsafe_allow_html=True)

# Monthly content addition
monthly_additions = filtered_df.groupby(['release_year', 'month_added']).size().reset_index(name='count')
fig_timeline = px.line(
    monthly_additions,
    x='release_year',
    y='count',
    color='month_added',
    title='Monthly Content Additions Over Time',
    labels={'count': 'Number of Titles Added', 'release_year': 'Year'}
)
fig_timeline.update_layout(height=400)
st.plotly_chart(fig_timeline, use_container_width=True)

# Genre analysis
st.markdown("---")
st.markdown('<h3 class="section-header">🎭 Genre Analysis</h3>', unsafe_allow_html=True)

# Split genres and count
genres = filtered_df['listed_in'].str.split(', ').explode()
genre_counts = genres.value_counts().head(15)

fig_genre = px.bar(
    x=genre_counts.values,
    y=genre_counts.index,
    orientation='h',
    color=genre_counts.values,
    color_continuous_scale='plasma',
    labels={'x': 'Count', 'y': 'Genre'},
    title='Top 15 Most Popular Genres'
)
fig_genre.update_layout(height=400)
st.plotly_chart(fig_genre, use_container_width=True)

# Advanced statistics
st.markdown("---")
st.markdown('<h3 class="section-header">📈 Advanced Statistics</h3>', unsafe_allow_html=True)

# Create two columns for advanced metrics
stat_col1, stat_col2 = st.columns(2)

with stat_col1:
    st.subheader("📊 Duration Statistics")
    duration_stats = filtered_df['duration_clean'].describe()
    st.dataframe(duration_stats, use_container_width=True)

with stat_col2:
    st.subheader("📅 Year Statistics")
    year_stats = filtered_df['release_year'].describe()
    st.dataframe(year_stats, use_container_width=True)

# Interactive data table
st.markdown("---")
st.markdown('<h3 class="section-header">📋 Interactive Data Explorer</h3>', unsafe_allow_html=True)

# Show sample data
if st.checkbox("Show raw data"):
    st.dataframe(filtered_df.head(100), use_container_width=True)

# Download filtered data
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name=f"netflix_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Advanced Netflix Analytics Dashboard | Built with Streamlit</p>
    <p>Data Source: Netflix Titles Dataset</p>
</div>
""", unsafe_allow_html=True)
