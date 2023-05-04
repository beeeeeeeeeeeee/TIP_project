// get json from url "http://127.0.0.1:8000/heatmaps?size=1&data=true&map=true"
//

function initMapConfig(){
    var map_config = $("#map_config");
    var elem_map_config = document.getElementById("map_config");
    // #check if cookie exists
    var config = Cookies.get('map_config');
    console.log("map_config",config);
    if(config == undefined){
        // set form values from cookie
        config = {
            "config_lat": "-37.8362108",
            "config_long": "144.9948872",
            "config_opacity": "0.5",
            "btnradio": "3"
        }
        Cookies.set('map_config',JSON.stringify(config))
    }else{
        config = JSON.parse(config);

    }
    map_config.find("#config_lat").val(config["config_lat"]);
    map_config.find("#config_long").val(config["config_long"]);
    map_config.find("#config_opacity").val(config["config_opacity"]);
    map_config.find("#btnradio"+config["btnradio"]).prop("checked",true);
    map_config.submit(configSubmitListener);

    elem_map_config.addEventListener("reset", configResetListener);
}
function configSubmitListener(event){
    event.preventDefault();
    console.log("clicked");

    var map_config = $("#map_config");
    var config = {
        "config_lat": map_config.find("#config_lat").val(),
        "config_long": map_config.find("#config_long").val(),
        "config_opacity": map_config.find("#config_opacity").val(),
        "btnradio": map_config.find("input[name='btnradio']:checked").val()
    }
    Cookies.set('map_config',JSON.stringify(config));
    console.log("map_config",
        JSON.parse(Cookies.get('map_config'))
    );
}
function configResetListener(event){
    event.preventDefault();
    console.log("clicked");
    // #remove cookie
    Cookies.remove('map_config');


    initMapConfig();
}
window.initMapConfig = initMapConfig;