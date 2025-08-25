{{ config(materialized='incremental') }}

select 
    r.current_faction,
    count(*) as total_population,
    avg(age) as avg_age,
    min(age) as min_age,
    max(age) as max_age,
    count(distinct region_id) as regions_present
from {{ source('silver', 'stg_people') }} p 
left join {{ source('silver', 'stg_regions') }} r 
    on p.current_region_id = r.region_id
group by r.current_faction
order by total_population desc