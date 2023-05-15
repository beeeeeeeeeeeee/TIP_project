let map;
let featureLayer;
let infoWindow;
let results_center;
let circle;
let suburbCurrent;
let placeIDs
let exportButton;

var selected_placeid = new Array();
var distance_store = new Array();
var markers = new Array();

// load placeIDs.json
// source https://gist.github.com/randomecho/5020859
fetch("/static/suburb_finder/js/placeIDs.json")
  .then((response) => response.json())
  .then((data) => {
    placeIDs = new Array(data)[0];
  }
);

var lat = -37.840935;
var lng = 144.946457;

async function initMap() {
  
   map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: lat, lng: lng },
    zoom: 12,
    // In the cloud console, configure this Map ID with a style that enables the
    // "Locality" feature layer.
    mapId: "73b815e38b2c33a3", // <YOUR_MAP_ID_HERE>,

  });

  const {spherical} = await google.maps.importLibrary("geometry")

  // Autocomplete for suburb input.
  var suburbInput = document.getElementById("suburb");
  const options = {
    componentRestrictions: { country: "au" },
    fields: ["place_id", "geometry", "name"],
    strictBounds: false,
    types: ["locality", "postal_code"],
  };
  const autocomplete = new google.maps.places.Autocomplete(suburbInput, options);
  autocomplete.bindTo("bounds", map);

  // Autocomplete for origin input.
  var originInput = document.getElementById("origin");
  const options_origin = {
    componentRestrictions: { country: "au" },
    fields: ["place_id", "geometry", "name"],
    strictBounds: false,
    types: ["address"],
  };
  const autocomplete_origin = new google.maps.places.Autocomplete(originInput, options_origin);
  autocomplete_origin.bindTo("bounds", map);


  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");


  // Add the feature layer.
  //@ts-ignore
  featureLayer = map.getFeatureLayer("LOCALITY");
  // Add the event listener for the feature layer.
  featureLayer.addListener("click", handlePlaceClick);
  infoWindow = new google.maps.InfoWindow({});
  // Apply style on load, to enable clicking.
  applyStyleToSelected();


  // Add the event listener for the search button.
  const searchButton = document.getElementById("search");
  searchButton.addEventListener("click", () => {
    
    // clear previous circle
    if(typeof circle !== "undefined"){
      circle.setMap(null);  
    }
    
    // Get suburb from input.
    suburbInput = document.getElementById("suburb");
    var suburb = suburbInput.value;
    console.log(suburb);

    var suburb_arr = suburb.split(" ");
    var postal_code = Number(suburb_arr[suburb_arr.length - 1]);
    console.log("postal_code: ", postal_code);
    
    // Get the place details from suburb.
    var place_add = null;
    // Get the place detail from placeIDs.json
    if( placeIDs.some(item => item.name + ' ' + item.state === suburb )){
      place_add = placeIDs.filter(item => item.name + ' ' + item.state === suburb )[0];

      if ( selected_placeid.some(item => item.placeID === place_add.placeID) ) {
        // do nothing
      } else {
        selected_placeid.push(place_add);
        console.log("selected_placeid ", selected_placeid);
      }
      suburbCurrent = place_add;
    }
    
    if( placeIDs.some(item => item.postcode.includes(postal_code) )) {
      place_add = placeIDs.filter(item => item.postcode.includes(postal_code) )[0];
      selected_placeid.push(place_add);
      console.log("selected_placeid ", selected_placeid);
    }

    applyStyleToMultipleSelected(selected_placeid);
    updateResultsTable(selected_placeid);

    getElementById("suburb").value = "";
    getElementById("origin").value = "";

  });

  // Add circle to map based on radius
  const radiusInput = document.getElementById("radius");
  
  radiusInput.addEventListener("change", () => {
    var radius_km = radiusInput.value * 100;
    
    // clear previous circle
    if(typeof circle !== "undefined"){
    circle.setMap(null);
    }
    var results_center = {lat: suburbCurrent.lat, lng: suburbCurrent.lng};

    // add new circle
    circle = new google.maps.Circle({
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#FF0000",
      fillOpacity: 0.35,
      map,
      center: results_center,
      radius: radius_km,
    });

    // for each postcode, check if it is within the circle
    var places_inrange = new Array();
    for (var i = 0; i < placeIDs.length; i++) {
      var place = placeIDs[i];
      var place_location = new google.maps.LatLng(place.lat, place.lng);
      if (google.maps.geometry.spherical.computeDistanceBetween(results_center, place_location) <= radius_km*1) {
        places_inrange.push(place);
        if ( selected_placeid.some(item => item.placeID === place.placeID) ) {
          // do nothing
        } else {
          selected_placeid.push(place);
        }
      }
    }

    applyStyleToMultipleSelected(selected_placeid);

    // update results_table
    updateResultsTable(selected_placeid);

  });

  // event listener for clear button
