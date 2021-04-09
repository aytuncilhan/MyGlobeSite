require([
  "esri/Map",
  "esri/layers/GeoJSONLayer",
  "esri/views/SceneView",
  "esri/core/watchUtils",
  "esri/geometry/Point"
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
          field: "PinColorID",
          stops: [
            {
              //Education
              value: 1,
              color: "#E8666C"
            },
            {
              //Journeys
              value: 2,
              color: "#fee440"
            },
            {
              //Professional
              value: 3,
              color: "#18191a"
            }
          ]
        },{
          type: "size",
          field: "PinSizeID",
          stops: [
            {
              value: 1,
              size: 25
            },
            {
              value: 2,
              size: 20
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
          text: "{Desc}" 
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

    const url_Academic = "https://aytuncilhan.github.io/Assets/GEOJSON/AcademicalLocations.geojson";
    //The layer accomodates the geographic info, graphics, and popup style
    var academicLayer = new GeoJSONLayer({
      url: url_Academic,
      popupTemplate: myPopuptemplate,
      renderer: myRenderer
    });

    const url_Pro = "https://aytuncilhan.github.io/Assets/GEOJSON/ProfessionalLocations.geojson";
    //The layer accomodates the geographic info, graphics, and popup style
    var geojsonLayer = new GeoJSONLayer({
      url: url_Pro,
      popupTemplate: myPopuptemplate,
      renderer: myRenderer
    });

    const url_Leisure = "https://aytuncilhan.github.io/Assets/GEOJSON/LeisureLocations.geojson";
    //The layer accomodates the geographic info, graphics, and popup style
    var LeisureLayer = new GeoJSONLayer({
      url: url_Leisure,
      popupTemplate: myPopuptemplate,
      renderer: myRenderer
    });

    // Initialize the Map
    var map = new Map({
      basemap: "satellite",
      layers: [geojsonLayer, academicLayer, LeisureLayer]
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
        collapseEnabled: true
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

    $("#toggle-event3").on('change', function() {
      if ($(this).is(':checked')) {
        academicLayer.visible = true;
      }
      else {
        academicLayer.visible = false;
      }
    });



    //Wait until the layer is loaded to display the Panel
    watchUtils.whenTrue(LeisureLayer, "loaded", function() {
      console.log("Layer Load Status: " + LeisureLayer.loadStatus);
      $('#leftPane').show();
      $('#togglePane').show();
    
      setTimeout(function() {

        //console.log('Popup Lat: ' + view.popup.location.latitude + ', Popup Lon: ' + view.popup.location.longitude);
        //console.log('Point Lat: ' + pointpopup.latitude + ', Point Lon: ' + pointpopup.longitude);
        //geojsonLayer.queryFeatures().then(res => {console.log('Popup Content: ' + res.features[0].symbol ) } ); 
        //view.popup.fetchFeatures({x:2, y:50}).then(res => {console.log('Fetched Res: ' + res ) } ); 
        console.log('Popup opened!');
      }, 5000);
      
    });


    //Log
    watchUtils.whenTrue(LeisureLayer, "not-loaded", function() {
      console.log("Layer Load Status: " + LeisureLayer.loadStatus);
    });
    watchUtils.whenTrue(LeisureLayer, "loading", function() {
      console.log("Layer Load Status: " + LeisureLayer.loadStatus);
    });
    watchUtils.whenTrue(LeisureLayer, "failed", function() {
      console.log("Layer Load Status: " + LeisureLayer.loadStatus);
    });

    //Delete the "Zoom To" box from the popup
    view.popup.actions = [];
    
    //Display the contents of the actions
    var count=0;
    if (view.popup.actions.length > 0) {
      view.popup.actions.forEach(element => {
        console.log("Item " + count + " : " + element.id );
        count++;
    });
    }
    else{
      console.log("There are no action items for the popup! Actions array length : " + view.popup.actions.length);
    }
    /*
    //End of function.
    setTimeout(function() {
            //Open Popup at defined point
            view.popup.open({
              title: 'hi there',
              location: p1,
              fetchFeatures: true
            });
          }, 10000);*/

              //Define point to open popup1
              var p1 = {
                type: "point", // autocasts as new Point()
                longitude: 2,
                latitude: 50
              };
            

            view.popup.autoOpenEnabled = false;
            view.on("click", function(event) {
              // Get the coordinates of the click on the view
              // around the decimals to 3 decimals
              var lat = Math.round(event.mapPoint.latitude * 1000) / 1000;
              var lon = Math.round(event.mapPoint.longitude * 1000) / 1000;

            view.popup.open({
              // Set the popup's title to the coordinates of the clicked location
              location: p1, // Set the location of the popup to the clicked location
              fetchFeatures: true,
              visible: true
            });
            console.log('Popup Lat: ' + lat + ', Popup Lon: ' + lon);

});



  }
  
);

