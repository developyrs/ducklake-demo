MODEL (
    name staging.stg_regions,
    kind VIEW
);

SELECT 
    Region_ID as region_id,
    Ancient_Name as region_name,
    Current_Faction as current_faction,
    Full_Name as full_name,
    Primary_Industry as primary_industry,
    Density_Tier as density_tier
FROM 
    my_lake.bronze.regions
WHERE 
    Region_ID IS NOT NULL;