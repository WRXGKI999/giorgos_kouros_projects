create table violations (
	vcode int primary key,
	vdescription nvarchar(255),
	vcategory nvarchar(255)
)
create table inspection_type (
	inscode int primary key,
	instype nvarchar(100)
)
create table timeinfo (
	insdate date primary key,
	insyear int,
	insmonth int,
	insday int,
	insweekday int
)
create table restaurants (
	rid int primary key,
	lat float,
	lon float
)
create table ins_data (
	rid int,
	insdate date,
	inscode int,
	vcode int,
	criticalissue int,
	nonCriticalissue int,

	primary key (rid, insdate, inscode, vcode),
	foreign key (rid) references restaurants(rid),
	foreign key (insdate) references timeinfo(insdate),
	foreign key (inscode) references inspection_type(inscode),
	foreign key (vcode) references violations(vcode)
)	
