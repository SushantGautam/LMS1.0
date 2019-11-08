$(document).ready(function() {

    var button_html = {
        html : 
            `
                <div class = "hamburger-content">
                    <div class = "ham1"></div>
                    <div class = "ham2"></div>
                    <div class = "ham3"></div>                
                </div>
            `
    }
    $('#tabs-for-download').droppable({
        tolerance: 'fit',
        drop: function( event, ui ) {
            $(this).removeClass("border").removeClass("over");
        },
        
        over: function(event, elem) {
            $(this).addClass("over");
        },
        out: function(event, elem) {
            $(this).removeClass("over");
        },
     });

    // ==================For TextBoxx================================
    class Textbox {
        constructor(collg = null, colmd = null, colsm = null, colxs = null, height = null, width = null, message="Type Something Here...") {
            let id = (new Date).getTime();
            let position = {
                height, width
            };
            let html = `
                <div class='textdiv col-lg-${collg} col-md-${colmd} col-sm-${colsm} col-xs-${colxs}'>
                     <div id="editor${id}" class="messageText"></div>
                     <div id="text-actions" class = "text-actions">
                         <i class="fas fa-trash" id=${id}></i>
                         <i class="fas fa-arrows-alt" id="draghere" ></i>
                     </div> 
                  </div>
            `;
            this.renderDiagram = function() {
                // dom includes the html,css code with draggable property
                let dom = $(html).css({
                    // "position": "absolute",
                    
                    "height": position.height,
                    "width": position.width,
                    "border": "2px dashed #000 !important"

                }).draggable({
                    containment: "#tabs-for-download",
                    scroll: false,
                    cursor: "move",
                    snap: ".gridlines",
                    snapMode: 'inner',
                    cursorAt: { bottom: 0 },
                  
                    handle: '#draghere'
                });
                

                var a = document.getElementsByClassName("current")[0];
                $('#' + a.id).append(dom);
                $('#editor'+id).summernote();
                $('#editor'+id).parent().find('.note-editable').html(message);
                // $(".editor-canvas").append(dom);
                // Making element Resizable

            };
        }
    }

    class Layout1{
        constructor(){
            let id = (new Date).getTime();
            let html = `
                    <div id="layout${id}" class="layout1">
                        <div class = "l1d1" style = "height:100%">
                            ${button_html.html}
                        </div>
                    </div>
            `;
            this.renderDiagram = function() {
                // dom includes the html,css code with draggable property
                let dom = $(html).css({
                    // "position": "absolute",
                    
                    // "height": position.height,
                    // "width": position.width,
                    // "border": "2px dashed #000 !important"

                })
                
                var a = document.getElementsByClassName("current")[0];
                $('#' + a.id).append(dom);
            };
        }
    }

    class Layout2{
        constructor(){
            let id = (new Date).getTime();
            let html = `
                    <div id="layout${id}" class="layout2">
                        <div class = "l1d1">
                            ${button_html.html}
                        </div>
                        <div class = "l1d2">
                            ${button_html.html}
                        </div>
                    </div>
            `;
            this.renderDiagram = function() {
                // dom includes the html,css code with draggable property
                let dom = $(html).css({
                    // "position": "absolute",
                    
                    // "height": position.height,
                    // "width": position.width,
                    // "border": "2px dashed #000 !important"

                })
                
                var a = document.getElementsByClassName("current")[0];
                $('#' + a.id).append(dom);
            };
        }
    }

    class Layout3{
        constructor(){
            let id = (new Date).getTime();
            let html = `
                    <div id="layout${id}" class="layout3">
                        <div class = "l1d1">${button_html.html}</div>
                        <div class = "l1d2">${button_html.html}</div>
                        <div class = "l1d3">${button_html.html}</div>
                    </div>
            `;
            this.renderDiagram = function() {
                // dom includes the html,css code with draggable property
                let dom = $(html).css({
                    // "position": "absolute",
                    
                    // "height": position.height,
                    // "width": position.width,
                    // "border": "2px dashed #000 !important"

                })
                
                var a = document.getElementsByClassName("current")[0];
                $('#' + a.id).append(dom);
            };
        }
    }

    class Layout4{
        constructor(){
            let id = (new Date).getTime();
            let html = `
                    <div id="layout${id}" class="layout4">
                        <div class = "l1d1">${button_html.html}</div>
                        <div class = "l1d2">${button_html.html}</div>
                        <div class = "l1d3">${button_html.html}</div>
                        <div class = "l1d4">${button_html.html}</div>
                    </div>
            `;
            this.renderDiagram = function() {
                // dom includes the html,css code with draggable property
                let dom = $(html).css({
                    // "position": "absolute",
                    
                    // "height": position.height,
                    // "width": position.width,
                    // "border": "2px dashed #000 !important"

                })
                
                var a = document.getElementsByClassName("current")[0];
                $('#' + a.id).append(dom);
            };
        }
    }
    
    function TextboxFunction(collg = null, colmd = null, colsm = null, colxs = null, message="Type Something Here...", height = null, width = null){
        const textBox = new Textbox(collg, colmd, colsm, colxs, message);
        
        textBox.renderDiagram();
    
        $('.textdiv').hover(function(e) {
            $(e.currentTarget).find('.text-actions').css({
                'display': 'block'
            });
            $(this).css({
                'border': '1px solid grey'
            })
    
        }, function() {
            $('.text-actions').css({
                'display': 'none'
            });
            $(this).css({
                'border': 'none'
            })
            $('.messageText').css({
                'border': 'none'
            })
        });
        
        $('.fa-trash').click(function(e) {
            $('#' + e.currentTarget.id).parent().parent().remove();
            //  alert('btn clickd')
        });
        $('.textdiv').resizable({
            containment: $('#tabs-for-download'),
            grid: [20, 20],
            autoHide: true,
            minWidth: 75,
            minHeight: 25
        });
        $('.note-editing-area').on('focusin', function(e){
            $(e.currentTarget).parent().find('.note-popover .popover-content,.panel-heading.note-toolbar').css('display','block')
        });
          
          var resultsSelected = false;
          $(".note-toolbar > .note-btn-group").hover(
              function () { resultsSelected = true; },
              function () { 
                resultsSelected = false; 
                // if(!$('.note-editing-area').has(':focus')){
                //   $('.note-popover .popover-content,.panel-heading.note-toolbar').css('display','none')
                // }
              }
          );
          $('.note-editing-area').on('focusout', function(e){
            if(!resultsSelected){
              $('.panel-heading.note-toolbar').css('display','none')
            }
          });
    }

    function Layout1Function(){
        const layout1 = new Layout1();
        
        layout1.renderDiagram();
    }

    function Layout2Function(){
        const layout2 = new Layout2();
        
        layout2.renderDiagram();
    }

    function Layout3Function(){
        const layout3 = new Layout3();
        
        layout3.renderDiagram();
    }

    function Layout4Function(){
        const layout4 = new Layout4();
        
        layout4.renderDiagram();
    }

    $(".draggable").draggable({
        helper: "clone",
        revert: "invalid",
        cursor: "pointer",
        cursorAt: {
            top: 56,
            left: 56
        },
        grid: [ 20, 20 ]
    });

    // $(".editor-canvas").droppable({
    //     drop: function(event, ui){
    //         dropfunction(event,ui)
    //     }
    // });

    function dropfunction(event, ui) {
        if (ui.helper.hasClass('textbox')) {
            TextboxFunction();
        }
        else if (ui.helper.hasClass('layouticon1')) {
            Layout1Function();
        }
        else if (ui.helper.hasClass('layouticon2')) {
            Layout2Function();
        }
        else if (ui.helper.hasClass('layouticon3')) {
            Layout3Function();
        }
        else if (ui.helper.hasClass('layouticon4')) {
            Layout4Function();
        }
    } 

    $("#tabs-for-download").droppable({
        drop: function(event, ui){
            dropfunction(event,ui)
        }
    });
});