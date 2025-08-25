{{ config(materialized='incremental') }}

-- Simple staging model to test dbt + DuckLake connection
select 
    Region_ID as region_id,
    Ancient_Name as ancient_name,
    Current_Faction as current_faction,
    Colloquial_Name as colloquial_name,
    Founding_Era as founding_era,
    Density_Tier as density_tier
from {{ source('bronze', 'regions') }}