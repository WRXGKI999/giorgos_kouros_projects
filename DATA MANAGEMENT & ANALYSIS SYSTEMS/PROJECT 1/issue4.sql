checkpoint
dbcc dropcleanbuffers
set statistics io on
set statistics time on
select top 100
userid, round((100.0 * (Reputation/10)) / (Upvotes+1), 2) as [Ratio %], Reputation, UpVotes, DownVotes
from Users where Reputation > 1000 and Upvotes > 100
order by [Ratio %] desc
set statistics time off
set statistics io off

checkpoint
dbcc dropcleanbuffers
create index idx1 on Users(Reputation, Upvotes) include (UserId, DownVotes) where Upvotes > 100 and Reputation > 1000
set statistics io on
set statistics time on
select top 100
userid, round((100.0 * (Reputation/10)) / (Upvotes+1), 2) as [Ratio %], Reputation, UpVotes, DownVotes
from Users where Reputation > 1000 and Upvotes > 100
order by [Ratio %] desc
set statistics time off
set statistics io off
drop index idx1 on Users

checkpoint
dbcc dropcleanbuffers
create index idx2 on Users(Reputation, Upvotes) include (UserId, DownVotes)
set statistics io on
set statistics time on
select top 100
userid, round((100.0 * (Reputation/10)) / (Upvotes+1), 2) as [Ratio %], Reputation, UpVotes, DownVotes
from Users where Reputation > 1000 and Upvotes > 100
order by [Ratio %] desc
set statistics time off
set statistics io off
drop index idx2 on Users