# SUMO ()

#### TO CONVERT OSM FILE TO NET FILE CAN YOU READ IT IN SUMO
```netconvert --osm-files berlin.osm.xml -o berlin.net.xml```
also you can use this opsions <br />
``` --geometry.remove --ramps.guess --junctions.join --tls.guess-signals --tls.discard-simple --tls.join --tls.default-type actuated```

#### add ploy
```polyconvert --net-file berlin.net.xml --osm-files berlin.osm --type-file typemap.xml -o berlin.poly.xml```

typemap.xml <br />
you can find in this path: <br />
"<SUMO_HOME>/data/typemap/osmPolyconvert.typ.xml"

### generate random trips:
```randomTrips.py -n map1.net.xml -e 1000 -o map1.trips.xml```
```duarouter -n map1.net.xml --route-files map1.trips.xml -o map.rou.xml --ignore-errors```