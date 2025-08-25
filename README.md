# DuckLake Demo: The Local Lakehouse

A complete demonstration of building a production-grade data lakehouse on your laptop using DuckDB, DuckLake, dbt, and SQLMesh.

## Overview

This project demonstrates the "Local Lakehouse" architecture - a modern data stack that runs entirely on your local machine while providing enterprise-grade capabilities including ACID transactions, time travel, and sophisticated data transformations.

**Key Technologies:**
- **DuckDB**: High-performance analytical database engine
- **DuckLake**: Open table format providing ACID transactions and versioning
- **dbt**: Data transformation and testing framework
- **SQLMesh**: Next-generation data transformation and orchestration
- **Streamlit**: Interactive data visualization dashboard

## Dataset

**Ondoriya Synthetic World Dataset**
- 1,425,690 people across 200 regions
- 4 political factions with demographic distributions
- Regional biome classifications and political control data
- Age demographics and population distributions



## Architecture

### Data Flow
```
Raw CSVs → DuckLake Bronze → Silver (Staging) → Gold (Marts) → Dashboard
```

### Layer Descriptions

**Bronze Layer**: Raw data ingested as-is into DuckLake format
- ACID compliant storage
- Time travel capabilities
- Schema enforcement
- Automatic compression and optimization

**Silver Layer**: Cleaned and standardized data
- Column name standardization
- Data type corrections
- Basic validation and quality checks
- Optimized for downstream consumption

**Gold Layer**: Business-ready analytical tables
- Aggregated metrics and KPIs
- Dimensional models
- Regional and faction analytics
- Performance optimized for querying

## Quick Start

### Prerequisites
```bash
# Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install duckdb ducklake dbt-duckdb sqlmesh streamlit plotly pandas
```

### 1. Data Ingestion
```bash
cd 02_bronze_ingestion/
python ingest_to_ducklake.py
```

### 2. dbt Pipeline
```bash
cd 03_dbt_pipeline/
dbt run
dbt test
```

### 3. SQLMesh Pipeline
```bash
cd 04_sqlmesh_pipeline/
sqlmesh plan dev
# Type 'y' when prompted to apply changes
```

### 4. Launch Dashboard
```bash
cd 05_streamlit_dashboard/
streamlit run dashboard.py
```

## Key Features Demonstrated

### DuckLake Capabilities
- **ACID Transactions**: Guaranteed data consistency
- **Time Travel**: Query historical versions of tables
- **Schema Evolution**: Handle schema changes gracefully
- **Automatic Optimization**: Background compaction and optimization

### Transformation Patterns
- **dbt Approach**: SQL-first, testing-oriented, mature ecosystem
- **SQLMesh Approach**: Next-generation features, virtual environments, advanced state management
- **Side-by-side Comparison**: Same business logic implemented in both frameworks

### Analytics Capabilities
- Regional population analysis
- Faction power distribution
- Demographic trends and breakdowns
- Data quality monitoring
- Interactive visualizations

## Performance Highlights

- **Ingestion**: 1.4M records in under 30 seconds
- **Transformations**: Complex joins and aggregations in seconds
- **Queries**: Sub-second response times on analytical workloads
- **Storage**: 80%+ compression compared to raw CSV

## Use Cases

This architecture is ideal for:

**Development & Testing**
- Local development of data pipelines
- Testing transformation logic
- Prototyping analytical models

**Edge Analytics**
- Embedded analytics in applications
- IoT data processing
- Remote location analytics

**Cost-Sensitive Environments**
- Startups and small teams
- Proof-of-concept projects
- Development environments

**Data Science Workflows**
- Feature engineering pipelines
- Model training data preparation
- Analytical research projects

## Scaling Considerations

**Excellent for** (< 1TB datasets):
- Analytical workloads
- Batch processing
- Single-node performance
- Development workflows

**Consider alternatives for**:
- Multi-petabyte datasets
- High-concurrency OLTP
- Distributed processing requirements
- Multi-region deployments

## dbt vs SQLMesh Comparison

| Feature | dbt | SQLMesh |
|---------|-----|---------|
| **Learning Curve** | Moderate | Steep |
| **Testing** | Built-in framework | Advanced auditing |
| **State Management** | External orchestrator | Built-in incremental |
| **Virtual Environments** | Limited | Advanced |
| **Column Lineage** | Third-party tools | Native support |
| **Ecosystem** | Mature, extensive | Growing, modern |

## Configuration Details

### DuckLake Connection
```python
import duckdb
con = duckdb.connect(":memory:")
con.execute("ATTACH 'ducklake:./data/catalog.ducklake' as my_lake")
```

### dbt profiles.yml
```yaml
ondoriya_dbt:
  outputs:
    dev:
      type: duckdb
      path: ':memory:'
      extensions: [ducklake]
      attach:
        - path: ducklake:./data/catalog.ducklake
          alias: my_lake
      schema: bronze
```

### SQLMesh config.yaml
```yaml
gateways:
  local_gateway:
    connection:
      type: duckdb
      catalogs:
        my_lake:
          type: ducklake
          path: ./data/catalog.ducklake
          data_path: ./data/catalog_data/
```

## Troubleshooting

**Connection Issues**
- Verify DuckLake extension is installed: `INSTALL ducklake;`
- Check file paths are absolute when needed
- Ensure proper permissions on data directory

**Performance Issues**
- Monitor memory usage with large datasets
- Use appropriate materialization strategies
- Consider partitioning for large tables

**Schema Issues**
- Validate column names match between layers
- Check data types in transformations
- Use `DESCRIBE` to inspect table schemas

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- DuckDB team for the incredible analytical engine
- DuckLake contributors for the open table format
- dbt Labs for the transformation framework
- Tobiko Data for SQLMesh innovation
- Streamlit team for the visualization platform


## Contact

For questions about this demo or speaking opportunities:
- Email: daniel@developyr.com
- LinkedIn: /in/wallacedanielk
- Company: developyr.com

---

*Built with ❤️ for the data community*