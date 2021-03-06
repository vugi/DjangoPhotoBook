/* 
 * Photobook 
 *
 * common.js 
 *
 * This file includes all shared components between view and edit -modes
 *
 */

$(document).ready(function(){
	console.log("[common.js] document ready");
	
	$("#next").click(function(){
		if(page+1<=pages){
			console.log("Next page");
			page++;
			loadPage(album,page,pageChangeCallback);
		} else {
			console.log("No next page");
		}
	});
	
	$("#previous").click(function(){
		if(page-1>0){
			console.log("Previous page");
			page--;
			loadPage(album,page,pageChangeCallback);
		} else {
			console.log("No previous page");
		}
	});
    
    $("#deleteAlbum").click(function() {
        var r=confirm("Are you sure? This will delete the album permanently.");
        if (r==true) {
                window.location = "delete";
        }
    });
});

function loadPage(album,page,callback){
	console.log("[common.js] loadPage "+album+","+page);
	
	updateArrows();
	updatePageNumbering();
	$("#loader").show();
	$("#page").empty();
	
	$.getJSON("/album/"+album+"/"+page+"/json/", function(data,status){
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
						.attr("class", "caption " + position.caption.font)
						.data("font", position.caption.font)
						.css({
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
		if(typeof callback == "function"){
			callback();
		}
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

function updatePageNumbering(){
	$("#page-numbering").html(page + "/" + pages);
}