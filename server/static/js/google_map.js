latitude = 37.5031256;
longitude = 126.9570334;
/*
var rec_name = ["mascara", "AC cream", ...]
var data = [
  [1, ["skinA", 4], ["lotionA", 1], ["sunblockA", 2]],
  [2, ["skinB", 5], ["lotionB", 2]],
  [3, ["skinC", 6], ["lotionC", 3], ["sunblockC", 5]],
  [4, ["skinD", 7], ["lotionD", 4]],
  [5, ["skinE", 8], ["lotionE", 5], ["sunblockE", 6]]
];
var locations = [
     [1, 'CAU UNIV', 37.507126, 126.958049, "address1"],
     [2, 'HeukSeok Subway', 37.508871, 126.963532, "address2"],
     [3, 'Sangdo Subway', 37.502940, 126.947820, "address3"],
     [4, 'Soongsil UNIV', 37.496335, 126.957390, "address4"],
     [5, 'JangSeongBaegi Subway', 37.504847, 126.939065, "address5"]
   ];
*/
function addLocation(lat, lng){

     var map = new google.maps.Map(document.getElementById('map'), {
       zoom: 15,
       center: new google.maps.LatLng(lat, lng),
       mapTypeId: google.maps.MapTypeId.ROADMAP
     });
infoWindow = new google.maps.InfoWindow;

     if (navigator.geolocation) {

          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            console.log(pos);
            infoWindow.setPosition(pos);
            infoWindow.setContent('You&apos;re in here.');
            infoWindow.open(map);
            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }


     var infowindow = new google.maps.InfoWindow();

     var marker, i;


     var idx = getNearestMachine(latitude, longitude, locations);
     var pinColor = "4286f4";
    var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
        new google.maps.Size(21, 34),
        new google.maps.Point(0,0),
        new google.maps.Point(10, 34));
    var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
        new google.maps.Size(40, 37),
        new google.maps.Point(0, 0),
        new google.maps.Point(12, 35));

     for (i = 0; i < locations.length; i++) {
       if(i == idx){
         marker = new google.maps.Marker({
                position: new google.maps.LatLng(locations[i][2], locations[i][3]),
                map: map,
                icon: pinImage,
                shadow: pinShadow
            });
       }
       else{
         marker = new google.maps.Marker({
           position: new google.maps.LatLng(locations[i][2], locations[i][3]),
           map: map
         });
        }
       google.maps.event.addListener(marker, 'click', (function(marker, i) {
         return function() {
           infowindow.setContent(locations[i][1]);
           infowindow.open(map, marker);
           setModalData(i+1);
           var modal = document.getElementById('myModal');
           // Get the <span> element that closes the modal
           var span = document.getElementsByClassName("close")[0];
           modal.style.display = "block";
           // When the user clicks the button, open the modal
           // When the user clicks on <span> (x), close the modal
           span.onclick = function() {
               $("#modal_data").remove();
               modal.style.display = "none";
           }

           // When the user clicks anywhere outside of the modal, close it
           window.onclick = function(event) {
               if (event.target == modal) {
                   $("#modal_data").remove();
                   modal.style.display = "none";
               }
           }
         }
       })(marker, i));
     }
}



function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }




function addLocationData(locations){

  for(var i=0; i<locations.length; i++){
    var template ='<div class="row"><div class="col-md-4"><div class="fh5co-feature fh5co-feature-sm " ><div class="fh5co-icon"><i class="icon-envelope-o"></i></div><div class="fh5co-text"><p><a href="#">'+locations[i][1]+'</a></p></div></div></div><div class="col-md-4"><div class="fh5co-feature fh5co-feature-sm " ><div class="fh5co-icon"><i class="icon-map-o"></i></div><div class="fh5co-text"><p>'+locations[i][4]+'</p></div></div></div></div>';
    $("#data").append(template);
  }

};

function getNearestMachine(lat, lng, locations){

  var min = 9876543210;
  var min_index = 0;
  for(var i=0; i<locations.length; i++){
    var temp_lat = locations[i][2] - lat;
    var temp_lng = locations[i][3] - lng;
    var length  = temp_lat * temp_lat + temp_lng * temp_lng;
    console.log(length);
    if(min >= length){
      min = length;
      min_index = i;
    }
  }
  return min_index;
}

function setModalData(NO){
  $('[name="table_data"]').empty();

  for(var i=0; i<data.length; i++){
    if(data[i][0] == NO){
      $('.modal-content').prepend('<br><h2 style="text-align: center">Stock in '+locations[i][1]+'</h2>');

      for(var j=1; j<data[i].length; j++){
        var template='<tr><th scope="row">'+j+'</th><td style="background-color:#c0cee2">'+data[i][j][0]+'</td><td>'+data[i][j][1]+'</td></tr>';
        $('[name="table_data"]').append(template);
      }

    }
  }



}


$(document).ready(function(e) {
    //initMap();
    //multiple location


    addLocation(latitude, longitude);
    addLocationData(locations);

});
