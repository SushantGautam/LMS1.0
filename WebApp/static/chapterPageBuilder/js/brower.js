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
  htmlfile = {};
  $('.pagenumber').each(function(key,value){
    textdiv = [];
    picdiv = [];
    buttondiv = [];
    pdf = [];
    numberofpages++;
    const obj=$("#tab"+parseInt(key+1)).children();
    let tops;
    let left;
    let width;
    let height;
    let content;
    htmlfile[(key+1)] = ($("#tab"+parseInt(key+1)).html());
    
    $.each( obj, function( i, value ) {
      if(value.classList.contains('textdiv')){
        console.log($(this).css("width"),$(this).css("height"))
        var clone = $(this).children('.messageText').clone();
        clone.find('div').remove();
        var content_html = clone.html();
        textdiv.push(
          {
            'tops': $(this).css("top"),
            'left': $(this).css("left"),
            'width': $(this).css("width"),
            'height': $(this).css("height"),
            'content': content_html
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
      if(value.classList.contains('btn-div')){
        buttondiv.push(
          {
            'tops': $(this).css("top"),
            'left': $(this).css("left"),
            'width': $(this).css("width"),
            'height': $(this).css("height"),
            'link': $(this).children("a").attr('href'),
          }
        );
      }
      if(value.classList.contains('pdf')){
        pdf.push(
          {
            'tops': $(this).css("top"),
            'left': $(this).css("left"),
            'width': $(this).css("width"),
            'height': $(this).css("height"),
            'link': $(this).children('object').attr('data'),
          }
        );
      }
    });
    pages[numberofpages] = [{'textdiv': textdiv,'pic':picdiv, 'btn-div':buttondiv, 'pdf': pdf}]
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
        'htmlfile': JSON.stringify(htmlfile),
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