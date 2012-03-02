/* 
 * Photobook 
 *
 * edit.js 
 *
 * Album editor
 *
 */

var pageChangeCallback = function(){
	makeEditable();
};

/* Set images resizable and draggable */
function makeEditable(){
	$("#page img")
		.resizable({aspectRatio: true})
		.parent().draggable({ containment: 'parent' });
}

$(function() {
	
	loadPage(album,page,function(){
		makeEditable();
	});
	
	$("#addImageModalBtn").click(function(){
		var url = $("#newImageUrl").val();
		console.log(url);
		var $img = $("<img>")
			.attr("src",url)
			.appendTo("#page");

		makeEditable();
	});
	
	$("#newImageUrl").bind("propertychange keyup input paste", function(){
		console.log("changed");
		$("#previewImg").attr("src",$("#newImageUrl").val());
	});
	
	$("#savePage").click(function(){
		var positions = [];
		
		$("#page img").each(function(){
			var $img = $(this);
			var x = parseInt($img.parent().css("left"));
			var y = parseInt($img.parent().css("top"));
			positions.push({
				"image": $img.attr("src"),
				"w": parseInt($img.css("width")),
				"h": parseInt($img.css("height")),
				"x": x ? x : 0,
				"y": y ? y : 0,
				"z": 1
			});
		});
		
		var obj = { "positions" : positions };
		console.log(obj);
		
		$.ajax({
		   	url: "/album/"+album+"/"+page+"/json/",
		    type: 'POST',
		    contentType: 'application/json; charset=utf-8',
		    data: JSON.stringify(obj),
		    dataType: 'text',
		    success: function(result) {
		        alert("page saved!");
		    }
		});
	});
	
	$("#deletePage").click(function () {
		window.location = "../"+page+"/delete";
	});
	
	$("#addPage").click(function () {
		$.ajax({
		   	url: "/album/"+album+"/"+(pages+1)+"/json/",
		    type: 'POST',
		    contentType: 'application/json; charset=utf-8',
		    success: function(result) {
		        console.log("page added");
		        pages++;
		        page=pages;
				loadPage(album,page);
		    }
		});
	});
	
	/* "caption": {
	       			"content": "Cute puppies ~<3",
	       			"font": "foobar"
	       		}, 
	*/

});