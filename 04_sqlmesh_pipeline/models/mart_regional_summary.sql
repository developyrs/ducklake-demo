MODEL (
    name analytics.regional_summary,
    kind FULL,
    cron '@daily',
    grain region_id
);

WITH regional_base AS (
    SELECT 
        region_id,
        region_name,
        current_faction,
        primary_industry,
        density_tier
    FROM staging.stg_regions
),

population_stats AS (
    SELECT 
        region_id,
        COUNT(*) as total_population,
        AVG(age) as avg_age,
        MIN(age) as min_age,
        MAX(age) as max_age
    FROM my_lake.bronze.people
    GROUP BY region_id
)

SELECT 
    rb.region_id,
    rb.region_name,
    rb.current_faction,
    rb.primary_industry,
    rb.density_tier,
    ps.total_population,
    ROUND(ps.avg_age, 2) as avg_age,
    ps.min_age,
    ps.max_age
FROM regional_base rb
LEFT JOIN population_stats ps ON rb.region_id = ps.region_id;