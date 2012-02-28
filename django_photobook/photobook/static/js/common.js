/* Photobook common.js */

$(document).ready(function(){
	console.log("[common.js] document ready");
	
	$("#next").click(function(){
		if(page+1<=pages){
			console.log("Next page");
			page++;
			loadPage(album,page);
		} else {
			console.log("No next page");
		}
	});
	
	$("#previous").click(function(){
		if(page-1>0){
			console.log("Previous page");
			page--;
			loadPage(album,page);
		} else {
			console.log("No previous page");
		}
	});
});

function loadPage(album,page,callback){
	console.log("[common.js] loadPage "+album+","+page);
	
	updateArrows();
	$("#loader").show();
	$("#page").empty();
	
	$.getJSON("/album/"+album+"/"+page+"/json", function(data,status){
		console.log(data,status);
		
		if(data && data.page && data.page.positions){
			for(var i=0; i<data.page.positions.length; i++){
				var position = data.page.positions[i];
				//console.log(position);
				
				if(position.image){
					$("<img />")
						.attr("src",position.image.url)
						.css({
							"position":"absolute", 
							"left": position.x+"px",
							"top": position.y+"px",
							"height": position.h+"px",
							"width": position.w+"px"
							})
						.appendTo("#page");
				} else if (position.caption) {
					$("<div>"+position.caption.content+"</div>")
						.css({
							"position":"absolute", 
							"left": position.x+"px",
							"top": position.y+"px",
							"height": position.h+"px",
							"width": position.w+"px"
							})
						.appendTo("#page");
				}
			}		
		}
		
		$("#loader").hide();
		callback();
	});
}

function updateArrows(){
	console.log("updateArrows");
	if(page>=pages){
		$("#next").addClass("disabled");
	} else {
		$("#next").removeClass("disabled");
	}
	
	if(page<=1){
		$("#previous").addClass("disabled");
	} else {
		$("#previous").removeClass("disabled");
	}
}