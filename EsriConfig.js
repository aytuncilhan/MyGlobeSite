require([
  "esri/Map",
  "esri/layers/GeoJSONLayer",
  "esri/views/SceneView"
  ],

  function (Map, GeoJSONLayer, SceneView) {

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
              color: "black"
            },
            {
              value: 2,
              color: "yellow"
            }
          ]
        },{
          type: "size",
          field: "ObjectID",
          stops: [
            {
              value: 1,
              size: 20
            },
            {
              value: 2,
              size: 20
            }
          ]
        }
      ]
    };

    const url = "https://aytuncilhan.github.io/PinnedLocations.geojson";
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

    //The layer accomodates the geographic info, graphics, and popup style
    var geojsonLayer = new GeoJSONLayer({
      url: url,
      popupTemplate: myPopuptemplate,
      renderer: myRenderer
    });

    // Initialize the Map
    var map = new Map({
      basemap: "satellite",
      layers: [geojsonLayer]
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

  }

);
