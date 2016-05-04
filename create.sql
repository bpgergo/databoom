drop table budget;
drop table func;
drop table org;
drop table econ;


create table func (
id varchar(40) PRIMARY KEY not null,
parent_id varchar(40) references func(id),
value text not null,
tags text 
);



create table econ (
id varchar(40) PRIMARY KEY not null,
parent_id varchar(40) references econ(id),
value text not null 
);

create table org (
id varchar(40) PRIMARY KEY not null,
parent_id varchar(40) references org(id),
value text not null 
);


create table budget(
id 		varchar(40) PRIMARY KEY not null,
func_id 	varchar(40) not null references func(id),
econ_id 	varchar(40) not null references econ(id),
org_id 		varchar(40) not null references org(id),
date_start 	date not null,
date_end 	date,
amount 		numeric not null,
comm 		text,
tags 		text
);


create view func_tree as
select
fff.value  || ' (' || fff.id || ')' parent_parent_cofog_name,
ff.value || ' (' || ff.id || ')' parent_cofog_name ,
f.value || ' (' || f.id || ')' cofog_name ,
b.amount
from budget b
inner join func f on (f.id = b.func_id)
left outer join func ff on (ff.id = f.parent_id)
left outer join func fff on (fff.id = ff.parent_id)
where amount > 0
;

create view econ_tree as
select
eee.value  || ' (' || eee.id || ')' parent_parent_econ_name,
ee.id ||' - '||ee.value  || ' (' || ee.id || ')' parent_econ_name,
e.value || ' (' || e.id || ')' econ_name  ,
b.amount
from budget b
inner join econ e on (e.id = b.econ_id)
left outer join econ ee on (ee.id = e.parent_id)
left outer join econ eee on (eee.id = ee.parent_id)
where amount > 0;


-- copy (select * from econ_tree) to '/tmp/postgres_export/econ_tree.csv' with csv
