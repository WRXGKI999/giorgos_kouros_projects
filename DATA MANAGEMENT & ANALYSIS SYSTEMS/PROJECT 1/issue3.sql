checkpoint
dbcc dropcleanbuffers
set statistics io on
set statistics time on
SELECT TagName, COUNT(*) AS UpVotes FROM Tags
INNER JOIN PostTags ON PostTags.TagId = Tags.tagid
INNER JOIN Posts ON Posts.ParentId = PostTags.PostId
INNER JOIN Users ON Posts.OwnerUserId=Users.Userid
INNER JOIN Votes ON Votes.PostId = Posts.postId
INNER JOIN VoteTypes ON Votes.voteTypeId=VoteTypes.VoteTypeID
WHERE VoteTypeName='UpVote' AND Users.displayName = 'Dominik Weber'
GROUP BY TagName ORDER BY UpVotes DESC
set statistics time off
set statistics io off

checkpoint
dbcc dropcleanbuffers
create index idx1 on Posts(ParentId, OwnerUserId)
set statistics io on
set statistics time on
SELECT TagName, COUNT(*) AS UpVotes FROM Tags
INNER JOIN PostTags ON PostTags.TagId = Tags.tagid
INNER JOIN Posts ON Posts.ParentId = PostTags.PostId
INNER JOIN Users ON Posts.OwnerUserId=Users.Userid
INNER JOIN Votes ON Votes.PostId = Posts.postId
INNER JOIN VoteTypes ON Votes.voteTypeId=VoteTypes.VoteTypeID
WHERE VoteTypeName='UpVote' AND Users.displayName = 'Dominik Weber'
GROUP BY TagName ORDER BY UpVotes DESC
set statistics time off
set statistics io off

checkpoint
dbcc dropcleanbuffers
create index idx2 on Votes(PostId, voteTypeId) 
set statistics io on
set statistics time on
SELECT TagName, COUNT(*) AS UpVotes FROM Tags
INNER JOIN PostTags ON PostTags.TagId = Tags.tagid
INNER JOIN Posts ON Posts.ParentId = PostTags.PostId
INNER JOIN Users ON Posts.OwnerUserId=Users.Userid
INNER JOIN Votes ON Votes.PostId = Posts.postId
INNER JOIN VoteTypes ON Votes.voteTypeId=VoteTypes.VoteTypeID
WHERE VoteTypeName='UpVote' AND Users.displayName = 'Dominik Weber'
GROUP BY TagName ORDER BY UpVotes DESC
set statistics time off
set statistics io off

checkpoint
dbcc dropcleanbuffers
create index idx3 on Users(displayName)
set statistics io on
set statistics time on
SELECT TagName, COUNT(*) AS UpVotes FROM Tags
INNER JOIN PostTags ON PostTags.TagId = Tags.tagid
INNER JOIN Posts ON Posts.ParentId = PostTags.PostId
INNER JOIN Users ON Posts.OwnerUserId=Users.Userid
INNER JOIN Votes ON Votes.PostId = Posts.postId
INNER JOIN VoteTypes ON Votes.voteTypeId=VoteTypes.VoteTypeID
WHERE VoteTypeName='UpVote' AND Users.displayName = 'Dominik Weber'
GROUP BY TagName ORDER BY UpVotes DESC
set statistics time off
set statistics io off
drop index idx1 on Posts
drop index idx2 on Votes
drop index idx3 on Users


