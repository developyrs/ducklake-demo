import streamlit as st
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Ondoriya Lakehouse", layout="wide")
st.title("Ondoriya Lakehouse Dashboard")
st.subheader("Built with DuckDB + DuckLake + dbt + SQLMesh")

# Connect to DuckLake
@st.cache_resource
def get_connection():
    con = duckdb.connect(":memory:")
    con.execute("ATTACH 'ducklake:/Volumes/External/developyr/source/ducklake-demo/data/catalog.ducklake' as my_lake")
    return con

con = get_connection()

# Overview metrics
st.header("Lakehouse Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    people_count = con.execute("SELECT COUNT(*) FROM my_lake.bronze.people").fetchone()[0]
    st.metric("Total Population", f"{people_count:,}")

with col2:
    region_count = con.execute("SELECT COUNT(*) FROM my_lake.bronze.regions").fetchone()[0]
    st.metric("Regions", region_count)

with col3:
    faction_count = con.execute("SELECT COUNT(DISTINCT current_faction) FROM my_lake.gold.mart_faction_analytics").fetchone()[0]
    st.metric("Factions", faction_count)

with col4:
    avg_age = con.execute("SELECT ROUND(AVG(avg_age), 1) FROM my_lake.gold.mart_faction_analytics").fetchone()[0]
    st.metric("Average Age", f"{avg_age} years")

st.divider()

# Regional Analytics Section
st.header("Regional Analytics (dbt Gold Layer)")

# Get regional data
regional_df = con.execute("""
    SELECT 
        ancient_name as region_name,
        current_faction,
        density_tier,
        biome,
        total_population,
        avg_age
    FROM my_lake.gold.mart_regional_analytics 
    WHERE total_population IS NOT NULL
    ORDER BY total_population DESC
    LIMIT 15
""").df()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Population by Region")
    fig1 = px.bar(
        regional_df.head(10), 
        x='total_population',
        y='region_name',
        color='current_faction',
        orientation='h',
        title="Top 10 Most Populated Regions"
    )
    fig1.update_layout(height=500)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Age vs Population by Faction")
    fig2 = px.scatter(
        regional_df,
        x='avg_age',
        y='total_population',
        color='current_faction',
        size='total_population',
        hover_data=['region_name', 'biome'],
        title="Regional Demographics"
    )
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)

# Biome breakdown (replacing industry)
st.subheader("Regional Biome Distribution")
biome_df = regional_df.groupby('biome').agg({
    'total_population': 'sum',
    'region_name': 'count'
}).reset_index()
biome_df.columns = ['biome', 'total_population', 'region_count']

col1, col2 = st.columns(2)

with col1:
    fig3 = px.pie(
        biome_df, 
        values='total_population', 
        names='biome',
        title="Population by Biome"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.bar(
        biome_df.sort_values('region_count', ascending=False),
        x='biome',
        y='region_count',
        title="Number of Regions by Biome"
    )
    fig4.update_xaxes(tickangle=45)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Faction Analytics Section
st.header("Faction Analytics (dbt Gold Layer)")

faction_df = con.execute("""
    SELECT 
        current_faction as faction,
        total_population,
        avg_age,
        min_age,
        max_age,
        regions_present
    FROM my_lake.gold.mart_faction_analytics
    ORDER BY total_population DESC
""").df()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Faction Power Distribution")
    fig5 = px.bar(
        faction_df,
        x='faction',
        y='total_population',
        title="Population by Faction"
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("Faction Age Demographics")
    fig6 = go.Figure()
    
    for _, faction in faction_df.iterrows():
        fig6.add_trace(go.Bar(
            name=faction['faction'],
            x=[faction['faction']],
            y=[faction['avg_age']],
            error_y=dict(
                type='data',
                symmetric=False,
                array=[faction['max_age'] - faction['avg_age']],
                arrayminus=[faction['avg_age'] - faction['min_age']]
            )
        ))
    
    fig6.update_layout(
        title="Average Age by Faction (with min/max range)",
        xaxis_title="Faction",
        yaxis_title="Age",
        showlegend=False
    )
    st.plotly_chart(fig6, use_container_width=True)

# Geographic spread
st.subheader("Faction Geographic Influence")
fig7 = px.bar(
    faction_df,
    x='faction',
    y='regions_present',
    title="Number of Regions Each Faction is Present In"
)
st.plotly_chart(fig7, use_container_width=True)

st.divider()

# SQLMesh Comparison
st.header("SQLMesh Analytics Comparison")

try:
    sqlmesh_df = con.execute("""
        SELECT 
            region_name,
            current_faction,
            total_population,
            avg_age
        FROM my_lake.sqlmesh__analytics.analytics__regional_summary__2903144500 
        ORDER BY total_population DESC
        LIMIT 10
    """).df()
    
    st.subheader("SQLMesh Regional Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**dbt Gold Layer (regional_analytics)**")
        st.dataframe(regional_df[['region_name', 'total_population', 'avg_age']].head())
    
    with col2:
        st.write("**SQLMesh Analytics (regional_summary)**")
        st.dataframe(sqlmesh_df)
        
except Exception as e:
    st.info(f"SQLMesh tables not available: {e}")
    # Add debug info to see what tables exist
    try:
        tables = con.execute("SHOW TABLES FROM my_lake.sqlmesh__analytics").df()
        st.write("Available SQLMesh analytics tables:")
        st.write(tables)
    except:
        st.write("Could not list SQLMesh analytics tables")

st.divider()

# Data Quality Insights
st.header("Data Quality Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    # Age distribution
    age_stats = con.execute("""
        SELECT 
            MIN(age) as min_age,
            MAX(age) as max_age,
            AVG(age) as avg_age,
            COUNT(*) as total_records
        FROM my_lake.bronze.people
    """).fetchone()
    
    st.metric("Age Range", f"{age_stats[0]}-{age_stats[1]} years")
    st.metric("Average Age", f"{age_stats[2]:.1f} years")

with col2:
    # Regional coverage
    coverage = con.execute("""
        SELECT 
            COUNT(DISTINCT p.current_region_id) as regions_with_people,
            COUNT(DISTINCT r.region_id) as total_regions
        FROM my_lake.bronze.people p
        FULL OUTER JOIN my_lake.bronze.regions r ON p.current_region_id = r.region_id
    """).fetchone()
    
    coverage_pct = (coverage[0] / coverage[1]) * 100
    st.metric("Regional Coverage", f"{coverage_pct:.1f}%")
    st.caption(f"{coverage[0]} of {coverage[1]} regions have population data")

with col3:
    # Data completeness
    completeness = con.execute("""
        SELECT 
            COUNT(CASE WHEN age IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) as age_completeness,
            COUNT(CASE WHEN current_region_id IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) as region_completeness
        FROM my_lake.bronze.people
    """).fetchone()
    
    st.metric("Age Data Complete", f"{completeness[0]:.1f}%")
    st.metric("Region Data Complete", f"{completeness[1]:.1f}%")

# Raw data sample
with st.expander("View Raw Bronze Data Sample"):
    bronze_sample = con.execute("SELECT * FROM my_lake.bronze.people LIMIT 5").df()
    st.dataframe(bronze_sample)