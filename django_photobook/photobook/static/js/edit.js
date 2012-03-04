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
    $( "#page img" ).resizable( "option", "containment", "parent" );
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
    
    $(document).on("click", "#foundPicture", function(){
        var url = $(this).attr("src");
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
    
    $("#searchBtn").click(function() {
        var url = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=baeae16ada7e043585db45da91af1601&text=" + $("#search").val() + "&safe_search=1&per_page=20";
        console.log(url);
        $("#results").empty();
        $.getJSON(url + "&format=json&jsoncallback=?", function(data) {
            $.each(data.photos.photo, function(i, item){
                src = "http://farm"+ item.farm +".static.flickr.com/"+ item.server +"/"+ item.id +"_"+ item.secret +"_m.jpg";
                console.log(src);
                var img ='<img id="foundPicture" data-dismiss="modal" src="' + src + '"alt="' + item.title + '"width="100" height="100" />';
                $("#results").append(img);
                console.log(img);
                if ( i == 3 ) return false;
            });
        });
    });
	
	$("#savePage").click(function(){
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
	
	/* "caption": {
	       			"content": "Cute puppies ~<3",
	       			"font": "foobar"
	       		}, 
	*/

});