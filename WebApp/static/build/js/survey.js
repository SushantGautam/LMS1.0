$(document).ready(function categoryAddButton(categoryName) {
    // .................................................................................
    $(".mcq_question").on("click", function () {
        $("#mcq_que").show(100);
        $("#short_que").hide();
    });

    $(".short_question").on("click", function () {
        $("#short_que").show(100);
        $("#mcq_que").hide();
    });
});

// -----------------------------ACTIVE AND EPIRE -------------------------------------
$("#ActiveButton").on("click", function () {
    $(".active_survey").show(300);
    //$(this).css('color', 'white');
    $(".expire_survey").hide();
});
$("#ExpireButton").on("click", function () {
    $(".expire_survey").show(300);
    // $(this).css('color', 'white');
    $(".active_survey").hide();
});

function Myfunctionbtn(event, obj) {
    event.preventDefault();

    console.log(`options-${obj.id}`);
    var parentLi = $(`#options-${obj.id}`);
    if (parentLi.children().length > 0) {
        lastChildId = parentLi.children().length + 1;
    } else {
        lastChildId = 1;
    }

    $("#options-" + obj.id)
        .append(`<li id="${lastChildId}" style="list-style:none; margin-left: 20px; ">
      <div style="display:flex;"><p style="margin-top: 10px; margin-right: 10px">${lastChildId}</p> 
      <input class="form-control" type="text" name="option" placeholder="option" style="margin-left: 5px;"></div>
      </li>`);
}

$(document).ready(function () {
    var count = 1;
    var increse = 1;
    $("#newQuestion").on("click", function (e) {
        e.preventDefault();
        var id1 = parseInt(count++);
        $("#mySelect").append(`
              <li id="question-${id1}">
              <div style="display:flex;"><p style="margin-top: 35px; margin-right: 20px">${id1}</p>
              <input class="form-control" placeholder="Enter Questions here..." type="text" style="list-style:none; margin-top: 30px; " name="questions"></div>
               <label for="option" style="margin-top: 10px; margin-bottom: 10px;">Option:</label><button id="${id1} " onclick="Myfunctionbtn(event,this)" class="btn btn-success" style="margin-top:5px; margin-bottom: 10px;">Add option</button> 
               </li><li id="options-${id1}" style="list-style:none;"></li>`);
    });
    $("#addButtons").on("click", function (e) {
        e.preventDefault();
        var id2 = parseInt(increse++);
        $("#short_que_add").append(
            `<li id="shq-${id2}"><div style="display:flex; align-items: center;"><p style="margin-top: 10px; margin-right: 20px; margin-bottom: 20px;">${id2}</p><input class="form-control" placeholder="Enter Questions here..." type="text" name="questions"></div></li>`
        );
    });

});

$(document).ready(function () {
    var navListItems = $("div.setup-panel div a"),
        allWells = $(".setup-content"),
        allNextBtn = $(".nextBtn");

    allWells.hide();

    navListItems.click(function (e) {
        e.preventDefault();
        var $target = $($(this).attr("href")),
            $item = $(this);

        if (!$item.hasClass("disabled")) {
            navListItems.removeClass("btn-primary").addClass("btn-default");
            $item.addClass("btn-primary");
            allWells.hide();
            $target.show();
            $target.find("input:eq(0)").focus();
        }
    });

    allNextBtn.click(function () {
        var curStep = $(this).closest(".setup-content"),
            curStepBtn = curStep.attr("id"),
            nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]')
                .parent()
                .next()
                .children("a"),
            curInputs = curStep.find("input[type='text'],input[type='url']"),
            isValid = true;

        $(".form-group").removeClass("has-error");
        for (var i = 0; i < curInputs.length; i++) {
            if (!curInputs[i].validity.valid) {
                isValid = false;
                $(curInputs[i])
                    .closest(".form-group")
                    .addClass("has-error");
            }
        }

        if (isValid) nextStepWizard.removeAttr("disabled").trigger("click");
    });

    $("div.setup-panel div a.btn-primary").trigger("click");
});