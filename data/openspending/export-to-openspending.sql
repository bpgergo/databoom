create table export_budget as
select
f.id as cofog_id, f.value cofog_name, ff.id parent_cofog_id, ff.value parent_cofog_name, fff.id parent_parent_cofog_id, fff.value parent_parent_cofog_name,
e.id econ_id, e.value econ_name, ee.id parent_econ_id, ee.value parent_econ_name, eee.id parent_parent_econ_id, eee.value parent_parent_econ_name,
b.date_start, b.amount
from budget b
inner join func f on (f.id = b.func_id)
inner join econ e on (e.id = b.econ_id)
left outer join func ff on (ff.id = f.parent_id)
left outer join func fff on (fff.id = ff.parent_id)
left outer join econ ee on (ee.id = e.parent_id)
left outer join econ eee on (eee.id = ee.parent_id)
limit 1

copy export_budget to '/tmp/postgres_export/ops_budget.csv' with csv;