const clearButton = document.getElementById("clear_button");
clearButton.addEventListener("click", () => {
  console.log("clear button clicked");
  clearAll();
  });

  exportButton = document.getElementById("export_csv");
  exportButton.addEventListener("click", export_csv);

}


// Handle the click event.
function handlePlaceClick(event) {
  let feature = event.features[0];
  console.log('feature: ', feature);
  console.log('event: ', event);
  if (!feature.placeId) return;

  // clear previous circle
  if(typeof circle !== "undefined"){
    circle.setMap(null);  
  }

  //const place = await feature.fetchPlace();

  var clicked_placeid = feature.placeId;

  // if placeid is already in json, remove it
  if ( selected_placeid.some(item => item.placeID === clicked_placeid) ) {
    // remove place from object
    selected_placeid = selected_placeid.filter(item => item.placeID !== feature.placeId);
    applyStyleToMultipleSelected(selected_placeid);
    updateResultsTable(selected_placeid);
    suburbCurrent = null;
  } else {
    var place_add = null;
    // Get the place detail from placeIDs.json
    if( placeIDs.some(item => item.placeID === clicked_placeid )){
      place_add = placeIDs.filter(item => item.placeID === clicked_placeid)[0];
      selected_placeid.push(place_add);
      console.log("place_add ", place_add);

      suburbCurrent = place_add;
    }

    applyStyleToMultipleSelected(selected_placeid);
    updateResultsTable(selected_placeid);
  }

}


// Stroke and fill with minimum opacity value.
//@ts-ignore
const styleDefault = {
  strokeColor: "#810FCB",
  strokeOpacity: 1.0,
  strokeWeight: 2.0,
  fillColor: "white",
  fillOpacity: 0.1, // Polygons must be visible to receive click events.
};

// Style for the clicked Administrative Area Level 2 polygon.
//@ts-ignore
const styleClicked = {
  ...styleDefault,
  fillColor: "#810FCB",
  fillOpacity: 0.5,
};

// Apply styles to the map.
function applyStyleToSelected(placeid) {
  // Apply styles to the feature layer.
  featureLayer.style = (options) => {
    // Style fill and stroke for a polygon.
    if (placeid && options.feature.placeId == placeid) {
      return styleClicked;
    }
    // Style only the stroke for the entire feature type.
    return styleDefault;
  };
}

// Apply styles to multiple features.
function applyStyleToMultipleSelected(placeids) {
  // Apply styles to the feature layer.
  featureLayer.style = (options) => {

    for( var i = 0; i < placeids.length; i++){ 
      if ( placeids[i].placeID === options.feature.placeId) { 
        return styleClicked;
      }
    }

    // Style fill and stroke for a polygon.
    if (placeids.includes(options.feature.placeId)) {
      return styleClicked;
    }
    // Style only the stroke for the entire feature type.
    return styleDefault;
  };

}

// Helper function to create an info window.
function updateInfoWindow(content, center) {
  infoWindow.setContent(content);
  infoWindow.setPosition(center);
  infoWindow.open({
    map,
    shouldFocus: false,
  });
}

// update radius value
function updateRadiusValue(val) {
  radius = val/10; // convert to float 0.1 to 25 km
  document.getElementById("radius_value").innerHTML = radius + " km";
}

// clear all selected places
function clearAll() {

  // clear selected places
  selected_placeid = Array();
  console.log(selected_placeid);

  // clear suburb currently selected
  suburbCurrent = null;

  // clear markers
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }

  // clear existing radius circle
  if(typeof circle !== "undefined"){
    circle.setMap(null);  
  }
  
  // clear search inputs
  var originInput = document.getElementById("origin");
  originInput.value = "";

  var suburbInput = document.getElementById("suburb");
  suburbInput.value = "";

  // reload suburb data removing distance and travel time data
  fetch("/static/suburb_finder/js/placeIDs.json")
  .then((response) => response.json())
  .then((data) => {
    placeIDs = new Array(data)[0];
  });

  applyStyleToMultipleSelected(selected_placeid);
  updateResultsTable(selected_placeid);

}

