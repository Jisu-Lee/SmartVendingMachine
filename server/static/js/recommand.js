
function addDynamicCosmetic(j, i){

  var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a href="work.html"><h4>'+j+'</h4><img src="images/work_2.jpg" alt="Free HTML5 Website Template by FreeHTML5.co" class="img-responsive"><h3 class="fh5co-work-title">Cosmetic '+i+'</h3>$99,999</a></div>'
  $(".data").append(template);
};


$(document).ready(function() {
  addDynamicCosmetic("1ST", 1);
  addDynamicCosmetic("1ST", 2);
  addDynamicCosmetic("1ST", 3);
  addDynamicCosmetic("2ND", 4);
  addDynamicCosmetic("2ND", 5);
  addDynamicCosmetic("2ND", 6);
  addDynamicCosmetic("3RD", 7);
  addDynamicCosmetic("3RD", 8);
  addDynamicCosmetic("3RD", 9);
  addDynamicCosmetic("4TH", 10);
  addDynamicCosmetic("4TH", 11);
  addDynamicCosmetic("4TH", 12);
});
