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

function convertFontToREM(font){
  return parseFloat(font)/14;
}

$(document).ready(function () {

  $("body").on('DOMSubtreeModified', ".tab-content-no", function () {
    data_save = true;
  });



})

// Preview purpose

$("#previewBtn").on("click",function(e){
  e.preventDefault();
  $("#SaveBtn").click();
  setTimeout(function(){
    let link = $("#previewBtn").attr('href');
    loadPreview(link, 1, 'Preview')
    // window.open($('#previewBtn').attr('href'))
  }, 7000)
})



$("#SaveBtn").on("click",function(e){
  $(this).html(`<i class='fa fa-spinner fa-spin '></i> Saving`);
  let prev_page = document.getElementsByClassName("tab-content-no current")[0].id.replace( /^\D+/g, '')
  setThumbnails(prev_page)
  deleteFile()
  setTimeout(function(){
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
      quizdiv = [];
      surveydiv = [];
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
          // $(clone).each(function(){
          //   if($(this).find('span').css('font-size')){
          //     let font = convertFontToREM($(this).find('span').css('font-size'))
          //     $(this).find('span').css('font-size', font + 'em')
          //   }
          // })
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
          link = $(this).find('model-viewer').attr('src');
  
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
        if(value.classList.contains('quiz-div')){
          quizdiv.push(
            {
              'tops': $(this)[0].style.top,
              'left': $(this)[0].style.left,
              'width': $(this)[0].style.width,
              'height': $(this)[0].style.height,
              'link': $(this).find("a").attr('href'),
              'quiz_btn_name': $(this).find(".resizable-text-only").text(),
              'quiz_name': $(this).find('.quiz-name').text(),
              'font_size': $(this).find('.resizable-text-only').css('font-size')
            }
          );
        }
        if(value.classList.contains('survey-div')){
          surveydiv.push(
            {
              'tops': $(this)[0].style.top,
              'left': $(this)[0].style.left,
              'width': $(this)[0].style.width,
              'height': $(this)[0].style.height,
              'link': $(this).find("a").attr('href'),
              'survey_btn_name': $(this).find(".resizable-text-only").text(),
              'survey_name': $(this).find('.survey-name').text(),
              'font_size': $(this).find('.resizable-text-only').css('font-size')
            }
          );
        }
      });
      backgroundcolor = $("#tab"+parseInt(this.value)).css('background-color')
      thumbnail = ($(value)[0].style['background-image']).replace(/^url\(["']?/, '').replace(/["']?\)$/, '');
      pages[numberofpages] = [{'textdiv': textdiv,'pic':picdiv, 'btn-div':buttondiv, 'pdf': pdf, 'video': video, '_3d': _3d, 'quizdiv':quizdiv, 'surveydiv':surveydiv, 'thumbnail': thumbnail, 'backgroundcolor': backgroundcolor}]
    });
    data = {
      'numberofpages': numberofpages, 
      'chaptertitle': $('#chaptertitle').text(),
      'pages': pages,
      'canvasheight': positionConvert($('#tabs-for-download').css('height'),$('body').height()),
      'canvaswidth': positionConvert($('#tabs-for-download').css('width'), $('body').width()),
    };
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
      },
      complete: function(data){
        $('#SaveBtn').html(`<a href="#" id="SaveBtn"><i class="fas fa-save"></i><br/>Save</a>`)
      }
    });
  }, 5000)
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
});

});

function loadPreview(link, ShowCloseBoxonInit = false, message) {
  $('#examiframeholder').addClass('examiframeholder')
  var ribbon = `<div class="ribbon blue"><span>${message}</span></div>`
  $('#iframeholder').append(`
      <iframe src = ${link} height = 100% width = 100%></iframe>
  `);
  if(message){
    $('#iframeholder').append(`
      ${ribbon}
  `);
  }
  $('iframe').on('load', function () {
      if ($(this).contents().find('#survey_already_taken').is(':visible')) {
          $('#closeiframebtn').css('display', 'block')
      }
      if (link != this.contentWindow.location.href && link + '/' != this.contentWindow.location.href) {
          $('#closeiframebtn').css('display', 'block')
      }
      if (ShowCloseBoxonInit) {
          $('#closeiframebtn').css('display', 'block')
      }
      
      $(this).contents().find('.closebtn, #hamburg-nav, #closechatopen').remove()
  });
}

$('#closeiframebtn').click(function () {
  $('#examiframeholder').removeClass('examiframeholder')
  $('#closeiframebtn').css('display', 'none')
  $('#iframeholder').empty();
})