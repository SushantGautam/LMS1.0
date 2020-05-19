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
  }, 4000)

})

$("#SaveBtn").on("click",function(e){
  $(this).html(`<i class='fa fa-spinner fa-spin '></i> Saving`);
  
  changePage(window.currentPage)
  setTimeout(function(){
    var pages = {}
    var numberofpages = 0
    
    data.numberofpages = $('.pagenumber').length
    data.chaptertitle = $('#chaptertitle').text()
    var json=JSON.stringify(data);
    $.ajax({
      url: save_json_url,
      type: 'post',
      data: {
        'csrfmiddlewaretoken': csrf_token,
        'json': json,
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
        $('#SaveBtn').html(`<a href="#" id="SaveBtn" style="background-color:#353c46;"><i style="color:white" class="fas fa-save"></i>&nbsp;Save</a>`)
      }
    });
  }, 3000)
});

$('#save-and-exit-btn').click(function (e) {
  e.preventDefault();

  window.alert = function () {
  };
  window.onbeforeunload = function () {
  };
  $('#SaveBtn').click();
  setTimeout(function(){
      var href = $('#goBackBtn').attr('href');
      location.href = href;
  }, 5000)
});

function loadPreview(link, ShowCloseBoxonInit = false, message, externallink = false) {
  $('#examiframeholder').addClass('examiframeholder')
  var ribbon = `<div class="ribbon blue"><span>${message}</span></div>`
  $('#iframeholder').append(`
      <iframe src = ${link} height = 100% width = 100%></iframe>
  `);
  if (message) {
    $('#iframeholder').append(`
      ${ribbon}
  `);
  }
  $('iframe').on('load', function () {
    if (!externallink) {
      if ($(this).contents().find('#survey_already_taken').is(':visible')) {
        $('#closeiframebtn').css({'display':'block', 'top':'6vh'})
      }
      if (link != this.contentWindow.location.href && link + '/' != this.contentWindow.location.href) {
        $('#closeiframebtn').css({'display':'block', 'top':'6vh'})
      }
    }
    if (ShowCloseBoxonInit) {
      $('#closeiframebtn').css({'display':'block', 'top':'6vh'})
    }
      
      $(this).contents().find('.closebtn, #hamburg-nav, #closechatopen, .edit-viewer').remove()
  });
}

$('#closeiframebtn').click(function () {
  $('#examiframeholder').removeClass('examiframeholder')
  $('#closeiframebtn').css('display', 'none')
  $('#iframeholder').empty();
})
