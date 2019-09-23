$(document).ready(function() {
    $('#loadingDiv').hide();
    // ==================For TextBoxx================================

    class Textbox {
        constructor(top=0, left=0, height=null ,width = null, message="Type Something Here...") {
            console.log(top, left,height,width)
            let id = (new Date).getTime();
            let position = {
                top, left, height, width
            };
            let html = `<div class='textdiv'  >
                     <div id="text-actions"   class = "text-actions">
                         <i class="fas fa-trash" id=${id}></i>
                         <i class="fas fa-arrows-alt" id="draghere" ></i>
                     </div> 
                     <div id="editor" class="messageText" contenteditable> ${message}</div>
                  </div>
                  `;
            this.renderDiagram = function() {
                // dom includes the html,css code with draggable property
                let dom = $(html).css({
                    "position": "absolute",
                    "top": position.top,
                    "left": position.left,
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
                // $(".editor-canvas").append(dom);
                // Making element Resizable

            };
        }
    }

    // ===========================FOR PICTURE=====================================

    class picture {
        constructor(top, left, pic=null, width=null, height=null) {
            let id = (new Date).getTime();
            let position = { top, left, width, height };
            let message = "";
            if(pic == null){
                message = "Drag and drop images here..."
            }
            let html =
            `<div class='pic' style='background-image:${pic}; background-repeat: no-repeat; background-size: contain; background-position: center; border: 0'>
                <div id="pic-actions">
                    <i class="fas fa-trash" id=${id}></i>
                    <i class="fas fa-upload" id=${id}></i>
                </div>
                <div>
                    <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                    <input type='file' accept="image/*" name="userImage" style="display:none" id=${id + 1} class="imgInp" />
                </form>
                <p id="picture-drag">${message}</p>
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
                "left": position.left,
                "width": position.width,
                "height": position.height
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
        constructor(top, left, link=null, height=null, width=null) {
            let id = (new Date).getTime();
            let position = { top, left, height, width };
            let videoobj;
            let message = ""
            if(link!=null){
                videoobj = `<div id='${link}'><div><script>
                var options = {
                    url: '${link}',
                    width: "${width}",
                    height: "${height}"
                };
              
                var videoPlayer = new Vimeo.Player('${link}', options);
              </script>`
            }else{
                message = "drag and drop video here...";
                videoobj = "";
            }
            let html =
                `<div class='video-div'>
                    <div id="video-actions">
                        <i class="fas fa-trash" id=${id}></i>
                        <i class="fas fa-upload" id=${id}></i>
                    </div>
                    <div>
                        <p id="video-drag">${message}</p>
                        
                        <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                        <input type='file' name="userImage" accept="video/*" style="display:none" id=${id + 1} class="video-form" />
                        </form>
      
                        <div class="progress">
                            <div id="progress-bar" class="progress-bar progress-bar-striped" role="progressbar" style="width: 0%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                                ${videoobj}
                    </div>
                </div>`

            //     <div id="progress-bar">
            //     <span id="progress-bar-fill"></span>
            // </div>


            this.RemoveElement = function () {
                return idss;
            }
            this.renderDiagram = function () {
                // dom includes the html,css code with draggable property

                let dom = $(html).css({
                    "position": "absolute",
                    "top": position.top,
                    "left": position.left,
                    "height": position.height,
                    "width": position.width
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
                $('#' + a.id).append(dom)
            };
        }
    }

    // =====================For Button==============================

    class Button {
        constructor(top, left, link=null, height=null, width=null) {
        let id = (new Date).getTime();
        let position = { top, left, height, width };
        let button_link = ""
        if(link != null){
            button_link = 'href = '+ link
        }
        let html = `
                        <div class="btn-div">
                            <div class="options">
                                <i class="fas fa-trash" id=${id}></i>
                                <i class="fas fa-link"   id=${id} ></i>
                                <i class="fas fa-arrows-alt" id="draghanle"></i>
                            
                            </div> 
                            <a class="btn" ${button_link} id=${id + 1}  target="_blank"  >Submit</a>
                        </div>
        
                `;

                // href = ${link}
        this.renderDiagram = function () {
            // dom includes the html,css code with draggable property
            let dom = $(html).css({
            "position": "absolute",
            "top": position.top,
            "left": position.left,
            "height": position.height,
            "width": position.width,
            }).draggable({
            //Constrain the draggable movement only within the canvas of the editor
            containment: "#tabs-for-download",
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


    // ====For PDF======
    class PDF {
        constructor(top, left, link=null, height=null, width=null) {
        let id = (new Date).getTime();
        var pdfobj;
        let position = { top, left, height, width };
        if(link!=null){
            pdfobj = `
                <object data="${link}" type="application/pdf" width="100%" height="100%">
                    alt : <a href="${link}"></a>
                </object>
            `
        }else{
            pdfobj = "";
        }
        let html = `
            <div class='pdf'>
                <div id="pdf-actions1">
                    <i class="fas fa-trash" id=${id}></i>
                    <i class="fas fa-upload" id=${id}></i>
                </div>
                <div>
                    <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                    <input type='file' accept="application/pdf"  style="display:none" id=${id + 1}  multiple="multiple" class="pdfInp" />
                    </form>
                    <p id="pdf-drag" placeholder="drag and drop files here..."></p>
                ${pdfobj}
                </div>
            </div>
        `;
        this.RemoveElement = function () {
            return idss;
        }
        this.renderDiagram = function () {
            // dom includes the html,css code with draggable property
            let dom = $(html).css({
            "position": "absolute",
            "top": position.top,
            "left": position.left,
            "height": position.height,
            "width": position.width
            }).draggable({
                //Constrain the draggable movement only within the canvas of the editor
                containment: "#tabs-for-download",
                scroll: false,
                grid: [50, 20],
                cursor: "move",
                snap: ".gridlines",
                snapMode: 'inner',
                cursorAt: { bottom: 0 }
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
            // canvas.append(dom);
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
// ====================== End of initializing elements ========================
    
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
    let toolbarheight = $('.editor-toolbar').height();
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

    function TextboxFunction(top=null, left=null, height="10%", width="20%", message="Type Something Here..."){
        const textBox = new Textbox(top, left, height, width, message);
        
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
            });
        
            $('.textdiv').resizable({
                containment: $('#tabs-for-download'),
                grid: [20, 20],
                autoHide: true,
                minWidth: 75,
                minHeight: 25
            });
    }

    function PictureFunction(top=null, left=null, pic = null, width=null, height=null){
        const Pic = new picture(
            top,
            left,
            pic,
            width,height);
        Pic.renderDiagram();
    
        $('.fa-upload').click(function(e) {
            trigger = parseInt(e.target.id) + 1;
            $('#' + trigger).trigger('click');
        });

        $('.fa-trash').click(function(e) {
            $('#' + e.currentTarget.id).parent().parent().remove();
            //  alert('btn clickd')
        });

        $('.pic').resizable({
            containment: $('#tabs-for-download'),
            grid: [20, 20],
            autoHide: true,
            minWidth: 150,
            minHeight: 150
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
            data.append("file-0", file);
            data.append('chapterID', chapterID);
            data.append('courseID', courseID);
            data.append('type', 'pic');
            $.ajax({
                url: save_file_url, //image url defined in chapterbuilder.html which points to WebApp/static/chapterPageBuilder/images
                data: data,
                contentType: false,
                processData: false,
                method: 'POST',
                type: 'POST',
                beforeSend: function() {
                    div.append(`<div class="loader" id="loadingDiv"></div>`)
                    $('#loadingDiv').show();
                }, 
                error: function(errorThrown){
                    alert("Failed to upload PDF")
                    div.find('#loadingDiv').remove();
                },
                success: function(data) {
                    div.find('p').text("");
                    div.find('#loadingDiv').remove();
                    div.css({
                        'background-image': 'url('+load_file_url+'/' + file.name + ')',
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
            let div = $('#picture-drag').parent().parent();
            $('#picture-drag').css({
                'display': 'none'
            })
            

            $(div).hover(function() {
                $(this).css("border", "1px solid red");
            }, function() {
                $(this).css("border", '0')
            })
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
                    });
                    // data.append('count', count);
                    data.append('type', 'pic');
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
                        beforeSend: function() {
                            div.append(`<div class="loader" id="loadingDiv"></div>`)
                            $('#loadingDiv').show();
                        }, 
                        error: function(errorThrown){
                            alert("Failed to upload PDF")
                            div.find('#loadingDiv').remove();
                        },
                        success: function(data) {
                            console.log(div)
                            div.find('#loadingDiv').remove();
                            div.find('p').text("");
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
    }

    function ButtonFuction(top=null, left=null, link=null, height=null, width=null){
        const btns = new Button(top, left, link, height, width);
        
        btns.renderDiagram();

        $('.btn').attr('contentEditable', true);

        $('.btn').on('click',function(){
            alert('say me more!!')
        })
    
        const div1 = $('i').parent();
    
        $('.fa-trash').click(function(e) {
            $('#' + e.currentTarget.id).parent().parent().remove();
            //  alert('btn clickd')
        });

        // $(".options").hover(function(){
        //     $('.options').css({
        //         'display':'block'
        //     }) 
        // })
    
        $('.fa-link').bind("click", function(e) {
            let argument = prompt("Enter a Link here...");
            if (argument == null || argument == "") {
                return console.log("cancled pressed")
            } else {
                var btn_id = parseInt(e.currentTarget.id) + 1
                $('#' + btn_id).attr({
                    "href": `http://${argument}`
                })
            }
    
        });
    
        $('.btn').resizable({
            containment: $('#tabs-for-download'),
            grid: [20, 20],
            autoHide: true,
            minWidth: 50,
            minHeight: 30,
        }); 
    }
    
    function PDFFunction(top=null, left=null, link=null, height=null, width=null){
        const Pdf = new PDF(
            top,
            left, link, height, width   
        );
    
        Pdf.renderDiagram();

        $('.pdf').resizable({
            containment: $('#tabs-for-download'),
            grid: [20, 20],
            autoHide: true,
          
        });
        

          // ==for pdf upload==
        $('.fa-upload').click(function(e) {
            trigger = parseInt(e.target.id) + 1;
            $('#' + trigger).trigger('click');
        });
    
        $('.fa-trash').click(function(e) {
            $('#' + e.currentTarget.id).parent().parent().remove();
        });

        $('.pdf').on('dragover', function(e) {
            e.stopPropagation();
            e.preventDefault();
            //   $(this).css('border',"2px solid #39F")
        })

        $('.pdf').on('drop', function(e) {
            e.stopPropagation();
            e.preventDefault();
            const files = e.originalEvent.dataTransfer.files;
            var file = files[0];
            upload(file);
        });

        function upload(file) {
            const data = new FormData();
            data.append("file-0", file);
            data.append('chapterID', chapterID);
            data.append('courseID', courseID);
            data.append('type', 'pic');
            $.ajax({
                url: save_file_url, //image url defined in chapterbuilder.html which points to WebApp/static/chapterPageBuilder/images
                data: data,
                contentType: false,
                processData: false,
                method: 'POST',
                type: 'POST',
                beforeSend: function() {
                    div.append(`<div class="loader" id="loadingDiv"></div>`)
                    $('#loadingDiv').show();
                }, 
                error: function(errorThrown){
                    alert("Failed to upload PDF")
                    div.find('#loadingDiv').remove();
                },
                success: function(data) {
                    div.empty();
                    div.append(`
                        <object data="/media/chapterBuilder/${courseID}/${chapterID}/${input.files[0].name}" type="application/pdf" width="100%" height="100%">
                            alt : <a href="/media/chapterBuilder/${courseID}/${chapterID}/${input.files[0].name}">test.pdf</a>
                        </object>
                    `);

                },
                error: function(data, status, errorThrown) {
                    alert(data.responseJSON.message);
                }
            });
            let div = $('#pdf-actions1').parent();
            console.log(div);
            $('#pdf-actions1').css({
                'display': 'none'
            });

            $(div).hover(function() {
                $(this).css(
                    {
                        "border": "1px solid red",

                });
               

              
            }, function() {
                $(this).css("border", '0')
            });


            $(div).resizable({
                containment: $('#tabs-for-download'),
                grid: [20, 20],
                autoHide: true,
                minWidth:500,
                minHeight:500


            
        })


        $('.pdf').css({
            'resize':' both'
        })

           

        }

        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    let div = $(input).parent().parent().parent();
                    var data = new FormData();
                    // var count = 0
                    // console.log(input.files);
                    $.each(input.files, function(i, file) {
                        // console.log(Math.round((file.size / 1024))) // get image size
                        data.append('file-' + i, file);
                    });
                    // data.append('count', count);
                    data.append('type', 'pdf');
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
                        beforeSend: function() {
                            div.append(`<div class="loader" id="loadingDiv"></div>`)
                            $('#loadingDiv').show();
                        }, 
                        error: function(errorThrown){
                            alert("Failed to upload PDF")
                            div.find('#loadingDiv').remove();
                        },                     
                        success: function(data) {
                            // console.log(data);
                            div.find('#loadingDiv').remove();
                            div.empty();
                            div.append(`
                                <object data="/media/chapterBuilder/${courseID}/${chapterID}/${input.files[0].name}" type="application/pdf" width="100%" height="100%">
                                    alt : <a href="/media/chapterBuilder/${courseID}/${chapterID}/${input.files[0].name}">test.pdf</a>
                                </object>
                            `);
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

                    $(div).resizable({
                        containment: $('#tabs-for-download'),
                        grid: [20, 20],
                        autoHide: true,
                        minWidth: 150,
                        minHeight: 150
                    });

                    $('.pdf').css({
                        'resize':'both'
                    })
                }
                reader.readAsDataURL(input.files[0]);
            }
        }
        $(".pdfInp").change(function(e) {
            readURL(this);
        });
    }

    function VideoFunction(top=null, left=null, link=null, height=null, width=null){
        const Videos = new video(top, left, link, height, width);
        Videos.renderDiagram();
        $('.fa-trash').click(function(e) {
            $('#' + e.currentTarget.id).parent().parent().remove();
            //  alert('btn clickd')
        });
        $('.fa-upload').click(function(e) {
            trigger = parseInt(e.target.id) + 1;
            $('#' + trigger).trigger('click');
        });

        $('.video-div').resizable({
            containment: $('.editor-canvas'),
            grid: [20, 20],
            autoHide: true,
            minWidth: 150,
            minHeight: 150
        });
    
        $('.video-div').on('dragover', function(e) {
            e.stopPropagation();
            e.preventDefault();
        })
    
        $('.video-div').resizable({
            containment: $('#tabs-for-download'),
            grid: [20, 20],
            autoHide: true,
            minWidth: 150,
            minHeight: 150
        });

        $('.video-div').on('drop', function(e) {
            e.stopPropagation();
            e.preventDefault();
            
    
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
            data.append('chapterID', chapterID);
            data.append('courseID', courseID);
            data.append('type', 'video');
            $.ajax({
                xhr: function() {
                    var xhr = new window.XMLHttpRequest();
    
                    xhr.upload.addEventListener("progress", function(evt) {
                        $('#progress-bar').css("display", "block");
    
                        if (evt.lengthComputable) {
                            var percentComplete = evt.loaded / evt.total;
                            percentComplete = parseInt(percentComplete * 100);
                            console.log(percentComplete);
                            // $('#progress-bar-fill').css('width', percentComplete + '%');
                                $("#progress-bar").attr('aria-valuenow',percentComplete).css('width',percentComplete+'%').text(percentComplete+'%');

                            if (percentComplete === 100) {
                                // $('#progress-bar').css("display", "none");
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
    
                                $('.video-div').resizable({
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
                url: save_video_url,
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
                    console.log(input.files)
                    $.each(input.files, function(i, file) {
                        data.append('file-' + i, file);
                    });
                    data.append('chapterID', chapterID);
                    data.append('courseID', courseID);
                    data.append('type', 'video');
                    $.ajax({
                        url: save_video_url,
                        data: data,
                        contentType: false,
                        processData: false,
                        method: 'POST',
                        type: 'POST',
                        beforeSend: function() {
                            div.append(`<div class="loader" id="loadingDiv"></div>
                            <p id = "percentcomplete"></p>
                            `)
                            $('#loadingDiv').show();
                        }, 
                        error: function(errorThrown){
                            alert("Failed to upload Video")
                            div.find('#loadingDiv').remove();
                            div.find('#percentcomplete').remove();
                        },                     
                        success: function(data) {
                            div.find('#loadingDiv').remove();
                            div.find('#percentcomplete').remove();
                            div.empty();
                            // div.append(`
                            // <video width="100%" height="90%" controls id=${data.link}>
                            // <source src="${load_file_url}/${input.files[0].name}" type="video/mp4">
                            //     Your browser does not support the video tag.
                            // </video>`);

                            div.append(`
                                ${data.html}
                            `);
                        },
                        xhr: function() {
                            var xhr = new window.XMLHttpRequest();
    
                            xhr.upload.addEventListener("progress", function(evt) {
                                $('#progress-bar').css("display", "block");
    
                                if (evt.lengthComputable) {
                                    var percentComplete = evt.loaded / evt.total;
                                    percentComplete = parseInt(percentComplete * 100);
                                    console.log(percentComplete);
                                    $('#percentcomplete').text(percentComplete+'%')
                                    $('#progress-bar-fill').css('width', percentComplete + '%');
    
                                    if (percentComplete === 100) {
                                        $('#progress-bar').css("display", "none");
                                        let div = $('#video-drag').parent().parent();
                                        $('#video-drag').css({
                                            'display': 'none'
                                        });
    
                                //         div.append(`
                                //         <video width="400" height="200" controls>
                                //         <source src="${load_file_url}/${input.files[0].name}" type="video/mp4">
                                //          Your browser does not support the video tag.
                                //       </video>
                                //   `);
    
                                        $(div).hover(function() {
                                            $(this).css("border", "1px solid red");
                                        }, function() {
                                            $(this).css("border", '0')
                                        })
    
                                        $('.video-div').resizable({
                                            containment: $('#tabs-for-download'),
                                            grid: [20, 20],
                                            autoHide: true,
                                            minWidth: 150,
                                            minHeight: 150
                                        });
                                        // console.log(file.name);
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
    }

    function dropfunction(event, ui) {
        if (ui.helper.hasClass('textbox')) {
            TextboxFunction(ui.helper.position().top - toolbarheight,
            ui.helper.position().left - sidebarWidth, "10%", "25%");
        } else if (ui.helper.hasClass('picture')) {
            PictureFunction(ui.helper.position().top - toolbarheight,
            ui.helper.position().left - sidebarWidth);
            //object of video component
        } else if (ui.helper.hasClass('video')) {
            VideoFunction(ui.helper.position().top - toolbarheight,
                ui.helper.position().left - sidebarWidth);
        } else if (ui.helper.hasClass('buttons')) {
            ButtonFuction(ui.helper.position().top - toolbarheight,
                ui.helper.position().left - sidebarWidth);
        } else if (ui.helper.hasClass('grid-1')) {
            PictureFunction(
                top = 0,
                left = 150,
                "",
                width = "30%", height="45%");
            
            
            // ===============for textbox inside grid-1============
            TextboxFunction(
                top="50%",
                left=150,
                height="45%", width='50% '
            );
        } else if (ui.helper.hasClass('grid')) {
            VideoFunction(
                top = 0,
                left = 0,
                "",
                height="50%",width = "100%");
            
            
            // ===============for textbox inside grid-1============
            TextboxFunction(
                top="52%",
                left=0,
                height="45%", width="100%"
            );
        } else if (ui.helper.hasClass('title-slide')) {
            PictureFunction(
                top = 0,
                left = "0%",
                "",
                width = "100%", height="60%");
            PictureFunction(
                top = 0,
                left = "50%",
                "",
                width = "100%", height="60%");
            TextboxFunction(
                top="62%",
                left=0,
                height="35%", width="100%",
                message="Your Content Here"
            );
        } else if (ui.helper.hasClass('title-content-details')) {
            TextboxFunction(
                top="0%",
                left=0,
                height="10%", width="50%",
                message="Your Title Here"
            );
            TextboxFunction(
                top="13%",
                left=0,
                height="84%", width="50%",
                message="Your Content Here"
            );
        } else if (ui.helper.hasClass('pdf-text')) {
            PDFFunction(
                top = "0%",
                left = 0,
                link="",
                height = "60%", width="100%");
            
            
            // ===============for textbox inside grid-1============
            TextboxFunction(
                top="62%",
                left=0,
                height="35%", width="100%"
            );
        
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
        
        }else if(ui.helper.hasClass('Pdf')){
            PDFFunction(ui.helper.position().top - toolbarheight,
            ui.helper.position().left - sidebarWidth);
        }
        $('.fa-trash').click(function(e) {
            $('#' + e.currentTarget.id).parent().parent().remove();
        });
    }

    $(".editor-canvas").droppable({
        drop: function(event, ui){
            dropfunction(event,ui)
        }
    });

    $("#add-page-btn").on("click", function() {
        newpagefunction();
    });
    
    function newpagefunction(){
        var num_tabs = $(".tabs-to-click ul li").length + 1;
        
        $(".tabs-to-click ul").append(`
            <!--<div>
                <button class="clone-page-btn" value="${num_tabs}"><i class="fa fa-clone fa-2x" aria-hidden="true"></i></button>
            </div>-->
            <li class="tabs-link pagenumber" onclick="openTab(event,'tab${num_tabs}')" >
               
            </li><br/>

            <p>${num_tabs}</p>
            
            
            `

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
    }

    function display(){
        $('#chaptertitle').text(chaptertitle);
        $('#tabs-for-download').empty();    // empty current canvas 
        $('.tabs-to-click > ul > li:first').remove()
        if(data.pages == undefined){
            $('#add-page-btn').click()
        }
        $.each(data.pages, function(key, value){
            newpagefunction()   // add pages corresponding to the number of pages in json
            $('.tabs-to-click > ul > li')[key-1].click()
            $.each(value, function(count){
                // -------------------------------
                $.each(value[count], function(div,div_value){
                    if(div == 'textdiv'){
                        $.each(div_value, function(css, css_value){
                            css_string = JSON.stringify(css_value)

                            TextboxFunction(css_value.tops,
                            css_value.left,css_value.height,css_value.width,css_value.content);
                        });
                    }
                    if(div == 'pic'){
                        $.each(div_value, function(css, css_value){
                            css_string = JSON.stringify(css_value)
                            PictureFunction(css_value.tops,
                                css_value.left,css_value['background-image'],css_value.width,css_value.height);
                        });
                    }

                    if(div == 'btn-div'){
                        $.each(div_value, function(css, css_value){
                            css_string = JSON.stringify(css_value)
                            
                            ButtonFuction(css_value.tops,
                                css_value.left, 
                                css_value.link,
                                css_value.height, css_value.width);
                        });
                    }

                    if(div == 'pdf'){
                        $.each(div_value, function(css, css_value){
                            css_string = JSON.stringify(css_value)
                            PDFFunction(
                                css_value.tops,
                                css_value.left,
                                css_value['link'],
                                css_value.height,css_value.width);
                        });
                    }

                    if(div == 'video'){
                        $.each(div_value, function(css, css_value){
                            css_string = JSON.stringify(css_value)
                            VideoFunction(
                                css_value.tops,
                                css_value.left,
                                css_value['link'],
                                css_value.height,css_value.width);
                        });
                    }
                });
            });
        });
        $('.tabs-to-click > ul > li')[0].click()
    }
    
    display();
});

//clone Page function
// $('.tabs-to-click').on('click', '.clone-page-btn', function(){
//     $(".tabs-to-click ul").append(`
//         <div>
//             <button class="clone-page-btn" value="${parseInt(this.value)+1}"><i class="fa fa-clone fa-2x" aria-hidden="true"></i></button>
//         </div>
//         <li class="tabs-link pagenumber" onclick="openTab(event,'tab${parseInt(this.value)+1}')" >
            
//         </li>
//     `);
    
//     $('#tab'+this.value).clone().after($('#tab'+this.value));

//     $(".editor-canvas").droppable({
//         drop: function(event, ui){
//             dropfunction(event,ui);
//         }
//     });

// });
// =====================================================================================
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