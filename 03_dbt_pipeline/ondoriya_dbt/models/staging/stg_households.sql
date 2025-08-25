{{ config(materialized='incremental') }}

Select 
    household_id,
    region_id,
    household_type
from {{ source('bronze', 'households') }}