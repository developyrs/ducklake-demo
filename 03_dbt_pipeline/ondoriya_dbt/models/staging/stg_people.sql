{{ config(materialized='incremental') }}

select 
    person_id,
    first_name,
    family_name,
    age, 
    current_region_id,
    household_id

from {{ source('bronze', 'people') }}