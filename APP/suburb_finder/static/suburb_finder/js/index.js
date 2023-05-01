let map;
let featureLayer;
let infoWindow;
let results_center;
let circle;
let suburbCurrent;
var placeid_list = new Array();
let vicPostcodes

console.log(placeid_list)

// load vicPostcodes.json
// source https://gist.github.com/randomecho/5020859
fetch("/static/suburb_finder/js/vicPostcode.json")
  .then((response) => response.json())
  .then((data) => {
    vicPostcodes = new Array(data);
    console.log(vicPostcodes[0][0]);
  });

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
    types: ["(regions)"],
  };
  const autocomplete = new google.maps.places.Autocomplete(suburbInput, options);
  autocomplete.bindTo("bounds", map);


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
    // Get the place details from suburb.
    const request = {
      query: suburb,
      fields: ["place_id", "geometry", "name"],
    };

    const service = new google.maps.places.PlacesService(map);
    service.findPlaceFromQuery(request, (results, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        console.log(results)
        suburbCurrent = results[0];
        // Get the place ID from the results.
        const placeId = results[0].place_id;
        
        // Apply the style to the feature layer.
        applyStyleToSelected(placeId);     
      }
    });

  });

  // Add circle to map based on radius
  const radiusInput = document.getElementById("radius");
  
  radiusInput.addEventListener("change", () => {
    var radius_km = radiusInput.value * 100;
    
    // clear previous circle
    if(typeof circle !== "undefined"){
    circle.setMap(null);
    }
    var results_center = suburbCurrent.geometry.location;
    console.log(results_center);

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
    var postcode_list = new Array();
    for (var i = 0; i < vicPostcodes[0].length; i++) {
      var postcode = vicPostcodes[0][i];
      var postcode_center = new google.maps.LatLng(postcode.lat, postcode.lng);
      if (google.maps.geometry.spherical.computeDistanceBetween(results_center, postcode_center) <= radius_km*1) {
        postcode_list.push(postcode.suburb);
      }
    }

    console.log("postcode_list", postcode_list);

    updatePlaceidList(postcode_list);


  });
}

// update placeid_list
function updatePlaceidList(postcode_list) {
  for (var i = 0; i < postcode_list[0].length; i++) {

    suburb = postcode_list[0][i];

    // Get the place details from suburb.
    const request = {
      query: suburb,
      fields: ["place_id"],
    };

    const service = new google.maps.places.PlacesService(map);
    service.findPlaceFromQuery(request, (results, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        // Get the place ID from the results.
        const placeId = results[0].place_id;
        placeid_list.push(placeId);
      }
    });
  }
  console.log("placeid_list_radius", placeid_list);

  applyStyleToMultipleSelected(placeid_list);

}


// Handle the click event.
async function handlePlaceClick(event) {
  let feature = event.features[0];
  if (!feature.placeId) return;

  // clear previous circle
  if(typeof circle !== "undefined"){
    circle.setMap(null);  
  }

  // Apply the style to the feature layer.
  //applyStyleToSelected(feature.placeId);

  // if placeid is already in list, remove it
  if ( placeid_list.includes(feature.placeId) ) {
    var index = placeid_list.indexOf(feature.placeId);
    if (index > -1) {
      placeid_list.splice(index, 1);
      applyStyleToMultipleSelected(placeid_list);
    }
    suburbCurrent = null;
  } else {
    // Add placeid to list
    placeid_list.push(feature.placeId);
    applyStyleToMultipleSelected(placeid_list);
    console.log("placeid_list_click", placeid_list);
  

    const place = await feature.fetchPlace();
    // Get the place details from suburb.
    const request = {
      query: place.displayName,
      fields: ["geometry", "name"],
    };
    
    const service = new google.maps.places.PlacesService(map);
    service.findPlaceFromQuery(request, (results, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        console.log(results)
        suburbCurrent = results[0];
        // Get the place ID from the results.
        const placeId = feature.placeId;
            
        // Apply the style to the feature layer.
        //applyStyleToSelected(placeId);
      }
    });
  

  // Add the info window.
  
  // console.log(place);
  let content =
    '<span style="font-size:small">Display name: ' +
    place.displayName +
    "<br/> Place ID: " +
    feature.placeId +
    "<br/> Feature type: " +
    feature.featureType +
    "</span>";

  //updateInfoWindow(content, event.latLng);
  
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
  placeid_list = Array();
  console.log(placeid_list);
  applyStyleToMultipleSelected(placeid_list);
  suburbCurrent = null;
  if(typeof circle !== "undefined"){
    circle.setMap(null);  
  }
}

// init onload functions
function init() {

}

var val = document.getElementById("radius").value;
updateRadiusValue(val);

// event listener for clear button
const clearButton = document.getElementById("clear");
clearButton.addEventListener("click", () => {
  clearAll();
});

window.onload = init;

window.initMap = initMap;
window.updateRadiusValue = updateRadiusValue;
