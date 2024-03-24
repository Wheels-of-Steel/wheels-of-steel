//check if js has connected
console.log("maps.js connected");

mapboxgl.accessToken = 'pk.eyJ1IjoiZW1lcnlqNiIsImEiOiJjbHU0dGRkZzUxYWxwMm5wZHJ4em50M2czIn0.oLZ_d-htIuYQbIhVuiV_JA';
        const map = new mapboxgl.Map({
            container: 'map', // container ID
            center: [-113.49856196994591,53.540920434717556], // starting position [lng, lat]
            zoom: 9.2, // starting zoom
            style: 'mapbox://styles/mapbox/streets-v9',
            preserveDrawingBuffer: true
        });

        function filterMapWard() {
            const wardInput = document.getElementById('wardList') // get input from the DOM
            const wardValue = wardInput.value
            filterMap('wards-layer', 'name_1', wardValue)
            filterMap('wards-layer-outline', 'name_1', wardValue)
            var features = map.querySourceFeatures('wards', {
                sourceLayer: 'wards-layer',
                filter: ["==", "name_1", wardValue]
            });
            // var layer = map.getLayer('wards-layer')
            // data_source = map.getSource('wards')
            //console.log(data_source.tileBounds.bounds)
            map.flyTo({
                center: features[0].geometry.coordinates[0][0],
                zoom: 11,
            });

            

        }
        function filterMap(layer_name, property_name, values) {
            map.setFilter(layer_name, ['match', ['get', property_name], values, true, false]);
        }

        map.on('load', () => {
            map.addSource('wards', {
                type: 'geojson',
                // Can also use a URL for the value for the `data` property.
                data: 'backend/data_sets/Edmonton_wards.geojson'
            });
            
            map.addSource('routes', {
                type: 'geojson',
                data: 'backend/data_sets/ETS_routes.geojson'
            });

            map.addSource('stops', {
                type: 'geojson',
                data: 'backend/data_sets/ETS_stops.geojson'
            });

            map.addLayer({
                'id': 'wards-layer',
                'type': 'fill',
                'source': 'wards',
                'paint': {
                    'fill-color': {
                        type: 'identity',
                        property: 'color',
                    },
                    //'fill-opacity': 0.4
                }
            });

            map.addLayer({
                'id': 'wards-layer-outline',
                'type': 'line',
                'source': 'wards',
                'paint': {
                    'line-color': 'rgba(0, 0, 0, 1)',
                    'line-width': 2
                }
            });

            map.addLayer({
                'id': 'routes-layer',
                'type': 'line',
                'source': 'routes',
                'paint': {
                    'line-color': 'rgba(0, 0, 255, 1)',
                    'line-width': 1
                }
            });

            map.addLayer({
                'id': 'stops-layer',
                'type': 'circle',
                'source': 'stops',
                'paint': {
                    'circle-color': 'rgba(255, 0, 0, 1)'
                }
            });
            
            let layer_name = 'wards-layer';
            let property_name = 'name_2';
            //let values = ['Anirniq Ward', 'Dene Ward'];
            let values = [];

            filterMap(layer_name, property_name, values);
            filterMap('wards-layer-outline', property_name, values);
            filterMap('routes-layer', 'route_id', ['']);
            filterMap('stops-layer', 'stop_id', ['']);
            // const style = map.getStyle();
            // style.layers.find(({ id }) => id === "wards-layer").paint['fill-color']['type'] = 'identity';
            // style.layers.find(({ id }) => id === "wards-layer").paint['fill-color']['property'] = 'rgb(0, 255, 0)';
            // map.setStyle(style);
        });
        $('#downloadLink').click(function() {
        var img = map.getCanvas().toDataURL('image/png')
        this.href = img
        });
