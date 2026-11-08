Original description
=====================

5 sources
---------- 
Fields:
----------
label: the name of the geographical point.
lat: latitude
lon: longitude
id: unique id of the entity
ontology: the source title. Sources are listed as "dbpedia, freebase, newyork times, geonames"
---------
lat and lon can be missing
---------
The file combinedSettlements(PerfectMatch).json contains the matched entites named as clusteredVertices

Repackaging Information
=======================

The original files were repackaged as 3 CSV files:
1) geographicalSettelments_ids.csv: contains the entries from settlements.json.
2) geographicalSettelments_cluster_map.csv: contains the entries from
   combinedSettlements(PerfectMatch).json.
3) geographicalSettelments_mappings.csv: contains the pairwise combinations
   within each cluster from the cluster mapping.