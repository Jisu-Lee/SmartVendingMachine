/*users = [ {birthyear:"", gender:"", id:"", name:"", pw:"", skintype:"", user_id:""},
            {.....}
            ]
*/
$(document).ready(function() {
    "use strict";

    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        if(check == true){
          sendDataAJAX(input);
        }

        return false;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

    function sleep(miliseconds) {
       var currentTime = new Date().getTime();

       while (currentTime + miliseconds >= new Date().getTime()) {
       }
    }

    function sendDataAJAX(input) {

        var myObj = new Object();
        //alert($('input[name="username"]').val()+"/"+$('input[name=pass]').val());

        var login_data = [$('input[name="username"]').val(), $('input[name="pass"]').val()];  //id = userID, data = cosmeticID
        myObj.data = login_data;
        var jsonText =  JSON.stringify(myObj);
        console.log(jsonText);
        $.ajax({
                url: '/getlogin',
                data: jsonText,
                type: 'POST',
                dataType: "json",
                contentType: 'application/json;charset=UTF-8',
                success: function(response) {
                    if(response["status"] == "ok"){
                        window.location.href='https://wannagraduate-220706.appspot.com/list';
                    }else{
                        window.location.href='https://wannagraduate-220706.appspot.com/login';
                    }
                },
                error: function(error) {
                    console.log(error);

                }
            });
            return false;

    }



});
