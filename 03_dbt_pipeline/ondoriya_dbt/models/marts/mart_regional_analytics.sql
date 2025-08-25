{{ config(materialized='incremental') }}

with regional_base as (
    select 
        r.region_id,
        r.ancient_name,
        r.colloquial_name,
        r.current_faction,
        r.density_tier,
        rb.biome
    from {{ source('silver', 'stg_regions') }} r
    left join {{ source('silver', 'stg_region_biome') }} rb 
        on r.region_id = rb.region_id
),

population_stats as (
    select 
        region_id,
        count(*) as total_population,
        avg(age) as avg_age
    from {{ source('silver', 'stg_people') }}
    group by region_id
),

faction_breakdown as (
    select 
        region_id,
        faction,
        count(*) as faction_population,
        count(*) * 100.0 / sum(count(*)) over (partition by region_id) as faction_percentage
    from {{ source('silver', 'stg_people') }}
    group by region_id, faction
)

select 
    rb.region_id,
    rb.ancient_name,
    rb.colloquial_name,
    rb.current_faction,
    rb.density_tier,
    rb.biome,
    ps.total_population,
    ps.avg_age
from regional_base rb
left join population_stats ps on rb.region_id = ps.region_id