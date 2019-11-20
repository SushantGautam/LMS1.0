var data_save = true;

window.onbeforeunload = function () {
  if (data_save) {
    $('#chapterlist').val(previous)
    return "It looks like you haven't saved the document. If you leave before saving, your changes will be lost.";
  } else {
    return;
  }
};


document.querySelector("#SaveBtn").addEventListener("click", function () {
  data_save = false;
  sessionStorage.setItem("Value", $(".tab-content-no"));


})

function positionConvert(element, divider){ 
  return parseFloat(element)*100/parseFloat(divider)
}

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
    video = [];
    _3d = [];
    numberofpages++;
    const obj=$("#tab"+parseInt(this.value)).children();
    let tops;
    let left;
    let width;
    let height;
    let content;
    htmlfile[(key+1)] = ($("#tab"+parseInt(this.value)).html());
    
    $.each( obj, function( i, value ) {
      if(value.classList.contains('textdiv')){
        var clone = $(this).find('.note-editable').clone();
        // clone.find('div').remove();
        var content_html = clone.html();
        textdiv.push(
          {
            'tops': $(this)[0].style.top,
            'left': $(this)[0].style.left,
            'width': $(this)[0].style.width,
            'height': $(this)[0].style.height,
            'content': content_html
          }
        );
      }
      if(value.classList.contains('pic')){
        console.log($(this)[0].style.height, $(this)[0].style.width, $('#tabs-for-download').css('height'))

        picdiv.push(
          {
            'tops': $(this)[0].style.top,
            'left': $(this)[0].style.left,
            'width': $(this)[0].style.width,
            'height': $(this)[0].style.height,
            'background-image': $(this).find("img").attr('src')
          }
        );
      }
      if(value.classList.contains('btn-div')){
        buttondiv.push(
          {
            'tops': $(this)[0].style.top,
            'left': $(this)[0].style.left,
            'width': $(this)[0].style.width,
            'height': $(this)[0].style.height,
            'link': $(this).children("a").attr('href'),
            'btn_name': $(this).children("a").text(),
          }
        );
      }
      if(value.classList.contains('pdfdiv')){
        pdf.push(
          {
            'tops': $(this)[0].style.top,
            'left': $(this)[0].style.left,
            'width': $(this)[0].style.width,
            'height': $(this)[0].style.height,
            'link': $(this).find('object').attr('data'),
          }
        );
      }
      if(value.classList.contains('video-div')){
        online_link = $(this).find('iframe').attr('src');
        local_link = $(this).find('video > source').attr('src');

        video.push(
          {
            'tops': $(this)[0].style.top,
            'left': $(this)[0].style.left,
            'width': $(this)[0].style.width,
            'height': $(this)[0].style.height,
            'online_link': online_link,
            'local_link': local_link
          }
        );
      }
      if(value.classList.contains('_3dobj-div')){
        link = $(this).find('iframe').attr('src');

        _3d.push(
          {
            'tops': $(this)[0].style.top,
            'left': $(this)[0].style.left,
            'width': $(this)[0].style.width,
            'height': $(this)[0].style.height,
            'link': link,
          }
        );
      }
      
    });
    thumbnail = ($(value)[0].style['background-image'])
    pages[numberofpages] = [{'textdiv': textdiv,'pic':picdiv, 'btn-div':buttondiv, 'pdf': pdf, 'video': video, '_3d': _3d, 'thumbnail': thumbnail}]
  });
  data = {
    'numberofpages': numberofpages, 
    'chaptertitle': $('#chaptertitle').text(),
    'pages': pages,
    'canvasheight': positionConvert($('#tabs-for-download').css('height'),$('body').height()),
    'canvaswidth': positionConvert($('#tabs-for-download').css('width'), $('body').width()),
  };
  console.log(pages)
  var json=JSON.stringify(data);
  $.ajax({
    url: save_json_url,
    type: 'post',
    data: {
      'csrfmiddlewaretoken': csrf_token,
      'json': json,
      'htmlfile': JSON.stringify(htmlfile),
      'chapterID': chapterID,
      'courseID': courseID
    },
    success: function (data) {
      alert('saved successfully.')
    },
    error: function(e){
      console.log(e)
      alert("Failed to save data")
    }
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