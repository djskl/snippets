-- UPDATE t619 SET rast = ST_SetValue(rast,1, st_polygonfromtext('POLYGON((100 39, 100 46, 108 46, 108 39, 100 39))', 4326),10)

-- insert into t619_parts values(1, (select ST_Clip(rast,st_polygonfromtext('POLYGON((100 39, 100 46, 108 46, 108 39, 100 39))', 4326), true) from t619 where rid=1));

-- UPDATE t619_parts SET rast = ST_Reclass(rast, 1, '[-2-285]:[1-10]', '4BUI') WHERE rid = 1;

-- UPDATE t619 SET rast = ST_MapAlgebra(rast, 1, (select rast from t619_parts where rid=1), 1, '[rast2]') where rid = 1;

/*
DROP TABLE t619 CASCADE;

DROP FUNCTION updaterast(integer,text,text);

CREATE FUNCTION updateRast(layerid int, poly_wkt text, reclassexpr text)
RETURNS BOOLEAN AS $$

DECLARE
	success BOOLEAN;
	tmp_rast_1 raster;
	tmp_rast_2 raster;
BEGIN
	select ST_Clip(rast, st_polygonfromtext($2, 4326), true) from t619 where rid=$1 into tmp_rast_1;
	select ST_Reclass(tmp_rast_1, $3, '8BUI') into tmp_rast_2;
	update t619 set rast = ST_MapAlgebra(rast, tmp_rast_2, '[rast2]', NULL, 'FIRST', '[rast2]', '[rast1]') where rid=$1;
	return true;
END;
$$
LANGUAGE plpgsql
*/

select updateRast(1, 'POLYGON((100 39, 100 46, 108 46, 108 39, 100 39))', '[-2-285]:[1-10]');

