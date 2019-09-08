$(document).ready(function() {

    function display(){
        $('#chaptertitle').text(chaptertitle);
        $.each(data.pages, function(key, value){
            $.each(value, function(count){
                
                // -------------------------------
                $.each(value[count], function(div,div_value){
                    if(div == 'textdiv'){
                        $.each(div_value, function(css, css_value){
                            css_string = JSON.stringify(css_value)
                            $('#tab'+key).append(`
                                <div class="textdiv ui-draggable" style = "position: absolute; top: ${css_value.tops}; left: ${css_value.left}; border: 1px solid grey;">
                                    ${css_value.content} 
                                </div>
                            `);
                            
                        });
                    }
                    if(div == 'pic'){
                        $.each(div_value, function(css, css_value){
                            css_string = JSON.stringify(css_value)
                            $('#tab'+key).append(`
                                <div style = ${css_string}>
                                </div>
                            `);
                        });
                    }
                });
            });
            
        });
    }
    display();
    
    // title click function
    $(".tlimit").on("click", function() {
        $("#title_id").css({
            'display': 'block'
        });
    });

    // save button click function
    $("#save_btn").on("click", function(e) {
        e.preventDefault();
        var title = $("#main_title").val();
        $(".tlimit").html(title);
        $("#title_id").css({
            'display': 'none'
        });
    });

    $("#close1").on("click", function() {
        $("#title_id").css({
            'display': 'none'
        });
    });

    let sidebarWidth = $(".sidebar").width(); // get width of sidebar

    // Making sidebar tools draggable
    $(".draggable").draggable({
        helper: "clone",
        revert: "invalid",
        cursor: "pointer",
        cursorAt: {
            top: 56,
            left: 56
        }
    });

    function dropfunction(event, ui) {
        if (ui.helper.hasClass('textbox')) {
            const textBox = new Textbox(ui.helper.position().top,
                ui.helper.position().left - sidebarWidth);
        
            textBox.renderDiagram();
        
            $('.textdiv').hover(function() {
                $('.text-actions').css({
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
            })
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.messageText').resizable({
                containment: $('#tabs-for-download'),
                grid: [20, 20],
                autoHide: true,
                minWidth: 75,
                minHeight: 25
            });
        } else if (ui.helper.hasClass('picture')) {
            const Pic = new picture(
                ui.helper.position().top,
                ui.helper.position().left - sidebarWidth);
            Pic.renderDiagram();
        
            $('.fa-upload').click(function(e) {
                trigger = parseInt(e.target.id) + 1;
                $('#' + trigger).trigger('click');
            });
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.pic').on('dragover', function(e) {
                e.stopPropagation();
                e.preventDefault();
                //   $(this).css('border',"2px solid #39F")
            })
        
            $('.pic').on('drop', function(e) {
                e.stopPropagation();
                e.preventDefault();
                const files = e.originalEvent.dataTransfer.files;
                var file = files[0];
                upload(file);
            });
        
            function upload(file) {
                const data = new FormData();
                data.append("fileName", file);
                $.ajax({
                    url: save_file_url, //image url defined in chapterbuilder.html which points to WebApp/static/chapterPageBuilder/images
                    data: data,
                    contentType: false,
                    processData: false,
                    method: 'POST',
                    type: 'POST',
                    success: function(data) {
                        // console.log(data);
                        div.css({
                            'background-image': 'url('+load_file_url+'/' + file.name + '")',
                            'background-repeat': 'no-repeat',
                            'background-size': 'contain',
                            'background-position': 'center',
                            'border': '0'
                        });
                    }
                });
                let div = $('#picture-drag').parent().parent();
                $('#picture-drag').css({
                    'display': 'none'
                })
                

                $(div).hover(function() {
                    $(this).css("border", "1px solid red");
                }, function() {
                    $(this).css("border", '0')
                })

                $('.pic').resizable({
                    containment: $('.editor-canvas'),
                    grid: [20, 20],
                    autoHide: true,
                    minWidth: 150,
                    minHeight: 150
                });

            }

            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        let div = $(input).parent().parent().parent();
                        // console.log(div);
                        var data = new FormData();
                        // var count = 0
                        // console.log(input.files);
                        $.each(input.files, function(i, file) {
                            // console.log(Math.round((file.size / 1024))) // get image size
                            data.append('file-' + i, file);
                            // count++;
                        });
                        // data.append('count', count);
                        data.append('chapterID', chapterID);
                        data.append('courseID', courseID);
                        // console.log("imageuploadfromhere")
                        $.ajax({
                            url: save_file_url,
                            data: data,
                            contentType: false,
                            processData: false,
                            enctype: 'multipart/form-data',
                            method: 'POST',
                            type: 'POST',
                            success: function(data) {
                                // console.log(data);
                                div.css({
                                  'background-image': 'url('+load_file_url+'/'+input.files[0].name+')',
                                  'background-repeat': 'no-repeat',
                                  'background-size': 'contain',
                                  'background-position': 'center',
                                  'border': '0'
                                });
                            },
                            error: function(data, status, errorThrown) {
                                alert(data.responseJSON.message);
                             }
                        });

                        $('#picture-drag').css({
                            'display': 'none'
                        })
                        
                        $(div).hover(function() {
                            $(this).css("border", "1px solid red");
                        }, function() {
                            $(this).css("border", '0')
                        })

                        $('.pic').resizable({
                            containment: $('.editor-canvas'),
                            grid: [20, 20],
                            autoHide: true,
                            minWidth: 150,
                            minHeight: 150
                        });
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }

            $(".imgInp").change(function(e) {
                readURL(this);

            });
            //object of video component
        } else if (ui.helper.hasClass('video')) {
            const Videos = new video(ui.helper.position().top,
                ui.helper.position().left - sidebarWidth);
            Videos.renderDiagram();
        
            $('.fa-upload').click(function(e) {
                trigger = parseInt(e.target.id) + 1;
                $('#' + trigger).trigger('click');
            });
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.video-div').on('dragover', function(e) {
                e.stopPropagation();
                e.preventDefault();
            })
        
            $('.video-div').on('drop', function(e) {
                e.stopPropagation();
                e.preventDefault();
                $(this).resizable({
                    containment: $('.editor-canvas'),
                    grid: [20, 20],
                    autoHide: true,
                    minWidth: 150,
                    minHeight: 150
                });
        
                $(this).css({
                    'padding': '5px'
                })
        
                const files = e.originalEvent.dataTransfer.files;
                var file = files[0];
                upload(file);
            });
        
            function upload(file) {
                var data = new FormData();
        
                data.append("FileName", file);
        
                $.ajax({
                    xhr: function() {
                        var xhr = new window.XMLHttpRequest();
        
                        xhr.upload.addEventListener("progress", function(evt) {
                            $('#progress-bar').css("display", "block");
        
                            if (evt.lengthComputable) {
                                var percentComplete = evt.loaded / evt.total;
                                percentComplete = parseInt(percentComplete * 100);
                                console.log(percentComplete);
                                $('#progress-bar-fill').css('width', percentComplete + '%');
        
                                if (percentComplete === 100) {
                                    $('#progress-bar').css("display", "none");
                                    let div = $('#video-drag').parent().parent();
                                    $('#video-drag').css({
                                        'display': 'none'
                                    });
        
                                    div.append(`
                                <video width="400" height="200" controls>
                                <source src="../uploads/${file.name}" type="video/mp4">
                                 Your browser does not support the video tag.
                              </video>
                          `);
        
                                    $(div).hover(function() {
                                        $(this).css("border", "1px solid red");
                                    }, function() {
                                        $(this).css("border", '0')
                                    })
        
                                    $('.pic').resizable({
                                        containment: $('.editor-canvas'),
                                        grid: [20, 20],
                                        autoHide: true,
                                        minWidth: 150,
                                        minHeight: 150
                                    });
                                    console.log(file.name);
                                }
        
                            }
                        }, false);
        
                        return xhr;
                    },
                    url: '/index',
                    data: data,
                    contentType: false,
                    processData: false,
                    method: 'POST',
                    type: 'POST',
                    success: function(data) {
                        console.log(data);
                    }
        
                });
        
            }
        
            function readURL(input) {
        
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        let div = $(input).parent().parent().parent();
        
                        var data = new FormData();
                        $.each($('.video-form')[0].files, function(i, file) {
                            data.append('file-' + i, file);
                        });
        
                        $.ajax({
        
                            url: '/index',
                            data: data,
                            contentType: false,
                            processData: false,
                            method: 'POST',
                            type: 'POST',
                            success: function(data) {
                                console.log(data);
                            },
                            xhr: function() {
                                var xhr = new window.XMLHttpRequest();
        
                                xhr.upload.addEventListener("progress", function(evt) {
                                    $('#progress-bar').css("display", "block");
        
                                    if (evt.lengthComputable) {
                                        var percentComplete = evt.loaded / evt.total;
                                        percentComplete = parseInt(percentComplete * 100);
                                        console.log(percentComplete);
                                        $('#progress-bar-fill').css('width', percentComplete + '%');
        
                                        if (percentComplete === 100) {
                                            $('#progress-bar').css("display", "none");
                                            let div = $('#video-drag').parent().parent();
                                            $('#video-drag').css({
                                                'display': 'none'
                                            });
        
                                            div.append(`
                                            <video width="400" height="200" controls>
                                            <source src="../uploads/${input.files[0].name}" type="video/mp4">
                                             Your browser does not support the video tag.
                                          </video>
                                      `);
        
                                            $(div).hover(function() {
                                                $(this).css("border", "1px solid red");
                                            }, function() {
                                                $(this).css("border", '0')
                                            })
        
                                            $('.pic').resizable({
                                                containment: $('.editor-canvas'),
                                                grid: [20, 20],
                                                autoHide: true,
                                                minWidth: 150,
                                                minHeight: 150
                                            });
                                            console.log(file.name);
                                        }
        
                                    }
                                }, false);
        
                                return xhr;
                            }
        
                        });
        
                        $('#video-drag').css({
                            'display': 'none'
                        });
        
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }
        
            $(".video-form").change(function(e) {
        
                readURL(this);
        
            });
        
        } else if (ui.helper.hasClass('buttons')) {
            const btns = new Button(ui.helper.position().top,
                ui.helper.position().left - sidebarWidth);
        
            btns.renderDiagram();
        
            const div1 = $('i').parent();
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
                //  alert('btn clickd')
            });
        
            $('.fa-link').bind("click", function(e) {
                let argument = prompt("Enter a Link here...");
                if (argument == null || argument == "") {
                    return console.log("cancled pressed")
                } else {
                    var btn_id = parseInt(e.currentTarget.id) + 1
                    $('#' + btn_id).attr({
                        "href": `${argument}`
                    })
                }
        
            });
        
            $('.btn').resizable({
                containment: $('.editor-canvas'),
                grid: [20, 20],
                autoHide: true,
                minWidth: 50,
                minHeight: 30,
            });
        
        } else if (ui.helper.hasClass('grid')) {
            const grids = new GridLayout();
            grids.renderDiagram();
        
            // ===for picture inside first grid====
        
            $('.fa-upload').click(function(e) {
                trigger = parseInt(e.target.id) + 1;
                $('#' + trigger).trigger('click');
            });
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.pic').on('dragover', function(e) {
                e.stopPropagation();
                e.preventDefault();
                //   $(this).css('border',"2px solid #39F")
            })
        
            $('.pic').on('drop', function(e) {
                e.stopPropagation();
                e.preventDefault();
                const files = e.originalEvent.dataTransfer.files;
                var file = files[0];
                upload(file);
        
            });
        
            function upload(file) {
                const data = new FormData();
                data.append("fileName", file);
                $.ajax({
                    url: '/index',
                    data: data,
                    contentType: false,
                    processData: false,
                    method: 'POST',
                    type: 'POST',
                    success: function(data) {
                        console.log(data);
                    }
        
                });
                let div = $('#picture-drag').parent().parent();
                $('#picture-drag').css({
                    'display': 'none'
                })
                div.css({
                    'background-image': 'url("../uploads/' + file.name + '")',
                    'background-repeat': 'no-repeat',
                    'background-size': 'contain',
                    'background-position': 'center',
                    'border': '0'
                });
        
                $(div).hover(function() {
                    $(this).css("border", "1px solid red");
                }, function() {
                    $(this).css("border", '0')
                })
        
                $('.pic').resizable({
                    containment: $('.editor-canvas'),
                    grid: [20, 20],
                    autoHide: true,
                    minWidth: 150,
                    minHeight: 150
                });
        
            }
        
            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        let div = $(input).parent().parent().parent();
                        // console.log(div);
                        var data = new FormData();
                        $.each($('.imgInp')[0].files, function(i, file) {
                            data.append('file-' + i, file);
                        });
                        console.log(data);
                        $.ajax({
                            url: '/index',
                            data: data,
                            contentType: false,
                            processData: false,
                            method: 'POST',
                            type: 'POST',
                            success: function(data) {
                                console.log(data);
                            }
        
                        });
        
                        $('#picture-drag').css({
                            'display': 'none'
                        })
        
                        div.css({
                            'background-image': 'url("../uploads/' + input.files[0].name + '")',
                            'background-repeat': 'no-repeat',
                            'background-size': 'contain',
                            'background-position': 'center',
                            'border': '0'
                        });
                        $(div).hover(function() {
                            $(this).css("border", "1px solid red");
                        }, function() {
                            $(this).css("border", '0')
                        })
        
                        $('.pic').resizable({
                            containment: $('.editor-canvas'),
                            grid: [20, 20],
                            autoHide: true,
                            minWidth: 150,
                            minHeight: 150
                        });
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }
        
            $(".imgInp").change(function(e) {
                readURL(this);
        
            });
        
            // ===============for textbox inside grid-1============
        
            $('.textdiv').hover(function() {
                $('#text-actions').css({
                    'display': 'block'
                });
                $(this).css({
                    'border': '1px solid grey'
                })
        
            }, function() {
                $('#text-actions').css({
                    'display': 'none'
                });
                $(this).css({
                    'border': 'none'
                })
                $('.messageText').css({
                    'border': 'none'
                })
            })
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.messageText').resizable({
                containment: $('.editor-canvas'),
                grid: [20, 20],
                autoHide: true,
                minWidth: 250,
                minHeight: 250
            });
        
        } else if (ui.helper.hasClass('grid-1')) {
            const grids = new GridLayout1();
            grids.renderDiagram();
        
            $('.fa-upload').click(function(e) {
                trigger = parseInt(e.target.id) + 1;
                $('#' + trigger).trigger('click');
            });
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.pic').on('dragover', function(e) {
                e.stopPropagation();
                e.preventDefault();
                //   $(this).css('border',"2px solid #39F")
            })
        
            $('.pic').on('drop', function(e) {
                e.stopPropagation();
                e.preventDefault();
                const files = e.originalEvent.dataTransfer.files;
                var file = files[0];
                upload(file);
        
            });
        
            function upload(file) {
                const data = new FormData();
                data.append("fileName", file);
                $.ajax({
                    url: '/index',
                    data: data,
                    contentType: false,
                    processData: false,
                    method: 'POST',
                    type: 'POST',
                    success: function(data) {
                        console.log(data);
                    }
        
                });
                let div = $('#picture-drag').parent().parent();
                $('#picture-drag').css({
                    'display': 'none'
                })
                div.css({
                    'background-image': 'url("../uploads/' + file.name + '")',
                    'background-repeat': 'no-repeat',
                    'background-size': 'contain',
                    'background-position': 'center',
                    'border': '0'
                });
        
                $(div).hover(function() {
                    $(this).css("border", "1px solid red");
                }, function() {
                    $(this).css("border", '0')
                })
        
                $('.pic').resizable({
                    containment: $('.editor-canvas'),
                    grid: [20, 20],
                    autoHide: true,
                    minWidth: 150,
                    minHeight: 150
                });
        
            }
        
            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        let div = $(input).parent().parent().parent();
                        // console.log(div);
                        var data = new FormData();
                        $.each($('.imgInp')[0].files, function(i, file) {
                            data.append('file-' + i, file);
                        });
                        console.log(data);
                        $.ajax({
                            url: '/index',
                            data: data,
                            contentType: false,
                            processData: false,
                            method: 'POST',
                            type: 'POST',
                            success: function(data) {
                                console.log(data);
                            }
        
                        });
        
                        $('#picture-drag').css({
                            'display': 'none'
                        })
        
                        div.css({
                            'background-image': 'url("../uploads/' + input.files[0].name + '")',
                            'background-repeat': 'no-repeat',
                            'background-size': 'contain',
                            'background-position': 'center',
                            'border': '0'
                        });
                        $(div).hover(function() {
                            $(this).css("border", "1px solid red");
                        }, function() {
                            $(this).css("border", '0')
                        })
        
                        $('.pic').resizable({
                            containment: $('.editor-canvas'),
                            grid: [20, 20],
                            autoHide: true,
                            minWidth: 150,
                            minHeight: 150
                        });
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }
        
            $(".imgInp").change(function(e) {
                readURL(this);
        
            });
        
            // ===============for textbox inside grid-1============
        
            $('.textdiv').hover(function() {
                $('#text-actions').css({
                    'display': 'block'
                });
                $(this).css({
                    'border': '1px solid grey'
                })
        
            }, function() {
                $('#text-actions').css({
                    'display': 'none'
                });
                $(this).css({
                    'border': 'none'
                })
                $('.messageText').css({
                    'border': 'none'
                })
            })
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.messageText').resizable({
                containment: $('.editor-canvas'),
                grid: [20, 20],
                autoHide: true,
                minWidth: 250,
                minHeight: 250
            });
        
        } else if (ui.helper.hasClass('title-slide')) {
            const title = new TitleSlide();
            title.renderDiagram();
        
            // ===for text in title slide===
        
            $('.textdiv').hover(function() {
                $('#text-actions').css({
                    'display': 'block'
                });
                $(this).css({
                    'border': '1px solid grey'
                })
        
            }, function() {
                $('#text-actions').css({
                    'display': 'none'
                });
                $(this).css({
                    'border': 'none'
                })
                $('.messageText').css({
                    'border': 'none'
                })
            })
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.messageText').resizable({
                containment: $('.editor-canvas'),
                grid: [20, 20],
                autoHide: true,
                minWidth: 250,
                minHeight: 250
            });
        
        } else if (ui.helper.hasClass('title-content-details')) {
            const titlecontent = new TitleContent();
            titlecontent.renderDiagram();
            // ==for text in title-content-details==
        
            $('.textdiv').hover(function() {
                $('#text-actions').css({
                    'display': 'block'
                });
                $(this).css({
                    'border': '1px solid grey'
                })
        
            }, function() {
                $('#text-actions').css({
                    'display': 'none'
                });
                $(this).css({
                    'border': 'none'
                })
                $('.messageText').css({
                    'border': 'none'
                })
            })
        
            $('.fa-trash').click(function(e) {
                $('#' + e.currentTarget.id).parent().parent().remove();
            });
        
            $('.messageText').resizable({
                containment: $('.editor-canvas'),
                grid: [20, 20],
                autoHide: true,
                minWidth: 250,
                minHeight: 250
            });
        
        } else if (ui.helper.hasClass('pdfVideo')) {
            const pdfVideolayout = new PdfVideoLayout();
            pdfVideolayout.renderDiagram();
        
        } else if (ui.helper.hasClass('tables')) {
            const tables = new Tables();
        
            tables.renderDiagram();
        
            // $("#table-dialog").attr("open","open");
            $('#table-dialog').css({
                'display': 'block'
            })
        
            $(".close").on("click", function() {
                $('#table-dialog').css({
                    'display': 'none'
                })
            })
        
            $("#ok").on("click", function(e) {
                e.preventDefault();
                var number_of_rows = $("#number_of_rows").val();
                var number_of_columns = $("#number_of_columns").val();
                var table_body = '<table id="tables_id" border="1" width="300px" height="300px">';
                for (var i = 0; i < number_of_rows; i++) {
                    table_body += '<tr>';
                    for (var j = 0; j < number_of_columns; j++) {
                        table_body += '<td>';
                        table_body += '<p contentEditable="true" >&nbsp; &nbsp;</p>';
                        table_body += '</td>';
                    }
                    table_body += '</tr>';
                }
                table_body += '</table>';
                $('.tableDiv').html(table_body);
                $("#table-dialog").css({
                    'display': 'none'
                });
        
            });
        
            // window.onclick = function(event) {
            //   if (event.target == modal) {
            //     modal.style.display = "none";
            //   }
            // }
        
        }
    }

    $(".editor-canvas").droppable({
        drop: function(event, ui){
            dropfunction(event,ui)
        }
    });

    $("#add-page-btn").on("click", function() {
        var num_tabs = $(".tabs-to-click ul li").length + 1;

        $(".tabs-to-click ul").append(

            `<li class="tabs-link pagenumber" onclick="openTab(event,'tab${num_tabs}')" >
               
            </li>`

        );
        $(".tabs").append(
            `<p id='tab${num_tabs}' style="display:none" class="tab-content-no droppable editor-canvas ui-droppable">
            
            </p>`
        );

        $(".editor-canvas").droppable({
            drop: function(event, ui){
                dropfunction(event,ui);
            }
        });
    });

    // ==================For TextBoxx================================

    class Textbox {
        constructor(top, left) {
            let id = (new Date).getTime();
            let position = {
                top, left
            };
            let html = `<div class='textdiv' >
                     <div id="text-actions" class = "text-actions">
                         <i class="fas fa-trash" id=${id}></i>
                         <i class="fas fa-arrows-alt" id="draghere" class="draghere"></i>
                     </div> 
                     <div id="editor" class="messageText" contenteditable> Type Something Here....</div>
                  </div>
                  `;
            this.renderDiagram = function() {
                // dom includes the html,css code with draggable property
                let dom = $(html).css({
                    "position": "absolute",
                    "top": position.top,
                    "left": position.left
                }).draggable({
                    //Constrain the draggable movement only within the canvas of the editor
                    containment: "#tabs-for-download",  // dragging beyond this <div> will not be possible
                    scroll: false,
                    grid: [50, 20],
                    cursor: "move",
                    handle: '#draghere'
                });

                var a = document.getElementsByClassName("current")[0];
                $('#' + a.id).append(dom);
                // $(".editor-canvas").append(dom);
                // Making element Resizable

            };
        }
    }

    // ===========================FOR PICTURE=====================================

    class picture {
        constructor(top, left) {
            let id = (new Date).getTime();
            let position = { top, left };
            let html =
            `<div class='pic'>
                <div id="pic-actions">
                    <i class="fas fa-trash" id=${id}></i>
                    <i class="fas fa-upload" id=${id}></i>
                </div>
                <div>
                    <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                    <input type='file' name="userImage" style="display:none" id=${id + 1} class="imgInp" />
                </form>
                <p id="picture-drag">drag and drop files here...</p>
                </div>
            </div>`

            this.RemoveElement = function () {
                return idss;
            }
            this.renderDiagram = function () {
            // dom includes the html,css code with draggable property

            let dom = $(html).css({
                "position": "absolute",
                "top": position.top,
                "left": position.left
            }).draggable({
                //Constraint   the draggable movement only within the canvas of the editor
                containment: "#tabs-for-download",
                scroll: false,
                cursor: "move",
                snap: ".gridlines",
                snapMode: 'inner',
                cursorAt: { bottom: 0 }
            });

            var a = document.getElementsByClassName("current")[0];
            // console.log(a);
            // console.log($('#' + a.id));
            $('#' + a.id).append(dom);
            // canvas.append(dom);
            };
        }
    }
    
     // ====================================For Video==============================

    class video {
        constructor(top, left) {
            let id = (new Date).getTime();
            let position = { top, left };
            let html =
                `<div class='video-div'>
                        <div id="video-actions">
                            <i class="fas fa-trash" id=${id}></i>
                            <i class="fas fa-upload" id=${id}></i>
                        </div>
                        <div>
                            <p id="video-drag">drag and drop video here...</p>
                            <div id="progress-bar">
                                <span id="progress-bar-fill"></span>
                            </div>
                            <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                            <input type='file' name="userImage" style="display:none" id=${id + 1} class="video-form" />
                        </form>
                        </div>
                    </div>`

            this.RemoveElement = function () {
                return idss;
            }
            this.renderDiagram = function () {
                // dom includes the html,css code with draggable property

                let dom = $(html).css({
                "position": "absolute",
                "top": position.top,
                "left": position.left
                }).draggable({
                //Constraint   the draggable movement only within the canvas of the editor
                containment: ".editor-canvas",
                scroll: false,
                cursor: "move",
                snap: ".gridlines",
                snapMode: 'inner',
                cursorAt: { bottom: 0 }
                });

                var a = document.getElementsByClassName("current")[0];
                $('#' + a.id).append(dom)
            };
        }
    }

    // =====================For Button==============================

    class Button {
        constructor(top, left) {
        let id = (new Date).getTime();
        let position = { top, left };
        let html = `
                        <div id="btn-div">
                            <div id="options">
                                <i class="fas fa-trash" id=${id}></i>
                                <i class="fas fa-link"   id=${id} ></i>
                                <i class="fas fa-arrows-alt" id="draghanle"></i>
                            
                            </div> 
                            <a class="btn" id=${id + 1}  target="_blank"  >Submit</a>
                        </div>
        
                `;
        this.renderDiagram = function () {
            // dom includes the html,css code with draggable property
            let dom = $(html).css({
            "position": "absolute",
            "top": position.top,
            "left": position.left
            }).draggable({
            //Constrain the draggable movement only within the canvas of the editor
            containment: ".editor-canvas",
            scroll: false,
            grid: [50, 20],
            cursor: "move",
            handle: '#draghanle'
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
            // canvas.append(dom);
            // Making element Resizable

        };
        }
    }

    // =====for grid system============

    class GridLayout {
        constructor(top, left) {
        let id = (new Date).getTime();
        let position = { top, left };
        let html = `
                        <div class="grid-container">
                            <div class="grid-header" > 
                            <div class='video-div'>
                            <div id="video-actions">
                                <i class="fas fa-trash" id=${id}></i>
                                <i class="fas fa-upload" id=${id}></i>
                            </div>
                            <div>
                                <p id="video-drag">drag and drop video here...</p>
                                <div id="progress-bar">
                                    <span id="progress-bar-fill"></span>
                                </div>
                                <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                                <input type='file' name="userImage" style="display:none" id=${id + 1} class="video-form" />
                            </form>
                            </div>
                        </div>
                            </div>
                            <div class="grid-body" >
                            <div class='textdiv' >
                                <div id="text-actions">
                                    <i class="fas fa-trash" id=${id}></i>
                                    <i class="fas fa-arrows-alt" id="draghere"></i>
                                </div> 
                                <div id="editor" class="messageText" contenteditable> 
                                    Type Something...
                                </div>
                            </div>
                            </div>
                        </div>
        
                `;
        this.renderDiagram = function () {
            // dom includes the html,css code with draggable property
            let dom = $(html).css({
            "position": "absolute",
            "top": 10,
            "left": 7,
            "padding": 16
            }).draggable({
            //Constrain the draggable movement only within the canvas of the editor
            containment: "#editor",
            scroll: false,
            grid: [150, 75],
            cursor: "move",
            handle: '#draghanle'
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom)
            // canvas.append(dom);
            // Making element Resizable

        };
        }
    }


    // ===============for GridLayout1=====================

    class GridLayout1 {
        constructor(top, left) {
        let id = (new Date).getTime();
        let position = { top, left };
        let html = `<div class="grid-container-1">
                            <div class="grid-section-left-1">
                            <div class='pic'>
                            <div id="pic-actions">
                                <i class="fas fa-trash" id=${id}></i>
                                <i class="fas fa-upload" id=${id}></i>
                            </div>
                            <div>
                                <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                                <input type='file' name="userImage" style="display:none" id=${id + 1} class="imgInp" />
                            </form>
                            <p id="picture-drag">drag and drop files here...</p>
                            </div>
                        </div>
                            </div>
                            <div class="grid-section-right-1">
                            <div class='textdiv' >
                                <div id="text-actions">
                                    <i class="fas fa-trash" id=${id}></i>
                                    <i class="fas fa-arrows-alt" id="draghere"></i>
                                </div> 
                                <div id="editor" class="messageText" contenteditable> 
                                    Type Something...
                                </div>
                            </div>
                            </div>
                        
                        </div>`;
        this.renderDiagram = function () {
            // dom includes the html,css code with draggable property
            let dom = $(html).css({
            "position": "absolute",
            "top": 20,
            "left": 7,
            "padding": 0
            }).draggable({
            //Constrain the draggable movement only within the canvas of the editor
            containment: "#editor",
            scroll: false,
            grid: [150, 75],
            cursor: "move",
            handle: '#draghanle'
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
            //  canvas.append(dom);
            // Making element Resizable

        };
        }
    }

    // =============================for title-slide========================================

    class TitleSlide {
        constructor(top, left) {
        let id = (new Date).getTime();
        let position = { top, left };
        let html = `
                        <div class="title-slide-container">
                        <div class="title-slide-head">
                            <div class="title-slide-left">
                            <div class='pic'>
                            <div id="pic-actions">
                                <i class="fas fa-trash" id=${id}></i>
                                <i class="fas fa-upload" id=${id}></i>
                            </div>
                            <div>
                                <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                                <input type='file' name="userImage" style="display:none" id=${id + 1} class="imgInp" />
                                </form>
                                <p id="picture-drag">drag and drop files here...</p>
                            </div>
                        </div>
                            </div>
                            <div class="title-slide-right">
                            <div class='pic'>
                    <div id="pic-actions">
                        <i class="fas fa-trash" id=${id}></i>
                        <i class="fas fa-upload" id=${id}></i>
                    </div>
                    <div>
                        <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                        <input type='file' name="userImage" style="display:none" id=${id + 1} class="imgInp" />
                        </form>
                        <p id="picture-drag">drag and drop files here...</p>
                    </div>
                </div>
                            </div>
                        </div>

                        <div class="title-slide-bottom">
                        <div class='textdiv' >
                        <div id="text-actions">
                            <i class="fas fa-trash" id=${id}></i>
                            <i class="fas fa-arrows-alt" id="draghere"></i>
                        </div> 
                        <div id="editor" class="messageText" contenteditable> 
                            Type Something...
                        </div>
                    </div>
                        </div>
                        </div>

        
                `;
        this.renderDiagram = function () {
            // dom includes the html,css code with draggable property
            let dom = $(html).css({
            "position": "absolute",
            "top": 20,
            "left": 25
            }).draggable({
            //Constrain the draggable movement only within the canvas of the editor
            containment: "#editor",
            scroll: false,
            grid: [150, 75],
            cursor: "move",
            handle: '#draghanle'
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
            //  canvas.append(dom);
            // Making element Resizable

        };
        }
    }

    // =========================title-content===============================


    class TitleContent {
    constructor(top, left) {
        let id = (new Date).getTime();
        let position = { top, left };
        let html = `
            <div class="title-content">
                <div class="title-content-heading">
                    <div class='textdiv' >
                        <div id="text-actions">
                            <i class="fas fa-trash" id=${id}></i>
                            <i class="fas fa-arrows-alt" id="draghere"></i>
                        </div> 
                    <div id="editor" class="messageText" contenteditable> Type Something Here....</div>
                    </div>
                    </div>
                
                <div class="title-content-info">
                    <div class='textdiv' >
                    <div id="text-actions">
                        <i class="fas fa-trash" id=${id}></i>
                        <i class="fas fa-arrows-alt" id="draghere"></i>
                    </div> 
                    <div id="editor" class="messageText" contenteditable> Type Something Here....</div>
                </div>
                </div>
            </div>
                `;
        this.renderDiagram = function () {
        // dom includes the html,css code with draggable property
        let dom = $(html).css({
            "position": "absolute",
            "top": 20,
            "left": 35
        }).draggable({
            //Constrain the draggable movement only within the canvas of the editor
            containment: "#editor",
            scroll: false,
            grid: [150, 75],
            cursor: "move",
            handle: '#draghandle'
        });

        var a = document.getElementsByClassName("current")[0];
        $('#' + a.id).append(dom)
        // canvas.append(dom);
        // Making element Resizable

        };
    }
    }

    class PdfVideoLayout {
    constructor(top, left) {
        let id = (new Date).getTime();
        let position = { top, left };
        let html = `
                    <div class="pdfvideoContainer">
                        <div class="pdf">
                        PDF will be shown here...
                        </div>

                        <div class="videos-content">
                        <div class='textdiv' >
                        <div id="text-actions">
                            <i class="fas fa-trash" id=${id}></i>
                            <i class="fas fa-arrows-alt" id="draghere"></i>
                        </div> 
                        <div id="editor" class="messageText" contenteditable> Type Something Here....</div>
                    </div>
                        </div>
                    </div>

        
                `;
        this.renderDiagram = function () {
        // dom includes the html,css code with draggable property
        let dom = $(html).css({
            "position": "absolute",
            "top": 20,
            "left": 35
        }).draggable({
            //Constrain the draggable movement only within the canvas of the editor
            containment: "#editor",
            scroll: false,
            grid: [150, 75],
            cursor: "move",
            handle: '#draghanle'
        });

        var a = document.getElementsByClassName("current")[0];
        $('#' + a.id).append(dom)
        // canvas.append(dom);
        // Making element Resizable

        };
    }

    }

    // =====================For Tables==============================

    class Tables {
        constructor(top, left) {
        let id = (new Date).getTime();
        let position = { top, left };
        let html = `
                        <div id="btn-div">
                            <div id="options">
                            <i class="fas fa-trash" id=${id}></i>
                            <i class="fas fa-arrows-alt" id="draghanle"></i>
                            </div> 
                        
                        <div  class="tableDiv" id="${id + 1}">

                        </div>
                            
                        </div>
    
                `;
        this.renderDiagram = function () {
            // dom includes the html,css code with draggable property
            let dom = $(html).css({
            "position": "absolute",
            "top": position.top,
            "left": position.left
            }).draggable({
            //Constrain the draggable movement only within the canvas of the editor
            containment: ".editor-canvas",
            scroll: false,
            grid: [50, 20],
            cursor: "move",
            handle: '#draghanle'
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom)
            //canvas.append(dom);
            // Making element Resizable

        };
        }
    }
});

function openTab(evt, tab_no) {

    tabcontent = document.getElementsByClassName("tab-content-no");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].className = tabcontent[i].className.replace("current", "");
    }
    tablinks = document.getElementsByClassName("tabs-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace("current", "");
    }

    document.getElementById(tab_no).style.display = "block";
    document.getElementById(tab_no).className += " current";
    evt.currentTarget.className += " current";

}

var colorList = ['000000', '993300', '333300', '003300', '003366', '000066', '333399', '333333',
    '660000', 'FF6633', '666633', '336633', '336666', '0066FF', '666699', '666666', 'CC3333', 'FF9933', '99CC33', '669966', '66CCCC', '3366FF', '663366', '999999', 'CC66FF', 'FFCC33', 'FFFF66', '99FF66', '99CCCC', '66CCFF', '993366', 'CCCCCC', 'FF99CC', 'FFCC99', 'FFFF99', 'CCffCC', 'CCFFff', '99CCFF', 'CC99FF', 'FFFFFF'
];
var picker = $('#color-picker');

for (var i = 0; i < colorList.length; i++) {
    picker.append('<li class="color-item" data-hex="' + '#' + colorList[i] + '" style="background-color:' + '#' + colorList[i] + ';"></li>');
}

$('body').click(function() {
    picker.fadeOut();
});

$('.call-picker').click(function(event) {
    event.stopPropagation();
    picker.fadeIn();
    picker.children('li').hover(function() {
        var codeHex = $(this).data('hex');

        $('.color-holder').css('background-color', codeHex);
        $('#pickcolor').val(codeHex);
    });
});
// Move caret back to 
function placeCaretAtEnd(el) {
    el.focus();
    if (typeof window.getSelection != "undefined" && typeof document.createRange != "undefined") {
        var range = document.createRange();
        range.selectNodeContents(el);
        range.collapse(false);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    } else if (typeof document.body.createTextRange != "undefined") {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(el);
        textRange.collapse(false);
        textRange.select();
    }
}

// Clean HTML tags using sanitize-html
function cleanHtml() {
    let value = $("#editor").html();
    let clean = sanitizeHtml(value, {
        allowedTags: ['div', 'blockquote', 'b', 'strong', 'i', 'em', 'ul', 'ol', 'li'],
        allowedAttributes: {
            'blockquote': ['style']
        }
    });

    let cleanValue = clean.trim();
    setContent();
}

// Paste from MS Word    *CREDIT: https://gist.github.com/sbrin/6801034
(function($) {
    $.fn.msword_html_filter = function(options) {
        let settings = $.extend({}, options);

        function word_filter(editor) {
            let content = editor.html();

            // Word comments like conditional comments etc
            content = content.replace(/<!--[\s\S]+?-->/gi, '');

            // Remove comments, scripts (e.g., msoShowComment), XML tag, VML content,
            // MS Office namespaced tags, and a few other tags
            content = content.replace(/<(!|script[^>]*>.*?<\/script(?=[>\s])|\/?(\?xml(:\w+)?|img|meta|link|style|\w:\w+)(?=[\s\/>]))[^>]*>/gi, '');

            // Convert <s> into <strike> for line-though
            content = content.replace(/<(\/?)s>/gi, "<$1strike>");

            // Replace nbsp entites to char since it's easier to handle
            //content = content.replace(/&nbsp;/gi, "\u00a0");
            content = content.replace(/&nbsp;/gi, ' ');

            // Convert <span style="mso-spacerun:yes">___</span> to string of alternating
            // breaking/non-breaking spaces of same length
            content = content.replace(/<span\s+style\s*=\s*"\s*mso-spacerun\s*:\s*yes\s*;?\s*"\s*>([\s\u00a0]*)<\/span>/gi, function(str, spaces) {
                return spaces.length > 0 ? spaces.replace(/./, " ").slice(Math.floor(spaces.length / 2)).split("").join("\u00a0") : '';
            });

            editor.html(content);

            // Parse out list indent level for lists
            $('p', editor).each(function() {
                let str = $(this).attr('style');
                let matches = /mso-list:\w+ \w+([0-9]+)/.exec(str);
                if (matches) {
                    $(this).data('_listLevel', parseInt(matches[1], 10));
                }
            });

            // Parse Lists
            let last_level = 0;
            let pnt = null;
            $('p', editor).each(function() {
                let cur_level = $(this).data('_listLevel');
                if (cur_level != undefined) {
                    let txt = $(this).text();
                    let list_tag = '<ul></ul>';
                    if (/^\s*\w+\./.test(txt)) {
                        let matches = /([0-9])\./.exec(txt);
                        if (matches) {
                            let start = parseInt(matches[1], 10);
                            list_tag = start > 1 ? '<ol start="' + start + '"></ol>' : '<ol></ol>';
                        } else {
                            list_tag = '<ol></ol>';
                        }
                    }

                    if (cur_level > last_level) {
                        if (last_level == 0) {
                            $(this).before(list_tag);
                            pnt = $(this).prev();
                        } else {
                            pnt = $(list_tag).appendTo(pnt);
                        }
                    }
                    if (cur_level < last_level) {
                        for (let i = 0; i < last_level - cur_level; i++) {
                            if (window.CP.shouldStopExecution(0)) break;
                            pnt = pnt.parent();
                        }
                        window.CP.exitedLoop(0);
                    }
                    $('span:first', this).remove();
                    pnt.append('<li>' + $(this).html().replace(/\d+\./g, '') + '</li>');
                    $('b:empty').remove();
                    $(this).remove();
                    last_level = cur_level;
                } else {
                    last_level = 0;
                }
            });

            $('[style]', editor).removeAttr('style');
            $('[align]', editor).removeAttr('align');
            $('span', editor).replaceWith(function() {
                return $(this).contents();
            });
            $('span:empty', editor).remove();
            $("[class^='Mso']", editor).removeAttr('class');
            $('p:empty', editor).remove();
        }

        return this.each(function() {
            let self = this;
            $(self).on('keyup paste', function() {

                setTimeout(function() {
                    let content = $(self).html();
                    /class="?Mso|style="[^"]*\bmso-|style='[^'']*\bmso-|w:WordDocument/i.test(content) ? word_filter($(self)) : cleanHtml();
                }, 400);
            });
        });
    };
})(jQuery);

$(function() {
    $('#editor').msword_html_filter();
});

function setContent() {
    let value = $(this).html();

    let el = $("#editor").get(0);
    placeCaretAtEnd(el);
}

//### EVENTS/ACTIONS ###//

//execCommand(aCommandName, aShowDefaultUI, aValueArgument)
function runCommand(el, commandName, arg) {
    if (commandName === "createLink") {
        let argument = prompt("Insert link:");
        if ((argument == null || argument == "")) {
            console.log("sorry cancled")
        } else {
            $(this).on('click', receiveURL);
        }

        document.execCommand(commandName, false, argument);
    } else {
        document.execCommand(commandName, false, arg);
    }
    $("#editor").focus();
    return false;
}

// Capture wysiwyg val and assign to textarea val
// $("#editor").keyup(function() {
//   let value = $(this).html();
//   $("#messageText").val(value);  
// });

// Show submitted data
$('#submit').click(function(e) {
    e.preventDefault();
    let content = $("#editor").html().trim();
    alert("VALUE SUBMITTED: \n" + content);
});