CREATE OR REPLACE FUNCTION public.merge_raster(
    id0 integer,
    id1 integer,
    val integer,
    x0 integer,
    x1 integer,
    nodata integer)
  RETURNS boolean AS
$BODY$

DECLARE
	tmp_rast_1 raster;
	tmp_rast_2 raster;
	tmp_rast_3 raster;
BEGIN
	-- update cluster_data set rast = ST_Reclass(rast, 1, '[1-'||$4||'):0, '||$4||':'||$3||', ('||$4||'-255]:0', '8BUI', $6) where dataid=$1;
	-- update cluster_data set rast = ST_Reclass(rast, 1, '[1-'||$5||'):0, '||$5||':'||$3||', ('||$5||'-255]:0', '8BUI', $6) where dataid=$2;
	select ST_Reclass(rast, 1, '[1-'||$4||'):0, '||$4||':'||$3||', ('||$4||'-255]:0', '8BUI', $6) from cluster_data where dataid=$1 into tmp_rast_1;
	select ST_Reclass(rast, 1, '[1-'||$5||'):0, '||$5||':'||$3||', ('||$5||'-255]:0', '8BUI', $6) from cluster_data where dataid=$2 into tmp_rast_2;
	select ST_Resample(tmp_rast_1, tmp_rast_2) into tmp_rast_3;
	update cluster_data set rast = ST_MapAlgebra(tmp_rast_3, tmp_rast_2, $3::text, NULL, 'SECOND', $6::text, $6::text, $6) where dataid=$2;
	return true;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.merge_raster(integer, integer, integer, integer, integer, integer)
  OWNER TO postgres;

