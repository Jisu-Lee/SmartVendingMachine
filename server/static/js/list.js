
function addDynamicCosmetic(NO, name, price, score, type, fav_flag){

  var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a href="/templates/detail/'+NO+'.html"><img src="/static/images/'+NO+'.jpg") }}" alt="cosmetic img" class="img-responsive"><h3 class="fh5co-work-title">'+name+'</h3>$'+price+'</a><span class="fa fa-star checked" style="float: right">'+' '+score+'</span></div>';
  $(".data").append(template);
};


$(document).ready(function() {
addDynamicCosmetic(1, "cosmetic 1", 11037, 3.4, null, true);
addDynamicCosmetic(2, "cosmetic 2", 11037, 3.4, null,  true);
addDynamicCosmetic(3, "cosmetic 3", 11037, 3.4, null,  true);

});
