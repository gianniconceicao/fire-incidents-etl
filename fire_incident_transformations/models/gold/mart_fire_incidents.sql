
/*
*/
with number_of_incidents as (
    select
        incident_date,
        neighborhood_district,
        battalion,
        count(*) as total_incidents,
        sum(
            case when fire_fatalities > 0 then 1 else 0 end
        ) as incidents_with_fatalities,
        sum(
            case when fire_fatalities = 0 or fire_fatalities is null then 1 else 0 end
        ) as incidents_without_fatalities,
        sum(
            case when fire_injuries > 0 then 1 else 0 end
        ) as incidents_with_injuries,
        sum(
            case when fire_injuries = 0 or fire_injuries is null then 1 else 0 end
        ) as incidents_without_injuries
    from {{ ref('int_fire_incidents') }}
    group by incident_date, neighborhood_district, battalion
)

select *
from number_of_incidents
order by incident_date, neighborhood_district, battalion