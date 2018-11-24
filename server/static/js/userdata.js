function addUserData(name, birthYear, skinType, gender){

  var temp1 = '<label class="control-label col-sm-2" id="name">Name:</label>';
  var temp2 = '<label class="control-label col-sm-2" id="birth_year">Birth Year:</label>';
  var temp3 = '<label class="control-label col-sm-2" id="skin_type">Skin Type:</label>';
  var temp4 = '<label class="control-label col-sm-2" id="gender">Gender:</label>';
  var name = '<div class="col-sm-10" ><p class="form-control-static">'+name+'</p></div>';
  var birthYear = '<div class="col-sm-10"><p class="form-control-static">'+birthYear+'</p></div>';
  var skinType = '<div class="col-sm-10"><p class="form-control-static">'+skinType+'</p></div>';
  var gender = '<div class="col-sm-10"><p class="form-control-static">'+gender+'</p></div>';

  $(".form-group").append(temp1);
  $(".form-group").append(name);
  $(".form-group").append(temp2);
  $(".form-group").append(birthYear);
  $(".form-group").append(temp3);
  $(".form-group").append(skinType);
  $(".form-group").append(temp4);
  $(".form-group").append(gender);
};

//user=[{"birthyear": "1995", "gender": "male", "id": "1", "name": "Leland", "pw": "9771", "skintype": "dry", "user_id": "Leland"}]
$(document).ready(function() {
addUserData(user[0]["name"], user[0]["birthyear"], user[0]["skintype"], user[0]["gender"]);

});
