
function addDynamicCosmetic(NO, name, price, score, type, fav_flag){

  var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a href="detail/'+NO+'.html"><img src="/static/images/'+NO+'.jpg") }}" alt="'+name+'" class="img-responsive"><h3 class="fh5co-work-title">'+name+'</h3>$'+price+'</a><span class="fa fa-star checked" style="float: right">'+' '+score+'</span></div>';
  $("#"+type).append(template);

  if(fav_flag == true){
    $('.fa-star').css("color","orange");
  }
};


$(document).ready(function() {
addDynamicCosmetic(1, "cosmetic 1", 11037, 3.4, "skin", true);
addDynamicCosmetic(2, "cosmetic 2", 11037, 4.5, "lotion",  true);
addDynamicCosmetic(3, "cosmetic 3", 11037, 3.9, "sunblock",  true);
addDynamicCosmetic(4, "cosmetic 4", 11037, 4.1, "skin", true);
addDynamicCosmetic(5, "cosmetic 5", 11037, 4.2, "lotion",  true);
addDynamicCosmetic(6, "cosmetic 6", 11037, 3.7, "sunblock",  true);
addDynamicCosmetic(7, "cosmetic 7", 11037, 3.9, "skin", true);
addDynamicCosmetic(8, "cosmetic 8", 11037, 4.4, "lotion",  true);
addDynamicCosmetic(9, "cosmetic 9", 11037, 4.1, "sunblock",  true);

});
