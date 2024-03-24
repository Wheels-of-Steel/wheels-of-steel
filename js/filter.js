function getStopsByRoutes(routes) {
    return fetch("./ETS_routes_stops.json")
        .then((res) => {
            if (!res.ok) {
                throw new Error
                    (`HTTP error! Status: ${res.status}`);
            }
            return res.json();
        })
        .then((data) => {
            console.log(data[0]);

            let stopArray = [];
            for (let i = 0; i < data.length; i++ )  {
                if ( routes.includes(data[i].route_id) ) {
                    stopArray.push(data[i].stop_id);
                }
            }
            // console.log(stopArray);
            return stopArray;
        })
        .catch((error) => 
               console.error("Unable to fetch data:", error));
        
    }