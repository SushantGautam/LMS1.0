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
    window.open($('#previewBtn').attr('href'))
  }, 7000)
})



$("#SaveBtn").on("click",function(e){
  $(this).html(`<i class='fa fa-spinner fa-spin '></i> Saving`);
  changePage(window.currentPage)
  deleteFile()
  setTimeout(function(){
    console.log(data)
    var pages = {}
    var numberofpages = 0
    
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
        console.log(data)
        alert('saved successfully.')
      },
      error: function(e){
        console.log(e)
        alert("Failed to save data")
      },
      complete: function(data){
        console.log(data)
        $('#SaveBtn').html(`<a href="#" id="SaveBtn"><i class="fas fa-save"></i><br/>Save</a>`)
      }
    });
  }, 5000)
});