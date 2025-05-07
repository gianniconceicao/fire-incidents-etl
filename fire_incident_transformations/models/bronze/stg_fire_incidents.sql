
/*

*/
with fire_incidents as (

    select *
    from {{ source('public', 'fire_incidents') }}

)

select *
from fire_incidents
where neighborhood_district is not null 
and battalion is not null