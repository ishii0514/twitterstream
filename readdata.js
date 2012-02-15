var map;
var markersArray = [];


$(function(){
	//"$(document).ready(function(){...});"と同じ
	// body onload の前に呼ばれる
	
  //mapの初期化
  initialize();
  // JSONファイル読み込み開始ボタン
  /*
  $("#dl","#btn").click(function(){
	  $.ajax({
		url:"data.json",
		cache:false,
		dataType:"json",
		success:function(json){
		var data=jsonRequest(json);
		addMarker(data);
    }
    });
  });
  */
  //JSONファイルポーリング
  $("#map_canvas").smartupdater({
	url : "data.json",
	dataType:"json",
	minTimeout: 2000 	// 2 seconds
	}, function (json) {
		deleteOverlays();
		var data=jsonRequest(json);
		addMarker(data);
	}
  );
});


function initialize() {
  var latlng = new google.maps.LatLng(41.791217,140.775032);
  var opts = {
    zoom: 10,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), opts);
 //google.maps.event.addListener(map,'click',clickAction);
  
}

// JSONファイル読み込み
function jsonRequest(json){
  var data=[];
  if(json.Marker){
    for(var i=0;i<json.Marker.length;i++){
      data.push(json.Marker[i]);
    }
  }
  return data;
}

function addMarker(data){
  var i=data.length;
  while(i-- >0){
    var dat=data[i];
    var obj={
      position:new google.maps.LatLng(dat.lat,dat.lng),
      map:map
    };
    var marker=new google.maps.Marker(obj);
    markersArray.push(marker);
  }
}
function deleteOverlays() {
  if (markersArray) {
    for (i in markersArray) {
      markersArray[i].setMap(null);
    }
    markersArray.length = 0;
  }
}