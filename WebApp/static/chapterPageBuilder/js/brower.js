var data_save = true;

window.onbeforeunload = function () {

  if (data_save) {
    return "It looks like you haven't saved the document. If you leave before saving, your changes will be lost.";
  } else {
    return;
  }
};


document.querySelector("#SaveBtn").addEventListener("click", function () {
  data_save = false;
  sessionStorage.setItem("Value", $(".tab-content-no"));


})

$(document).ready(function () {

  $("body").on('DOMSubtreeModified', ".tab-content-no", function () {
    data_save = true;
  });



})

$("#SaveBtn").on("click",function(e){
  
  pages = {}
  var numberofpages = 0
  $('.pagenumber').each(function(key,value){
    textdiv = [];
    picdiv = [];
    numberofpages++;
    const obj=$("#tab"+parseInt(key+1)).children();
    let tops;
    let left;
    let width;
    let height;
    let content;
    $.each( obj, function( i, value ) {
      tops=$(this).css("top");
      left=$(this).css("left");
      width=$(this).css("width");
      height=$(this).css("height");
      content=$(this).text();

      console.log(value.classList);
      if(value.classList.contains('textdiv')){
        textdiv.push(
          {
            'tops': $(this).css("top"),
            'left': $(this).css("left"),
            'width': $(this).css("width"),
            'height': $(this).css("height"),
            'content': $(this).text()
          }
        );
      }
      if(value.classList.contains('pic')){
        picdiv.push(
          {
            'tops': $(this).css("top"),
            'left': $(this).css("left"),
            'width': $(this).css("width"),
            'height': $(this).css("height"),
            'background-image': value.style.backgroundImage
          }
        );
      }
    });
    pages[numberofpages] = [{'textdiv': textdiv,'pic':picdiv}]
  });
  data = {
    'numberofpages': numberofpages, 
    'chaptertitle': $('#chaptertitle').text(),
    'pages': pages,
    'canvasheight': $('.editor-canvas').css('height'),
    'canvaswidth': $('.editor-canvas').css('width'),
  };
  var json=JSON.stringify(data);
  $.ajax({
      url: save_json_url,
      type: 'post',
      data: {
        'json': json,
        'chapterID': chapterID,
        'courseID': courseID
      },
      success: function (data) {
        console.log(data)
        alert('saved successfully.')
      },
    });
});

$("#loadBtn").on("click",function(){
  $.get('/index/read', function(list) {
    let html=`
      <div>
      </div>
    `;
    let dom = $(html).css({
      "position": "absolute",
      "top": list.html.top,
      "left": list.html.left,
      "width":list.html.width,
      "height":list.html.height,
      "content":list.html.content
    });
    console.log(html);
  
});

});
  

