/* ################################################################################### */
/* ####################                 CSRFToken                 ####################*/
/* ################################################################################### */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			// Only send the token to relative URLs i.e. locally.
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		}
	}
});

/******************* when window size is smaller, change some css **********************/

$(window).resize(function(){
	var width = $(window).width();
	if( width < 500 ){
		$("body").css("font-size","0.8em");
		$("nav").attr("data-offset-top","0");
	} else if( width >= 500 ){
		$("body").css("font-size", "1.2em");
	}	
});

/******************* In profile page, show info of level,point.. **********************/

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

/******************* change affix offset dynamically **********************/
//$("nav").affix({ offset: {top:$("div.background").height()-10 } });

/******************* category menu click function **********************/

$(document).ready(function(){
	$("ul#menu li button").click(function(){
		var name = "#"+$(this).val();
		var pos = $(this).offset();
		console.log("pos", pos);
		console.log("name", $(name).offset() );
		if( $(name).css("display") == "none"){
			if($(window).scrollTop() == 0 ){
				if($(window).width() < 800){
					$(name).offset({top:8.5, left:pos.left});
				} else{
					$(name).offset({top:pos.top-90, left:pos.left});
				}
			} else {
				$(name).offset({top:pos.top-100, left:pos.left});
			}			
			$(name).slideDown("300");
			$(name).siblings().hide();
			$(name).siblings().css('top','0');
			$(name).siblings().css('left','0');
		} else {
			$(name).hide();
			$(name).css('top','0');
			$(name).css('left','0');
		}
	});
	
	$("#wrap").click(function(){
		$(".list-box div").hide();
		$(".list-box div").css('top','0');
		$(".list-box div").css('left','0');
	});
	
	$(window).scroll(function(){
		$(".list-box div").hide();
		$(".list-box div").css('top','0');
		$(".list-box div").css('left','0');
	});
});


/******************* Purchase Page receiver info  **********************/

var chk = document.getElementById("receiverCheck");
$(chk).click(function(){
	if(chk.checked){
		$("input.rname").attr("value",$("input.sname").attr("value"));
		$("input.rnumber").attr("value",$("input.snumber").attr("value"));
		$("input.raddress").attr("value",$("input.saddress").attr("value"));
		$("input.raddress").attr("type","text");
		$("input.postcodify_postcode5").attr("type","hidden");
		$("input.postcodify_address").attr("type","hidden");
		$("input.postcodify_extra_info").attr("type","hidden");
		$("input.postcodify_details").attr("type","hidden");
	}else{
		$("input.rname").attr("value","");
		$("input.rnumber").attr("value","");
		$("input.raddress").attr("value","");
		
		$("input.raddress").attr("type","hidden");
		$("input.postcodify_postcode5").attr("type","text");
		$("input.postcodify_address").attr("type","text");
		$("input.postcodify_extra_info").attr("type","text");
		$("input.postcodify_details").attr("type","text");
	}
});

