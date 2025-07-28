CREATE TABLE inspections_data (
	rid int,
	lat float,
	lon float,
	insdate date,
	insyear int,
	insmonth int,
	insday int,
	insweekday int,
	inscode int,
	instype nvarchar(100),
	criticalissue int,
	nonCriticalissue int,
	vcode int,
	vdescription nvarchar(255),
	vcategory nvarchar(255)
)

bulk insert inspections_data
from 'C:\Users\geoko\Desktop\inspections_data\inspections_data.txt'
with (datafiletype = 'widechar', firstrow = 2, fieldterminator = '|',
rowterminator = '\n');
