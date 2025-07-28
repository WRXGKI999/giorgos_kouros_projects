insert into violations select distinct vcode, vdescription, vcategory from inspections_data order by vcode

 insert into timeinfo select distinct insdate, insyear, insmonth, insday,insweekday from inspections_data order by insdate

 insert into restaurants select distinct rid, lat, lon from inspections_data order by rid

 insert into inspection_type select distinct inscode, instype from inspections_data order by inscode

 insert into ins_data select rid, insdate, inscode, vcode, criticalissue, nonCriticalissue from inspections_data
