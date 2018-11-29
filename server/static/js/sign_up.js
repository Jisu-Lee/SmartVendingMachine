(function($) {

    $(".toggle-password").click(function() {

        $(this).toggleClass("zmdi-eye zmdi-eye-off");
        var input = $($(this).attr("toggle"));
        if (input.attr("type") == "password") {
          input.attr("type", "text");
        } else {
          input.attr("type", "password");
        }
      });
      $(".re-toggle-password").click(function() {
alert("ss");
          $(this).toggleClass("zmdi-eye zmdi-eye-off");
          var input = $($('this').attr("toggle"));
          if (input.attr("type") == "password") {
            input.attr("type", "text");
          } else {
            input.attr("type", "password");
          }
        });

    var submitAction = function() {
	/* do something with Error */
  if($('#password').val() == $('#re_password').val()) {
    var myObj = new Object();

    var name = $('#name').val();
    var skin_type = $('#skin_type').val();
    var birth_year = $('#birth_year').val();
    var gender = $('#gender').val();
    var password = $('#password').val();
    //alert(user_id+"/"+cosmetic_id+"/-1");
    //alert("favorite cancel");

    var data = [name, skin_type, birth_year, gender, password];  //id = userID, data = cosmeticID
    myObj.data = data;
    var jsonText =  JSON.stringify(myObj);
    console.log(jsonText);
    $.ajax({
                        url: '/signup',
                        data: jsonText,
                        type: 'POST',
                        dataType: "json",
                        contentType: 'application/json;charset=UTF-8',
                        success: function(response) {
                            console.log(response);
                            if(reponse["status"] == "ok"){
                            $('#cos'+cosmetic_id).css("color", "gray");
                            window.location.href='https://wannagraduate-220706.appspot.com/login'
                            }

                        },
                        error: function(error) {
                            console.log("error");
                        }
                    });

    return false;
  }
  else return false;


};
$('form').bind('submit', submitAction);

})(jQuery);
