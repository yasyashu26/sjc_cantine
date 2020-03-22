$(document).ready(function(){
 $('.header').height($(window).height());
 
})

/* scroll effect */

$(".btn btn-outline-secondary btn-lg").click(function(){
    $("body,html").animate({
     scrollTop:$("coll" + $(this).data('value')).offset().top
    },2000)
    
   })