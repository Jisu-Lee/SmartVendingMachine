
//var instance = M.Tabs.init(el, options);

 // Or with jQuery
 function addDynamicCosmetic(i){
   var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a href="work.html"><img src="images/work_2.jpg" alt="Free HTML5 Website Template by FreeHTML5.co" class="img-responsive"><h3 class="fh5co-work-title">Cosmetic '+i+'</h3>$99,999</a><span class="fa fa-star checked" style="float: right"></span></div>'
   $("#test1").append(template);
 }

 $(document).ready(function(){

   //$('.tabs').tabs();
   addDynamicCosmetic(1);
   addDynamicCosmetic(2);
 });
