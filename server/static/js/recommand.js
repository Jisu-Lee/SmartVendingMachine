
function addDynamicCosmetic(NO, name, price, score, type, fav_flag){
  imgNo = (Math.floor(Math.random() * 10)) % 3 + 1;
  var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a ><img src="/static/images/'+type+"_"+imgNo+'.jpg") }}" alt="'+name+'" class="img-responsive"><h3 class="fh5co-work-title">'+name+'</h3>$'+price+'</a><span class="fa fa-star " id="cos'+NO+'" style="float: right">'+' '+score+'</span></div>';
  $("#"+type).append(template);

  if(fav_flag == true){
    $('.fa-star').css("color","orange");
  }
};


$(document).ready(function() {
	for(var i=0; i<recommanded_cos.length; i++){
		ptype = (recommanded_cos[i]["product_type"]).toUpperCase();
		if(ptype == "SUNSCREEN"){
			recommanded_cos[i]["product_type"] = "sunblock";
		}
		else if(ptype == "MOSITURIZER"){
			recommanded_cos[i]["product_type"] = "skin";
		}else if(ptype == "CREAM"){
			recommanded_cos[i]["product_type"] = "lotion";
		}
	addDynamicCosmetic(i+1, recommanded_cos[i]["name"], recommanded_cos[i]["price"], recommanded_cos[i]["rating"], recommanded_cos[i]["product_type"], recommanded_cos[i]["fav_flag"]);
	}

});
