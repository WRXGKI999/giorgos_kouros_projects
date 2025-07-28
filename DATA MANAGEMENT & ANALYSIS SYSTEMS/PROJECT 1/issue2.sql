checkpoint
dbcc dropcleanbuffers
set statistics io on
set statistics time on
SELECT users.* FROM users, posts, postTypes WHERE users.userid=posts.ownerUserid and posts.postTypeid=PostTypes.postTypeid and postTypeName='Answer'
EXCEPT
SELECT users.* FROM users, posts, postTypes WHERE users.userid=posts.ownerUserid and posts.postTypeid=PostTypes.postTypeid and postTypeName='Question'
set statistics time off
set statistics io off

checkpoint 
dbcc dropcleanbuffers
set statistics io on
set statistics time on
SELECT * FROM users WHERE EXISTS (
	SELECT 1 FROM posts, PostTypes WHERE posts.postTypeid=PostTypes.postTypeid and postTypeName='Answer' and posts.ownerUserId = users.userId)
AND NOT EXISTS (
    SELECT 1 FROM posts, PostTypes WHERE posts.postTypeid=PostTypes.postTypeid and postTypeName='Question' and posts.ownerUserId = users.userId)
set statistics time off
set statistics io off

checkpoint
dbcc dropcleanbuffers
create index idx1 on posts(ownerUserId, postTypeId)
set statistics io on
set statistics time on
SELECT * FROM users WHERE EXISTS (
	SELECT 1 FROM posts, PostTypes WHERE posts.postTypeid=PostTypes.postTypeid and postTypeName='Answer' and posts.ownerUserId = users.userId)
AND NOT EXISTS (
    SELECT 1 FROM posts, PostTypes WHERE posts.postTypeid=PostTypes.postTypeid and postTypeName='Question' and posts.ownerUserId = users.userId)
set statistics time off
set statistics io off
drop index idx1 on posts