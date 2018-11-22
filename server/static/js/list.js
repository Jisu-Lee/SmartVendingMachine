var list = [[1, "cosmetic 1", 11037, 3.4, null, true],
      [2, "cosmetic 2", 11037, 3.4, null,  false],
      [3, "cosmetic 3", 11037, 3.4, null,  true]];

var user_id = 1;  //로그인한 사용자에 따하 바뀌도록
function addDynamicCosmetic(NO, name, price, score, type, fav_flag){
  var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a class="rate"><img src="/static/images/'+NO+'.jpg") }}" alt="cosmetic img" class="img-responsive"><h3 class="fh5co-work-title">'+name+'</h3>$'+price+'</a><span class="fa fa-star " id="cos'+NO+'" style="float: right">'+' '+score+'</span></div>';
  $(".data").append(template);
  if(fav_flag == true){
    $('#cos'+NO).css("color", "orange");
  }
};



$(document).ready(function() {

  $(document).on('click', '.fa-star', function (e) {
          //e.stopPropagation();
          var cosmetic_id = this.id; //cosmetic id
          cosmetic_id = parseInt(cosmetic_id.replace("cos", ""));
          var myObj = new Object();

          if($('#'+this.id).css("color") == "rgb(255, 165, 0)"){
            //favorite cancle
            $('#'+this.id).css("color", "gray");
          var data = [user_id, cosmetic_id, false];  //id = userID, data = cosmeticID
          }else{
              //favorite
              $('#'+this.id).css("color", "orange");
              var data = [user_id, cosmetic_id, true];  //id = userID, data = cosmeticID
          }

          myObj.data = data;
          var jsonText =  JSON.stringify(myObj);
          console.log(jsonText);
          $.ajax({
                  url: '/list',
                  data: jsonText,
                  type: 'POST',
                  dataType: "json",
                  contentType: 'application/json;charset=UTF-8',
                  success: function(response) {
                      console.log(response);
                  },
                  error: function(error) {
                      console.log(error);
                  }
              });

      });


addDynamicCosmetic(1, "cosmetic 1", 11037, 3.4, null, true);
addDynamicCosmetic(2, "cosmetic 2", 11037, 3.4, null,  false);
addDynamicCosmetic(3, "cosmetic 3", 11037, 3.4, null,  true);
});
