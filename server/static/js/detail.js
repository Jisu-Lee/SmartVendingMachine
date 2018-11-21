function addDetailData(NO, name, price, score, type, fav_flag, explanation){
  var template = '<div class="col-md-12 animate-box" data-animate-effect="fadeInLeft"><figure class="text-center"><img src="/static/images/'+NO+'.jpg") }}" alt="cosmetic img" class="img-responsive"></figure></div><div class="col-md-8 col-md-offset-2 animate-box" data-animate-effect="fadeInLeft"><div class="col-md-9 col-md-push-3"><h1>'+name+'</h1><p>'+explanation+'</p><h3 style="float:right">'+price+'</h3></div><div class="col-md-3 col-md-pull-9 fh5co-services"><h3>'+type+'</h3><ul><li>'+score+'</li></ul></div></div>';
  $("#detail").append(template);
};

$(document).ready(function() {
addDetailData(1, "cosmetic 1", 11037, 3.4, "skin",  true, "왜 안보이지?");

});