function updateResultsTable(selected_placeid) {
  var table = document.getElementById("results_table");
  table.innerHTML = "";

  var originInput = document.getElementById("origin");
  if (originInput.value) {   
    calculateDistance(originInput.value, selected_placeid);
    addMarker(originInput.value);

  } else {
    buildResultsTable(selected_placeid);
  }
}

function buildResultsTable(selected_placeid) {

  // clear table
  var table = document.getElementById("results_table");
  table.innerHTML = ``; 

  if(selected_placeid){
    // order by travel time
    selected_placeid.sort(function(a, b) {
      return parseFloat(a.travelTimeValue) - parseFloat(b.travelTimeValue);
    });

    for (var i = 0; i < selected_placeid.length; i++) {
      var place = selected_placeid[i];
      var row = table.insertRow(i);
      
      var cell1 = row.insertCell(0);
      cell1.innerHTML = place.name;
      
      var cell2 = row.insertCell(1);
      const num_pc = place.postcode.length;
      if(num_pc > 1){
        min = Math.min(place.postcode.length, 4);
        cell2.innerHTML = `${place.postcode.slice(0, min).join(", ")}`;
      } else {
        cell2.innerHTML = place.postcode[0];
      }
      var cell3 = row.insertCell(2);
      cell3.innerHTML = place.distance;
      
      var cell4 = row.insertCell(3);
      cell4.innerHTML = place.travelTime;
    }
  }
  
}

function calculateDistance(origin, selected_placeid) {
  // Array of selected_placeid.name
  console.log("placeids: ", selected_placeid);
  var destination = [];
  for (var i = 0; i < selected_placeid.length; i++) {
    destination.push(selected_placeid[i].name + ", " + selected_placeid[i].state);
  }
  console.log("destination", destination);

  var service = new google.maps.DistanceMatrixService();
  service.getDistanceMatrix(
    { origins: [origin],
      destinations: destination,
      travelMode: "DRIVING",
      unitSystem: google.maps.UnitSystem.METRIC,
    }, 
    (response, status) => {
      if (status !== "OK") {
        alert("Error was: " + status);
      } else {
        distance_store = Array();
        var origins = response.originAddresses;
        var destinations = response.destinationAddresses;

        for (var i = 0; i < origins.length; i++) {
          var results = response.rows[i].elements;
          for (var j = 0; j < results.length; j++) {
            var element = results[j];
            console.log("element", element);
            console.log("element.distance", element.distance);
            var distance = element.distance.text;
            var duration = element.duration.text;
            var duration_value = element.duration.value;
            var from = origins[i];
            var to = destinations[j];
            
            selected_placeid[j].distance = distance;
            selected_placeid[j].travelTime = duration;
            selected_placeid[j].travelTimeValue = duration_value;

            buildResultsTable(selected_placeid);
          }
        }
        console.log("calc dist return: ", selected_placeid);
        return selected_placeid;
      }
    }
  );
}

function addMarker(origin_address) {
  
  console.log("markers: ", markers);

  // clear markers
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }

  // geo code origin address
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: origin_address }, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      var origin = results[0].geometry.location;
      console.log("origin", origin);
      marker = new google.maps.Marker({
        position: origin,
        map: map,
        title: origin_address,
      });
      markers.push(marker);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}

  
function export_csv() {
  console.log("exporting to csv");
  var csv = "Name, Postcode, Distance, Travel Time\n";
  selected_placeid.forEach(function(row) {
    csv += row.name + "," + row.postcode + "," + row.distance + "," + row.travelTime + "\n";
  });
  
  console.log(csv);
  
  var hiddenElement = document.createElement('a');
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
  hiddenElement.target = '_blank';
  hiddenElement.download = 'suburb_finder_results.csv';
  hiddenElement.click();
};

// repostion map to include all markers
function repositionMap() {
  var bounds = new google.maps.LatLngBounds();
  for (var i = 0; i < markers.length; i++) {
    bounds.extend(markers[i].getPosition());
  }
  map.fitBounds(bounds);
}

// init onload functions
function init() {
  
}

window.onload = init;

window.initMap = initMap;
window.updateRadiusValue = updateRadiusValue;