checkpoint
dbcc dropcleanbuffers
set statistics io on
set statistics time on
select top 20
	DisplayName, UserId, AVG(Posts.Score) as Avg_Score
from Users
inner join Posts on UserId = Posts.OwnerUserId
group by DisplayName, UserId
having count(Posts.PostId) > = 100
order by Avg_Score desc
set statistics time off
set statistics io off

checkpoint
dbcc dropcleanbuffers
create index idx1 on Posts (OwnerUserId) include (Score, PostId)
create index idx2 on Users (UserId) include (DisplayName)
set statistics io on
set statistics time on
select top 20
	DisplayName, UserId, AVG(Posts.Score) as Avg_Score
from Users
inner join Posts on UserId = Posts.OwnerUserId
group by DisplayName, UserId
having count(Posts.PostId) > = 100
order by Avg_Score desc
set statistics time off
set statistics io off
drop index idx1 on Posts
drop index idx2 on Users