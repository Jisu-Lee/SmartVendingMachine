
 function addDynamicCosmetic(NO, name, price, score, type, fav_flag){

   var imgNo = (Math.floor(Math.random() * 10)) % 3 + 1;
   var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a ><img src="/static/images/' +type+"_"+imgNo+ '.jpg" alt="WG" class="img-responsive"><h3 class="fh5co-work-title">'+name+'</h3>$'+price+'</a><span class="fa fa-star checked cos'+NO+'" style="float: right">'+' '+score+'</span></div>';

   $("#"+type).append(template);
   $("#home").append(template);
   if(fav_flag == "true"){
     $('.fa-star').css("color","orange");
}
 };

$(document).ready(function(){
	for(var i=0; i<fav_list.length; i++){
		ptype = (fav_list[i]["product_type"]).toUpperCase();
		if(ptype == "SUNSCREEN"){
			fav_list[i]["product_type"] = "sunblock";
		}
		else if(ptype == "MOSITURIZER"){
			fav_list[i]["product_type"] = "skin";
		}else if(ptype == "CREAM"){
			fav_list[i]["product_type"] = "lotion";
		}
	addDynamicCosmetic(fav_list[i][0], fav_list[i]["name"], fav_list[i]["price"], fav_list[i]["rating"], fav_list[i]["product_type"], fav_list[i]["fav_flag"])
	}
});
