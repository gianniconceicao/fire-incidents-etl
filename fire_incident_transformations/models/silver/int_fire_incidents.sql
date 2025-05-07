

/*

*/
with fire_incidents as (

    SELECT
        incident_number,
        exposure_number,
        id,
        address,
        incident_date,
        call_number,
        alarm_dttm,
        arrival_dttm,
        close_dttm,
        city,
        zipcode,
        battalion,
        station_area,
        box,
        suppression_units,
        suppression_personnel,
        ems_units,
        ems_personnel,
        other_units,
        other_personnel,
        first_unit_on_scene,
        estimated_property_loss,
        estimated_contents_loss,
        fire_fatalities,
        fire_injuries,
        civilian_fatalities,
        civilian_injuries,
        number_of_alarms,
        primary_situation,
        mutual_aid,
        action_taken_primary,
        action_taken_secondary,
        action_taken_other,
        detector_alerted_occupants,
        property_use,
        area_of_fire_origin,
        ignition_cause,
        ignition_factor_primary,
        ignition_factor_secondary,
        heat_source,
        item_first_ignited,
        structure_type,
        structure_status,
        fire_spread,
        no_flame_spread,
        detectors_present,
        detector_type,
        detector_operation,
        detector_effectiveness,
        detector_failure_reason,
        automatic_extinguishing_system_present,
        automatic_extinguishing_sytem_type,
        automatic_extinguishing_sytem_perfomance,
        automatic_extinguishing_sytem_failure_reason,
        number_of_sprinkler_heads_operating,
        supervisor_district,
        neighborhood_district,
        point,
        data_as_of,
        data_loaded_at
    from {{ ref('stg_fire_incidents') }}

)

select *
from fire_incidents