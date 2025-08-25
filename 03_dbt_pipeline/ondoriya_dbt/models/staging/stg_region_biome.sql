{{ config(materialized='incremental') }}

select 
    Region_ID as region_id,
    Biome as biome,
    -- other biome-related columns
from {{ source('bronze', 'region_biome') }}