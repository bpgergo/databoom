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
