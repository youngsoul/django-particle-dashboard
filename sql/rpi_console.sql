select count(*) from particle_readings_particlereading;
select * from particle_readings_particlereading order by id desc;

select * from particle_readings_particlereading order by created_at asc limit 20;

with avg_values as (select date(created_at)              as d,
                           extract(HOUR from created_at) as h,
                           date_trunc('hour', created_at) as hh,
                           avg(float_value)              as tempA0_hourly_avg
                    from particle_readings_particlereading
                    where event_name = 'tempA0'
                      and device_id = '250019001247343339383037'
                    group by d, h, hh
                    order by d, h)
select tempA0_hourly_avg, concat(d, ' ', h)::timestamp from avg_values;

create or replace view beehive_hourly_tempa0 as
select date_trunc('hour', created_at) as hourly_date,
                           avg(float_value) as tempA0_hourly_avg
                    from particle_readings_particlereading
                    where event_name = 'tempA0'
                      and device_id = '250019001247343339383037'
                    group by hourly_date
                    order by hourly_date;


drop view beehive_hourly_tempa4;
create or replace view beehive_hourly_tempa4 as
select date_trunc('hour', created_at) as hourly_date,
                           avg(float_value) as tempA4_hourly_avg
                    from particle_readings_particlereading
                    where event_name = 'tempA4'
                      and device_id = '250019001247343339383037'
                    group by hourly_date
                    order by hourly_date;

select * from beehive_hourly_tempa0;

drop view beehive_hourly_temp_avg;
create or replace view beehive_hourly_temp_avg as
    select a.hourly_date, (a.tempA0_hourly_avg + b.tempA4_hourly_avg)/2 as tmp_avg
    from beehive_hourly_tempa0 a, beehive_hourly_tempa4 b
    where a.hourly_date = b.hourly_date;
select * from beehive_hourly_temp_avg;



select a.hourly_date, (a.tempA0_hourly_avg + b.tempA4_hourly_avg)/2
from beehive_hourly_tempa0 a, beehive_hourly_tempa4 b
where a.hourly_date = b.hourly_date;

select count(*) from beehive_hourly_tempa0;

select a.id, a.float_value, b.float_value, (a.float_value + b.float_value)/2
from particle_readings_particlereading a, particle_readings_particlereading b
where a.id = b.id and a.device_id = '250019001247343339383037' and a.event_name='tempA0' ;


select *
from particle_readings_particlereading a, particle_readings_particlereading b
where a.id = b.id and a.device_id = '250019001247343339383037';

select * from particle_readings_particlereading where float_value < 80;

select * from particle_readings_particlereading where device_id='250019001247343339383037' order by created_at desc;

select * from particle_readings_particlereading where id=4072;

with s as (
select float_value
from particle_readings_particlereading
where device_id='250019001247343339383037' and event_name='tempA4'
order by created_at desc
limit 3
)
select avg(float_value) from s;
