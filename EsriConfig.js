require([
  "esri/Map",
  "esri/layers/GeoJSONLayer",
  "esri/views/SceneView",
  "esri/core/watchUtils"
  ],

  function (Map, GeoJSONLayer, SceneView, watchUtils) {

    var UniWebStyle = {
      type: "web-style",
      name: "Pushpin 3",
      portal: { url: "https://www.arcgis.com" },
      styleName: "EsriIconsStyle",
    };

    //Pinned Locations Icon to override the default renderer of GeoJSON Layer
    const myRenderer = {
      type: "simple",
      field: "ObjectID",
      symbol: UniWebStyle,
      visualVariables: [
        {
          type: "color",
          field: "IconColorID",
          stops: [
            {
              value: 1,
              color: "#E8666C"
            },
            {
              value: 2,
              color: "#fee440"
            }
          ]
        },{
          type: "size",
          field: "ObjectID",
          stops: [
            {
              value: 1,
              size: 25
            },
            {
              value: 2,
              size: 25
            }
          ]
        }
      ]
    };

    const myPopuptemplate = {
      title: "{Title}",
      content: [
        { 
          type: "text",
          text: "{City}" 
        }, 
        {
          type: "media",
          mediaInfos:
          {
            type: "image",
            value: {
              sourceURL: "{url}"
            }
          }
        }
    ]
    };

    const url_Pro = "https://aytuncilhan.github.io/ProfessionalLocations.geojson";
    //The layer accomodates the geographic info, graphics, and popup style
    var geojsonLayer = new GeoJSONLayer({
      url: url_Pro,
      popupTemplate: myPopuptemplate,
      renderer: myRenderer
    });

    const url_Leisure = "https://aytuncilhan.github.io/LeisureLocations.geojson";
    //The layer accomodates the geographic info, graphics, and popup style
    var LeisureLayer = new GeoJSONLayer({
      url: url_Leisure,
      popupTemplate: myPopuptemplate,
      renderer: myRenderer
    });

    // Initialize the Map
    var map = new Map({
      basemap: "satellite",
      layers: [geojsonLayer, LeisureLayer]
    });

    // Creating the SceneView instance to display the 3D globe
    var view = new SceneView({
      container: "viewDiv", // Reference to the DOM node that will contain the view
      map: map, // Reference to the created map object
      scale: 50000000, // Sets the initial scale to 1:50,000,000
      center: [14, 42], // Sets the center point of view with lon/lat

      popup: {
        dockEnabled: true,
        dockOptions: {
          position: "top-right",
          breakpoint: false,
          buttonEnabled: false
        },
        collapseEnabled: false
      },

      highlightOptions: {
        color: [255, 255, 255],
        haloOpacity: 0.8
      }
    });

    $("#toggle-event1").on('change', function() {
      if ($(this).is(':checked')) {
        geojsonLayer.visible = true;
      }
      else {
        geojsonLayer.visible = false;
      }
    });

    $("#toggle-event2").on('change', function() {
      if ($(this).is(':checked')) {
        LeisureLayer.visible = true;
      }
      else {
        LeisureLayer.visible = false;
      }
    });

    //Wait until the layer is loaded to display the Panel
    watchUtils.whenTrue(LeisureLayer, "loaded", function() {
      console.log("Changed to " + LeisureLayer.loadStatus);
      $('#leftPane').show()
    });
    
  }
  
);

