checkpoint
dbcc dropcleanbuffers
set statistics io on
set statistics time on
select displayName, profileViews
from users
where year(CreationDate) = 2010
order by CreationDate, profileViews;
set statistics time off
set statistics io off

checkpoint
dbcc dropcleanbuffers
create nonclustered index idx1 on users(CreationDate, profileviews) include (displayname)
--nonclustered afou xreiazomaste sygkekrimena pedia tou pinaka users kai oxi olokliro opote mas symferei na kanoume separate ta data pou theloume na mas dosei to 
--query, wste na anaktithoun grigorotera apo ton server xoris na metaboume ston arxiko pinaka users
set statistics io on
set statistics time on
select displayName, profileViews
from users
where CreationDate >= '2010-01-01' AND CreationDate < '2011-01-01'
order by CreationDate, profileViews;
set statistics time off
set statistics io off
drop index idx1 on users


