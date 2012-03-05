/* 
 * Photobook 
 *
 * edit.js 
 *
 * Album editor
 *
 */

//2s timeout for edit events, after which the page will be saved
var editTimeout = {  
      timeout: function() {  
        savePage();
        delete this.timeoutID;  
      },  
      
      setup: function() {  
        this.cancel();  
        var self = this;  
        this.timeoutID = window.setTimeout(function() {self.timeout();}, 2000); 
      },  
      
      cancel: function() {  
        if(typeof this.timeoutID == "number") {  
          window.clearTimeout(this.timeoutID);  
          delete this.timeoutID;  
        }  
      }  
};  
 
var pageChangeCallback = function(){
	makeEditable();
};

function savePage(){
	$("#savePage").button('loading');
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

	$("#page .caption").each(function(){
		var $caption = $(this);
		var x = parseInt($caption.css("left"));
		var y = parseInt($caption.css("top"));
		positions.push({
			"caption": {
				"content": $caption.text(),
				"font": $caption.data("font")
			},
			"w": parseInt($caption.css("width")),
			"h": parseInt($caption.css("height")),
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
	        console.log("page saved!");
	        $("#savePage").button('reset');
	    }
	});
};

function makeEditable(){
	makeImgEditable();
	makeCaptionEditable();
}

/* Set images resizable, draggable and removable */
function makeImgEditable($img){
	console.log("makeImgEditable",$img);
	
	// If image is not set, let's use all images in the page
	if (typeof($img) === "undefined"){
		$img = $("#page img")
	}
	
	$img
		/* Make resizable using JQuery UI */
		.resizable({aspectRatio: true, containment: 'parent'})
		/* Resizable will generate a parent div around img, let's use it */
		.parent()
			/* Make draggable using JQuery UI */
			.draggable({ containment: 'parent' })
			/* Add delete-button on hover */
			.hover(function() {
					$("<a id='hover-delete-button' class='btn btn-inverse'><i class='icon-trash icon-white'></i></a>")
						.click(function() {
							var img = $(this).siblings("img");
							console.log("Delete image", img);
							img.remove();
						})
						.appendTo($(this));
				},
				/* Remove button on unhover */
				function() {
					$("#hover-delete-button").remove();
				}
			)
			.on("resize drag", function() {
				editTimeout.setup();
			});
}

function makeCaptionEditable($div){
	console.log("makeCaptionEditable",$div);
	
	// If caption is not set, let's use all captions in the page
	if (typeof($div) === "undefined"){
		$div = $("#page div.caption");
	}

	$div
    	.resizable({ containment: 'parent'})
		.draggable({ containment: 'parent'})
		.hover(function() {
				$("<a id='hover-delete-button' class='btn btn-inverse'><i class='icon-trash icon-white'></i></a>")
					.click(function() {
						var $div = $(this).parent();
						console.log("Delete caption", $div);
						$div.remove();
					})
					.appendTo($(this));
			},
			/* Remove button on unhover */
			function() {
				$("#hover-delete-button").remove();
			}
		)
		.on("resize drag", function() {
			editTimeout.setup();
		});
}

function addImage(url){
	console.log("Add image " + url);
	var $img = $("<img>")
		.attr({src: url})
		.appendTo("#page");

	makeImgEditable($img);
	editTimeout.setup();
}

function addCaption(text,font){
	var text = $("<div>"+text+"</div>")
		.attr("class","caption " + font)
		.data("font",font)
		.css("z-index",100)
		.appendTo("#page");
		
	makeCaptionEditable(text);
	editTimeout.setup();	
}

// Document ready callback

$(function() {

	/* Load the first page and make it editable */
	
	loadPage(album,page,function(){
		makeEditable();
	});
	
	/* Adding images */
	
	$("#addImageModalBtn").click(function(){
		addImage($("#newImageUrl").val());
	});
    
    $(document).on("click", "#foundPicture", function(){
    	addImage($(this).attr("src"));
    });
	
	$("#newImageUrl").bind("propertychange keyup input paste", function(){
		console.log("#newImageUrl changed");
		$("#previewImg").attr("src",$("#newImageUrl").val());
	});
    
    $("#searchBtn").click(function() {
        var url = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=baeae16ada7e043585db45da91af1601&text=" + $("#search").val() + "&safe_search=1&per_page=20";
        $("#results").empty();
        $.getJSON(url + "&format=json&jsoncallback=?", function(data) {
            $.each(data.photos.photo, function(i, item){
                src = "http://farm"+ item.farm +".static.flickr.com/"+ item.server +"/"+ item.id +"_"+ item.secret +"_m.jpg";
                var img ='<img id="foundPicture" data-dismiss="modal" src="' + src + '"alt="' + item.title + '"width="100" height="100" />';
                $("#results").append(img);
                if ( i == 3 ) return false;
            });
        });
    });
    
    /* Adding captions */
    
    $("#addCaptionModalBtn").click(function(){
    	var text = $("#newCaption").val();
    	var font = $('input:radio[name=styleSelect]:checked').val();
    	addCaption(text,font)
	});
	
	/* Saving page */
	
	$("#savePage").click(function(){
		savePage();
	});
	
	$("#deletePage").click(function () {
        console.log("Delete pressed")
		var r=confirm("Are you sure? This will delete the page permanently.");
        if (r==true) {
                window.location = "../"+page+"/delete";
        }
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

});