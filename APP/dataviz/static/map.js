class MapViz {
    constructor(map) {
      // bindings
      this.loadConfig = this.loadConfig.bind(this)
      this.get_data = this.get_data.bind(this)
      this.vizStyle = this.vizStyle.bind(this)
      this.configPolling = this.configPolling.bind(this)
      //init stuffs
      this.map = map;
      this.config = JSON.parse(Cookies.get('map_config'))
      this.colorScaler = d3.scaleSequential().domain([0,20]).interpolator(d3.interpolateMagma);
      this.geo_data = null;
      // this.agg_data = null;
      this.get_data().then((result) => {
        this.geo_data = result;
        
        // this.agg_data = result["agg_data"];
        this.map.data.addGeoJson(this.geo_data);
        var max_value = d3.max(this.geo_data.features, d => d.properties.value)
        this.colorScaler = d3.scaleSequential().domain([0,max_value]).interpolator(d3.interpolateMagma);
        this.map.data.setStyle(this.vizStyle);
      })
  
      this.styleDefault = {
        strokeColor: "#f00",
        strokeOpacity: 0,
        strokeWeight: 0,
        fillOpacity: 0.7,
        clickable: true
      };
      this.styleClicked = {
        ...this.styleDefault,
        // fillColor: "#810FCB",
        fillOpacity: 0.9,
        strokeWeight: 1,
        strokeOpacity: 1,
      };
      this.configPolling()
  
      // this.map.data.setStyle(this.vizStyle);
    }
    loadConfig() {
      this.config = JSON.parse(Cookies.get('map_config'))
    }
    vizStyle(feature) {
        // var partition = feature.getProperty('partition');
        // var value = this.agg_data["value"][partition]
        var value = feature.getProperty('value')
        var color = this.colorScaler(value)
        feature.setProperty('color', color);
        var fillOpacity = this.config["config_opacity"]
        var strokeOpacity = this.styleDefault["strokeOpacity"]
        var clickable = true
        if (value <= 0 || value === undefined) {
          color = 'none'
          fillOpacity = 0.0
          strokeOpacity = 0
          clickable = false
        }
  
        return {
          ...this.styleDefault,
          fillColor: color,
          fillOpacity: fillOpacity,
          strokeOpacity: strokeOpacity,
          clickable: clickable
  
        };
      
    }
    async get_data() {
  
    
  
      
      const size = this.config["btnradio"]
      console.log("fetching",size);
      const result = await $.ajax({
        url: "http://localhost:8080/heatmaps?size="+size+"&data=true&map=true",
        crossDomain: true,
        dataType: 'json',
        async: true,
        success: function (data) {
          console.log("fetched",size);
          return data;
        },
        error: function (xhr, status) {
          alert("error" + status);
        }
      })
      // this.data = result;
      this.geo_data = result;
      // this.agg_data = result["agg_data"];
      return result;
    }
    configPolling() {
      setInterval(() => {
        var old_config = this.config;
        // console.log("old",JSON.stringify(old_config));
  
        this.loadConfig();
        // console.log("new",JSON.stringify(this.config));
  
        // console.log("comp",JSON.stringify(old_config) !== JSON.stringify(this.config));
        if (!_.isEqual(old_config,this.config)) {
  
          this.map.data.setStyle(this.vizStyle);
          
          this.map.setCenter({
            lat: parseFloat(this.config["config_lat"]),
            lng: parseFloat(this.config["config_long"])
          });
          console.log("yo setting center");
  
          if(old_config["btnradio"] != this.config["btnradio"]){
            //fetch new data
            this.get_data().then((result) => {
              this.geo_data = result;
              // this.agg_data = result["agg_data"];
              map.data.forEach(function(feature) {
                  map.data.remove(feature);
              });
              var max_value = d3.max(this.geo_data.features, d => d.properties.value)
              this.colorScaler = d3.scaleSequential().domain([0,max_value]).interpolator(d3.interpolateMagma);
              this.map.data.addGeoJson(this.geo_data);
              this.map.data.setStyle(this.vizStyle);

            })
  
          }
          
        }
        
      }, 1000);
    }
  }
  
  
  window.MapViz = MapViz;