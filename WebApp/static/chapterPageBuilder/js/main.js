var firstload = true;
var tempVarStorage;
var tobedeletedfiles = {
    'pic': [],
    'video': [],
    'pdf': [],
    '_3d': [],
}

function getEmbedVideo(url) {
    var ytRegExp = /\/\/(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([\w|-]{11})(?:(?:[\?&]t=)(\S+))?$/;
    var ytRegExpForStart = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/;
    var ytMatch = url.match(ytRegExp);
    var igRegExp = /(?:www\.|\/\/)instagram\.com\/p\/(.[a-zA-Z0-9_-]*)/;
    var igMatch = url.match(igRegExp);
    var vRegExp = /\/\/vine\.co\/v\/([a-zA-Z0-9]+)/;
    var vMatch = url.match(vRegExp);
    var vimRegExp = /\/\/(player\.)?vimeo\.com\/([a-z]*\/)*(\d+)[?]?.*/;
    var vimMatch = url.match(vimRegExp);
    var dmRegExp = /.+dailymotion.com\/(video|hub)\/([^_]+)[^#]*(#video=([^_&]+))?/;
    var dmMatch = url.match(dmRegExp);
    var youkuRegExp = /\/\/v\.youku\.com\/v_show\/id_(\w+)=*\.html/;
    var youkuMatch = url.match(youkuRegExp);
    var qqRegExp = /\/\/v\.qq\.com.*?vid=(.+)/;
    var qqMatch = url.match(qqRegExp);
    var qqRegExp2 = /\/\/v\.qq\.com\/x?\/?(page|cover).*?\/([^\/]+)\.html\??.*/;
    var qqMatch2 = url.match(qqRegExp2);
    var mp4RegExp = /^.+.(mp4|m4v)$/;
    var mp4Match = url.match(mp4RegExp);
    var oggRegExp = /^.+.(ogg|ogv)$/;
    var oggMatch = url.match(oggRegExp);
    var webmRegExp = /^.+.(webm)$/;
    var webmMatch = url.match(webmRegExp);
    var fbRegExp = /(?:www\.|\/\/)facebook\.com\/([^\/]+)\/videos\/([0-9]+)/;
    var fbMatch = url.match(fbRegExp);
    var $video_element;
    if (ytMatch && ytMatch[1].length === 11) {
        var youtubeId = ytMatch[1];
        var start = 0;
        if (typeof ytMatch[2] !== 'undefined') {
            var ytMatchForStart = ytMatch[2].match(ytRegExpForStart);
            if (ytMatchForStart) {
                for (var n = [3600, 60, 1], i = 0, r = n.length; i < r; i++) {
                    start += (typeof ytMatchForStart[i + 1] !== 'undefined' ? n[i] * parseInt(ytMatchForStart[i + 1], 10) : 0);
                }
            }
        }
        $video_element = $('<iframe>')
            .attr('frameborder', 0)
            .attr('src', '//www.youtube.com/embed/' + youtubeId + (start > 0 ? '?start=' + start : ''))
            .attr('width', '100%').attr('height', '100%');
    } else if (vimMatch && vimMatch[3].length) {
        $video_element = $('<iframe webkitallowfullscreen mozallowfullscreen allowfullscreen>')
            .attr('frameborder', 0)
            .attr('src', '//player.vimeo.com/video/' + vimMatch[3])
            .attr('width', '100%').attr('height', '100%');
    } else if (dmMatch && dmMatch[2].length) {
        $video_element = $('<iframe>')
            .attr('frameborder', 0)
            .attr('src', '//www.dailymotion.com/embed/video/' + dmMatch[2])
            .attr('width', '100%').attr('height', '100%');
    } else if (youkuMatch && youkuMatch[1].length) {
        $video_element = $('<iframe webkitallowfullscreen mozallowfullscreen allowfullscreen>')
            .attr('frameborder', 0)
            .attr('height', '100%')
            .attr('width', '100%')
            .attr('src', '//player.youku.com/embed/' + youkuMatch[1]);
    } else if (mp4Match || oggMatch || webmMatch) {
        $video_element = $('<video controls>')
            .attr('src', url)
            .attr('width', '100%').attr('height', '100%');
    } else {
        // this is not a known video link. Now what, Cat? Now what?
        return false;
    }
    return $video_element[0];
}

function revertpositionConvert(element, multiplier) {
    return parseFloat(element) * parseFloat(multiplier) / 100
}

function positionConvert(element, divider) {
    return parseFloat(element) * 100 / parseFloat(divider)
}

function convertFontToREM(font) {
    return parseFloat(font) / 14;
}

function convertFontToPX(font) {
    return parseFloat(font) * 14;
}

// Initializing Elements

// ==================For TextBoxx================================
// $('#tabs-for-download').droppable({
//     tolerance: 'fit',
//     drop: function (event, ui) {
//         $(this).removeClass("border").removeClass("over");
//     },

//     over: function (event, elem) {
//         $(this).addClass("over");
//     },
//     out: function (event, elem) {
//         $(this).removeClass("over");
//     },
// });

class Textbox {
    constructor(top = 0, left = 0, height = null, width = null, message = "") {
        let id = (new Date).getTime();
        let position = {
            top, left, height, width
        };
        let html = `<div class='textdiv' >
                 
                 <div id="editor${id}" class="messageText"></div>
                 <div id="text-actions" class = "text-actions">
                     <i class="fas fa-trash" id=${id}></i>
                     <i class="fas fa-arrows-alt" id="draghere" ></i>
                 </div> 
              </div>
              `;
        this.renderDiagram = function () {
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
                cursorAt: {bottom: 0},

                handle: '.text-actions',
                stop: function () {
                    var l = positionConvert($(this).position().left, parseFloat($('#tabs-for-download').width())) + "%";
                    var t = positionConvert($(this).position().top, parseFloat($('#tabs-for-download').height())) + "%";
                    var h = positionConvert($(this).height(), parseFloat($('#tabs-for-download').height())) + "%";
                    var w = positionConvert($(this).width(), parseFloat($('#tabs-for-download').width())) + "%";
                    $(this).css("left", l);
                    $(this).css("top", t);
                    $(this).css("height", h);
                    $(this).css("width", w);
                }
            });


            var a = document.getElementsByClassName("current")[0];

            $('#' + a.id).append(dom);
            let placeholder = ''
            if(!message){
                placeholder = 'Type Something here...'
            }
            $('#editor' + id).summernote({
                followingToolbar: false,
                disableResizeEditor: true,
                placeholder: placeholder,
                fontSizes: ['8', '9', '10', '11', '12', '14', '16', '18', '20', '24', '36', '48', '56', '64', '72'],
                toolbar: [
                    ['style', ['style']],
                    ['font', ['bold', 'underline', 'clear', 'strikethrough', 'superscript', 'subscript']],
                    ['fontsize', ['fontsize']],
                    ['fontname', ['fontname']],
                    ['color', ['color']],
                    ['para', ['ul', 'ol', 'paragraph']],
                    ['table', ['table']],
                    ['insert', ['link', 'hr']],
                    ['height', ['height']],
                    ['view', ['help']],
                ],
                callbacks: {
                    onPaste: function (e) {
                        var bufferText = ((e.originalEvent || e).clipboardData || window.clipboardData).getData('Text');
                        e.preventDefault();
                        document.execCommand('insertText', false, bufferText);
                    }
                }
            });
            $('.note-editable').css('font-size', '15px');
            $('.note-toolbar').css('display', 'none')


            $('#editor' + id).parent().find('.note-statusbar').remove();
            $('#editor' + id).parent().find('.note-editable').html(message);
            // $('#editor' + id).parent().find('.note-editable').each(function(){
            //     if($(this).find('span').css('font-size')){
            //         let font = convertFontToPX($(this).find('span')[0].style['font-size'])
            //         $(this).find('span').css('font-size', font + 'px')
            //     }
            // })
            // $(".editor-canvas").append(dom);
            // Making element Resizable
        };
    }
}

// ===========================FOR PICTURE=====================================

class picture {
    constructor(top, left, pic = null, width = null, height = null) {

        let id = (new Date).getTime();
        let position = {top, left, width, height};
        let message = "";
        if (pic == null) {
            message = `
                <div class = "file-upload-icon">
                    <img src = "/static/chapterPageBuilder/images/uploadIcon.png" height = "100%" width = "100%"></img>
                </div>
                Drag and drop images here...
                `
        }
        let img = '';
        if (pic != null) {
            img = `<img src = '${pic}' width= "100%" height="100%" style = "object-fit: cover;"></img>`
        }
        let html =
            `<div class='pic'>
            <div id="pic-actions">
                <i class="fas fa-trash" id=${id}></i>
                <i class="fas fa-upload" id=${id}></i>
                <i class="fas fa-link imagelink" id=${id}></i>
            </div>
            ${img}
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
                cursorAt: {bottom: 0},
                stop: function () {
                    var l = positionConvert($(this).position().left, parseFloat($('#tabs-for-download').width())) + "%";
                    var t = positionConvert($(this).position().top, parseFloat($('#tabs-for-download').height())) + "%";
                    var h = positionConvert($(this).height(), parseFloat($('#tabs-for-download').height())) + "%";
                    var w = positionConvert($(this).width(), parseFloat($('#tabs-for-download').width())) + "%";
                    $(this).css("left", l);
                    $(this).css("top", t);
                    $(this).css("height", h);
                    $(this).css("width", w);
                }
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
        };
    }
}

// ====================================For Video==============================

class video {
    constructor(top, left, link = null, height = null, width = null) {
        let id = (new Date).getTime();
        var now = Math.floor(Math.random() * 900000) + 100000;
        let position = {top, left, height, width};
        let videoobj;
        let message = "";
        // if(link!=null){
        //     videoobj = `<div id='${now}'><div>
        //  <script>
        //     var options = {
        //         url: '${link}',
        //         width: "${width}",
        //         height: "${height}"
        //     };

        //     var videoPlayer = new Vimeo.Player('${now}', options);
        //   </script>`
        //  ================================   end for vimeo    ===========================================
        if (link != null) {

            // videoobj = `
            //         <video width="100%" height="75%" controls>
            //             <source src="https://www.youtube.com/embed/${myYoutubeId}"  type="video/mp4">
            //         </video>
            // `
            if (link.includes('www') && link.includes('.com')) {
                videoobj = `<iframe width="100%" height="94%" src="${link}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>`
            } else {
                videoobj = `
                    <video width="100%" height="94%" controls>
                        <source src="${link}"  type="video/mp4">
                    </video>
            `
            }
        } else {
            message = `
            Add video here...<br> <a href ='https://converterpoint.com/' target = '_blank'>Need help converting?</a>`;
            videoobj = `<div class="progress video-text-div">
                <div id="progress-bar" class="progress-bar progress-bar-striped" role="progressbar" style="width: 0%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
            </div>`;
        }
        let html =
            `<div class='video-div'>
                <div id="video-actions">
                    <i class="fas fa-trash" id=${id}></i>
                    <i class="fas fa-upload" id=${id}></i>
                    <i class="fas fa-link videolink" id=${id}></i>
                </div>
                <div>
                    <p id="video-drag">${message}</p>
                    
                    <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                    <input type='file' name="userImage" accept="video/*" style="display:none" id=${id + 1} class="video-form" />
                    </form>
                    ${videoobj}
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
                "height": position.height,
                "width": position.width
            }).draggable({
                //Constraint   the draggable movement only within the canvas of the editor
                containment: "#tabs-for-download",
                scroll: false,
                cursor: "move",
                snap: ".gridlines",
                snapMode: 'inner',
                cursorAt: {bottom: 0},
                stop: function () {
                    var l = positionConvert($(this).position().left, parseFloat($('#tabs-for-download').width())) + "%";
                    var t = positionConvert($(this).position().top, parseFloat($('#tabs-for-download').height())) + "%";
                    var h = positionConvert($(this).height(), parseFloat($('#tabs-for-download').height())) + "%";
                    var w = positionConvert($(this).width(), parseFloat($('#tabs-for-download').width())) + "%";
                    $(this).css("left", l);
                    $(this).css("top", t);
                    $(this).css("height", h);
                    $(this).css("width", w);
                }
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom)
        };
    }
}

// =====================For Button==============================

class Button {
    constructor(top, left, link = null, height = null, width = null, name = 'Button', font_size) {
        let id = (new Date).getTime();
        let position = {top, left, height, width};
        let button_link = ""
        if (link != null) {
            button_link = 'href = ' + link
        }
        let html = `
                    <div class="btn-div" data-width = "${width}">
                        <div class="options">
                            <i class="fas fa-trash" id=${id}></i>
                            <i class="fas fa-link"   id=${id} ></i>
                            <i class="fas fa-arrows-alt" id="draghanle"></i>
                        
                        </div> 

                        <div class="button-name-builder ">
                        <a ${button_link} id=${id + 1}  target="_blank">
                        
                        <button class="custom-btn-only"style="width:100%; height:100%">
                            <div class="row text-center" width=100%>
                            <span class="resizable-text-only " style = "width:100%; font-size: ${font_size}">${name} </span>
                            </div>
                            <div class="row text-center">
                            </div>    
                        </button>

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
                cursor: "move",
                handle: '.options',
                stop: function () {
                    var l = positionConvert($(this).position().left, parseFloat($('#tabs-for-download').width())) + "%";
                    var t = positionConvert($(this).position().top, parseFloat($('#tabs-for-download').height())) + "%";
                    var h = positionConvert($(this).height(), parseFloat($('#tabs-for-download').height())) + "%";
                    var w = positionConvert($(this).width(), parseFloat($('#tabs-for-download').width())) + "%";
                    $(this).css("left", l);
                    $(this).css("top", t);
                    $(this).css("height", h);
                    $(this).css("width", w);
                }
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
            // canvas.append(dom);
            // Making element Resizable

        };
    }
}

class Quiz {
    constructor(top, left, link = null, height = null, width = null, name = 'Play Quiz', quiz_span_name = "", font_size) {
        let id = (new Date).getTime();
        let position = {top, left, height, width};
        let quiz_link = ""
        if (link != null) {
            quiz_link = 'href = ' + link
        }
        let html = `
                    <div class="quiz-div" data-width = "${width}">
                        <div class="options">
                            <i class="fas fa-trash" id=${id}></i>
                            <i class="fas fa-link"   id=${id} ></i>
                            <i class="fas fa-arrows-alt" id="draghanle"></i>
                        
                        </div> 
                        <div class="button-name-builder ">
                        <a ${quiz_link} id = ${id + 1} target= "_blank">
                            <button class="custom-btn-only"style="width:100%; height:100%">
                            <div class="row text-center" width=100%>
                            <span class="resizable-text-only " style = "width:100%; font-size: ${font_size}">${name} </span>
                            </div>
                            <div class="row text-center">
                            <span class = "quiz-name " style = "bottom: 0px; width:100% ;">
                            ${quiz_span_name}</span>

                            </div>
                            
                            
                            </button>
                        </a>
                       
                        
                        </div>     
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
                cursor: "move",
                handle: '.options',
                stop: function () {
                    var l = positionConvert($(this).position().left, parseFloat($('#tabs-for-download').width())) + "%";
                    var t = positionConvert($(this).position().top, parseFloat($('#tabs-for-download').height())) + "%";
                    var h = positionConvert($(this).height(), parseFloat($('#tabs-for-download').height())) + "%";
                    var w = positionConvert($(this).width(), parseFloat($('#tabs-for-download').width())) + "%";
                    $(this).css("left", l);
                    $(this).css("top", t);
                    $(this).css("height", h);
                    $(this).css("width", w);
                }
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
            // canvas.append(dom);
            // Making element Resizable

        };
    }
}

class Survey {
    constructor(top, left, link = null, height = null, width = null, name = 'Take Survey', survey_span_name = "", font_size) {
        let id = (new Date).getTime();
        let position = {top, left, height, width};
        let survey_link = ""
        if (link != null) {
            survey_link = 'href = ' + link
        }
        let html = `
                    <div class="survey-div" data-width = "${width}">
                        <div class="options">
                            <i class="fas fa-trash" id=${id}></i>
                            <i class="fas fa-link"   id=${id} ></i>
                            <i class="fas fa-arrows-alt" id="draghanle"></i>
                        
                        </div> 
                        <div class="button-name-builder">
                            <a ${survey_link} id=${id + 1}  target="_blank" >
                            
                                <button class="custom-btn-only"style="width:100%; height:100%">
                                <div class="row text-center" width=100%>
                                    <span class="resizable-text-only" style = "width:100%; font-size: ${font_size}">${name} </span>
                                </div>
                                <div class="row text-center">
                                    <span class = "survey-name " style = "bottom: 0px; width:100% ;">
                                    ${survey_span_name}</span>
                                    </div>
                                </button>
                                
                            </a>
                        </div>    
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
                cursor: "move",
                handle: '.options',
                stop: function () {
                    var l = positionConvert($(this).position().left, parseFloat($('#tabs-for-download').width())) + "%";
                    var t = positionConvert($(this).position().top, parseFloat($('#tabs-for-download').height())) + "%";
                    var h = positionConvert($(this).height(), parseFloat($('#tabs-for-download').height())) + "%";
                    var w = positionConvert($(this).width(), parseFloat($('#tabs-for-download').width())) + "%";
                    $(this).css("left", l);
                    $(this).css("top", t);
                    $(this).css("height", h);
                    $(this).css("width", w);
                }
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
    constructor(top, left, link = null, height = null, width = null) {
        let id = (new Date).getTime();
        var pdfobj;
        var message;
        let position = {top, left, height, width};
        if (link != null) {
            pdfobj = `
            <object data="${link}" type="application/pdf" width="100%" height="100%">
                alt : <a href="${link}"></a>
            </object>
        `
            message = ''
        } else {
            message = `
            <div class = "file-upload-icon">
                <img src = "/static/chapterPageBuilder/images/uploadIcon.png" height = "100%" width = "100%"></img>
            </div>
            drag and drop files here...`;
            pdfobj = "";
        }
        let html = `
        <div class='pdfdiv'>
            <div id="pdfdiv-actions1">
                <i class="fas fa-trash" id=${id}></i>
                <i class="fas fa-upload" id=${id}></i>
            </div>
            <div>
                <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                <input type='file' accept="application/pdf"  style="display:none" id=${id + 1}  multiple="multiple" class="pdfInp" />
                </form>
                <p id="pdfdiv-drag" placeholder="drag and drop files here...">${message}</p>
            </div>
            ${pdfobj}
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
                cursor: "move",
                snap: ".gridlines",
                snapMode: 'inner',
                cursorAt: {bottom: 0},
                stop: function () {
                    var l = positionConvert($(this).position().left, parseFloat($('#tabs-for-download').width())) + "%";
                    var t = positionConvert($(this).position().top, parseFloat($('#tabs-for-download').height())) + "%";
                    var h = positionConvert($(this).height(), parseFloat($('#tabs-for-download').height())) + "%";
                    var w = positionConvert($(this).width(), parseFloat($('#tabs-for-download').width())) + "%";
                    $(this).css("left", l);
                    $(this).css("top", t);
                    $(this).css("height", h);
                    $(this).css("width", w);
                }
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
            // Making element Resizable

        };
    }
}

// =====================For 3DObjects==============================

class _3Dobject {
    constructor(top, left, file = null, height = null, width = null) {
        let id = (new Date).getTime();
        let position = {top, left, width, height};
        let message = "";
        var _3dobj;
        if (file == null) {
            message = `
            <div class = "file-upload-icon">
                <img src = "/static/chapterPageBuilder/images/uploadIcon.png" height = "100%" width = "100%"></img>
            </div>
            Add 3D objects here...`
        }
        if (file != null) {
            _3dobj = `
                <model-viewer
                src="${file}"
                alt="Here is a 3D Object."
                auto-rotate
                camera-controls  
                style="height: 100%;width:100%;"></model-viewer>

            `
        } else {
            _3dobj = "";
        }
        let html =
            `<div class='_3dobj-div'>
                <div id="_3dobj-actions">
                    <i class="fas fa-trash" id=${id}></i>
                    <i class="fas fa-upload" id=${id}></i>
                </div>
                <div>
                    <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                    <input type='file' name="userImage" style="display:none" id=${id + 1} class="_3dobjinp" />
                </form>
                <p id="_3dobj-drag">${message}</p>
            </div>
            ${_3dobj}
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
                "height": position.height,
                "width": position.width
            }).draggable({
                //Constrain the draggable movement only within the canvas of the editor
                containment: "#tabs-for-download",
                scroll: false,
                cursor: "move",
                snap: ".gridlines",
                snapMode: 'inner',
                cursorAt: {bottom: 0},
                stop: function () {
                    var l = positionConvert($(this).position().left, parseFloat($('#tabs-for-download').width())) + "%";
                    var t = positionConvert($(this).position().top, parseFloat($('#tabs-for-download').height())) + "%";
                    var h = positionConvert($(this).height(), parseFloat($('#tabs-for-download').height())) + "%";
                    var w = positionConvert($(this).width(), parseFloat($('#tabs-for-download').width())) + "%";
                    $(this).css("left", l);
                    $(this).css("top", t);
                    $(this).css("height", h);
                    $(this).css("width", w);
                }
            });

            var a = document.getElementsByClassName("current")[0];
            $('#' + a.id).append(dom);
        };
    }
}

// ====================== End of initializing elements ========================

// Element Functions
function TextboxFunction(top = null, left = null, height = "20%", width = "30%", message = "") {
    const textBox = new Textbox(top, left, height, width, message);

    textBox.renderDiagram();
    $('.textdiv').hover(function (e) {
        $(e.currentTarget).find('.text-actions').css({
            'display': 'block'
        });
        $(this).css({
            'border': '1px solid grey'
        })

    }, function () {
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

    $('.fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });
    $('.textdiv').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 75,
        minHeight: 25,
        autoHide: true,
        stop: function (e, ui) {
            //   var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        }
    });
    $('.note-editing-area').on('focusin', function (e) {
        $(e.currentTarget).parent().find('.note-popover .popover-content,.panel-heading.note-toolbar').css('display', 'block')
    });

    var resultsSelected = false;
    $(".note-toolbar > .note-btn-group").hover(
        function () {
            resultsSelected = true;
        },
        function () {
            resultsSelected = false;
            // if(!$('.note-editing-area').has(':focus')){
            //   $('.note-popover .popover-content,.panel-heading.note-toolbar').css('display','none')
            // }
        }
    );
    $('.note-editing-area').on('focusout', function (e) {
        if (!resultsSelected) {
            $('.panel-heading.note-toolbar').css('display', 'none')
        }
    });
}

function PictureFunction(top = null, left = null, pic = null, width = null, height = null) {
    const Pic = new picture(
        top,
        left,
        pic,
        width, height);
    Pic.renderDiagram();

    $('.fa-upload').off().unbind().click(function (e) {
        trigger = parseInt(e.target.id) + 1;
        $('#' + trigger).trigger('click');
    });

    $('.fa-trash').click(function (e) {
        if ($('#' + e.currentTarget.id).find('img').length > 0) {
            if ($('#tabs-for-download').find('img[src$="' + $(div).find('img').attr('src') + '"]').length == 1) {
                tobedeletedfiles.pic.push($('#' + e.currentTarget.id).find('img').attr('src'))
            }
        }
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('.imagelink').off().bind("click", function (e) {
        var link_id = parseInt(e.currentTarget.id) + 1
        var div = $('#' + e.currentTarget.id).parent().parent();
        // var prevlink = $(this).parent().parent().find('background-image').replace('url(','').replace(')','').replace(/\"/gi, "");
        var prevlink = $(this).parent().parent().find('img').attr('src')
        if (prevlink == undefined) {
            prevlink = "";
        }
        var link = prompt("Link of image", prevlink);
        if (link == null) {
            return false
        } else if (!link.startsWith('http://') && !link.startsWith('https://')) {
            link = '' + link
        }

        PictureFunction(
            $(div)[0].style.top,
            $(div)[0].style.left,
            link,
            $(div)[0].style.width,
            $(div)[0].style.height,
        );
        div.remove()
    });

    $('.pic').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 150,
        minHeight: 150,
        stop: function (e, ui) {
            // var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        }
    });

    $('.pic').on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        //   $(this).css('border',"2px solid #39F")
    })

    $('.pic').on('drop', function (e) {
        
        e.stopPropagation();
        e.preventDefault();
        const files = e.originalEvent.dataTransfer.files;
        var file = files[0];
        upload(file, $(this));
    });

    function upload(file, element) {
        let div = element;
        const data = new FormData();
        data.append("file-0", file);
        data.append('chapterID', chapterID);
        data.append('courseID', courseID);
        data.append('type', 'pic');
        data.append('csrfmiddlewaretoken', csrf_token);
       
        $.ajax({
            url: save_file_url, //image url defined in chapterbuilder.html which points to WebApp/static/chapterPageBuilder/images
            data: data,
            contentType: false,
            processData: false,
            method: 'POST',
            type: 'POST',
            beforeSend: function () {
                div.append(`<div class="loader" id="loadingDiv"></div>`)
                $('#loadingDiv').show();
            },
            error: function (errorThrown) {
                alert("Failed to upload PDF")
                div.find('#loadingDiv').remove();
            },
            success: function (data) {
                div.find('#loadingDiv').remove();
                div.find('p').text("");

                PictureFunction(
                    $(div)[0].style.top,
                    $(div)[0].style.left,
                    load_file_url + '/' + data.media_name,
                    $(div)[0].style.width,
                    $(div)[0].style.height,
                );
                div.remove()
            },
            error: function (data, status, errorThrown) {
                alert(data.responseJSON.message);
            }
        });

        $('#picture-drag').css({
            'display': 'none'
        })


        $(div).hover(function () {
            $(this).css("border", "1px solid red");
        }, function () {
            $(this).css("border", '0')
        })
    }

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                let div = $(input).parent().parent().parent();
                var data = new FormData();
                $.each(input.files, function (i, file) {
                    data.append('file-' + i, file);
                });
                if ($(div).find('img').length > 0) {
                    if ($('#tabs-for-download').find('img[src$="' + $(div).find('img').attr('src') + '"]').length == 1) {
                        tobedeletedfiles.pic.push($(div).find('img').attr('src'));
                    }
                }
                data.append('csrfmiddlewaretoken', csrf_token);
                data.append('type', 'pic');
                data.append('chapterID', chapterID);
                data.append('courseID', courseID);
                $.ajax({
                    url: save_file_url,
                    data: data,
                    contentType: false,
                    processData: false,
                    enctype: 'multipart/form-data',
                    method: 'POST',
                    type: 'POST',
                    beforeSend: function () {
                        div.append(`<div class="loader" id="loadingDiv"></div>`)
                        $('#loadingDiv').show();
                    },
                    success: function (data) {
                        div.find('#loadingDiv').remove();
                        div.find('p').text("");

                        PictureFunction(
                            $(div)[0].style.top,
                            $(div)[0].style.left,
                            load_file_url + '/' + data.media_name,
                            $(div)[0].style.width,
                            $(div)[0].style.height,
                        );
                        div.remove()
                    },
                    error: function (data, status, errorThrown) {
                        alert(data.responseJSON.message);
                        div.find('#loadingDiv').remove();
                    }
                });

                $('#picture-drag').css({
                    'display': 'none'
                })

                $(div).hover(function () {
                    $(this).css("border", "1px solid red");
                }, function () {
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

    $(".imgInp").off().change(function (e) {
        readURL(this);

    });
}

function ButtonFunction(top = null, left = null, link = null, height = null, width = null, name = 'Button', font_size) {
    const btns = new Button(top, left, link, height, width, name, font_size);

    btns.renderDiagram();

    const div1 = $('i').parent();

    $('.fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('.fa-link').bind("click", function (e) {
        var btn_id = parseInt(e.currentTarget.id) + 1

        $('#btn-form input[type=text]').val('');
        $('#btn-name').val($(this).parent().parent().find('a').text().trim());
        var link = $(this).parent().parent().find('a').attr('href');
        if (link != undefined) {
            link = link.replace('http://', '');
        }
        $('#btn-link').val(link);

        $('#button_id').val(btn_id);
        $('#btn-modal').modal('show');
    });

    $('.btn-div').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 50,
        minHeight: 30,
        stop: function (e, ui) {
            // var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        },
    });

    $('.btn-div').on('resize', function () {
        old_div_width = revertpositionConvert(parseFloat($(this).data('width')), $('#tabs-for-download').width());
        div_width = $(this).width();
        font = parseFloat($(this).find('.resizable-text-only').css('font-size')) * (div_width / old_div_width);
        $(this).find('.resizable-text-only').css(
            'font-size', font + 'px'
        )
        $(this).data('width', positionConvert(div_width, $('#tabs-for-download').width()))
    })

}

function QuizFunction(top = null, left = null, link = null, height = null, width = null, name = 'Select Quiz', quiz_span_name = "", font_size) {
    const quiz = new Quiz(top, left, link, height, width, name, quiz_span_name, font_size);

    quiz.renderDiagram();

    $('.quiz-div button').off().on('click', function (e) {
        e.preventDefault()
        link = $(this).parent().parent().find('a')[0].href
        if (link) {
            quizpk = (link.split('/')[4]).match(/\d+/);
            if (window.location.href.indexOf("/teachers") > -1) {
                link = "/quiz/markingfilter/" + quizpk
                loadPreview(link, 1)
            } else {
                link = "/quiz/detail/" + quizpk
                loadPreview(link, 1)
            }
        } else {
            $(this).closest('.quiz-div').find('.fa-link').click()
        }
    });


    const div1 = $('i').parent();

    $('.fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('.quiz-div .fa-link').bind("click", function (e) {
        tempVarStorage = $(this)
        $.ajax({
            url: `/quiz/api/v1/quiz/?course_code=${courseID}`, //image url defined in chapterbuilder.html which points to WebApp/static/chapterPageBuilder/images
            processData: false,
            method: 'GET',
            success: function (data) {
                $('#myTable').empty()
                for (var i = 0; i < data.length; i++) {
                    $('#myTable').append(`<tr>
                        <td>
                            ${data[i].title}
                        </td>
                        <td>
                            <button type="button" class="selectquiz" value="${data[i].pk}">Select</button>
                        </td>
                    </tr>`);
                }
            },
        });
        var btn_id = parseInt(e.currentTarget.id) + 1
        $('#quiz-form input[type=text]').val('');
        $('#quiz-btn-name').val($(this).parent().parent().find('.resizable-text-only').text().trim());
        var link = $(this).parent().parent().find('a').attr('href');
        if (link != undefined) {
            link = link.replace('http://', '');
        } else {
            $('#quiz-btn-name').parent().hide()
            $('#quiz-name').parent().parent().hide()
        }
        $('#quiz-link').val(link);
        $('#quiz-name').val($(this).parent().parent().find('.quiz-name').text().trim());
        $('#quiz_id').val(btn_id);
        $('#quiz-modal').modal('show');
    });

    $('.quiz-div').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 50,
        minHeight: 30,
        stop: function (e, ui) {
            // var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        },
    });

    $('.quiz-div').on('resize', function () {
        old_div_width = revertpositionConvert(parseFloat($(this).data('width')), $('#tabs-for-download').width());
        div_width = $(this).width();
        font = parseFloat($(this).find('.resizable-text-only').css('font-size')) * (div_width / old_div_width);
        $(this).find('.resizable-text-only').css(
            'font-size', font + 'px'
        )
        $(this).data('width', positionConvert(div_width, $('#tabs-for-download').width()))
    })

}

function SurveyFunction(top = null, left = null, link = null, height = null, width = null, name = 'Select Survey', survey_span_name = "", font_size) {
    const survey = new Survey(top, left, link, height, width, name, survey_span_name, font_size);

    survey.renderDiagram();

    $('.survey-div button').off().on('click', function (e) {
        e.preventDefault()
        link = $(this).parent().parent().find('a')[0].href
        if (link) {
            surveypk = (link.split('/')[6]).match(/\d+/);
            if (window.location.href.indexOf("/teachers") > -1) {
                link = "/teachers/surveyinfodetail/detail/" + surveypk
                loadPreview(link, 1)
            } else {
                link = "/survey/surveyinfo/detail/" + surveypk
                loadPreview(link, 1)
            }
        } else {
            $(this).closest('.survey-div').find('.fa-link').click()
        }
    })

    const div1 = $('i').parent();

    $('.fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('.survey-div .fa-link').on("click", function (e) {
        tempVarStorage = $(this)
        $.ajax({
            url: `/survey/api/v1/surveyinfo/?Course_Code=${courseID}`, //image url defined in chapterbuilder.html which points to WebApp/static/chapterPageBuilder/images
            processData: false,
            method: 'GET',
            success: function (data) {
                $('#mySurveyTable').empty()
                for (var i = 0; i < data.length; i++) {
                    $('#mySurveyTable').append(`<tr>
                        <td>
                            ${data[i].Survey_Title}
                        </td>
                        <td>
                            <button type="button" class="selectsurvey" value="${data[i].pk}">Select</button>
                        </td>
                    </tr>`);
                }
            },
        });
        var btn_id = parseInt(e.currentTarget.id) + 1
        $('#survey-form input[type=text]').val('');
        $('#survey-btn-name').val($(this).parent().parent().find('.resizable-text-only').text().trim());
        var link = $(this).parent().parent().find('a').attr('href');
        if (link != undefined) {
            link = link.replace('http://', '');
        } else {
            $('#survey-btn-name').parent().hide()
            $('#survey-name').parent().parent().hide()
        }
        $('#survey-link').val(link);
        $('#survey-name').val($(this).parent().parent().find('.survey-name').text().trim());
        $('#survey_id').val(btn_id);
        $('#survey-modal').modal('show');
    });

    $('.survey-div').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 50,
        minHeight: 30,
        stop: function (e, ui) {
            // var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        },
    });

    $('.survey-div').on('resize', function () {
        old_div_width = revertpositionConvert(parseFloat($(this).data('width')), $('#tabs-for-download').width());
        div_width = $(this).width();
        font = parseFloat($(this).find('.resizable-text-only').css('font-size')) * (div_width / old_div_width);
        $(this).find('.resizable-text-only').css(
            'font-size', font + 'px'
        )
        $(this).data('width', positionConvert(div_width, $('#tabs-for-download').width()))
    })
}

function PDFFunction(top = null, left = null, link = null, height = null, width = null) {
    const Pdf = new PDF(
        top,
        left, link, height, width
    );

    Pdf.renderDiagram();

    // ==for pdf upload==
    $('.fa-upload').off().click(function (e) {
        trigger = parseInt(e.target.id) + 1;
        $('#' + trigger).trigger('click');
    });

    $('.fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('.pdfdiv').on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        //   $(this).css('border',"2px solid #39F")
    })

    $('.pdfdiv').on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
        const files = e.originalEvent.dataTransfer.files;
        var file = files[0];
        upload(file, $(this));
    });

    function upload(file, element) {
        let pdfdiv = element;
        const data = new FormData();
        data.append("file-0", file);
        data.append('chapterID', chapterID);
        data.append('courseID', courseID);
        data.append('type', 'pdf');
        data.append('csrfmiddlewaretoken', csrf_token);
        $.ajax({
            url: save_file_url, //image url defined in chapterbuilder.html which points to WebApp/static/chapterPageBuilder/images
            data: data,
            contentType: false,
            processData: false,
            method: 'POST',
            type: 'POST',
            beforeSend: function () {
                pdfdiv.append(`<div class="loader" id="loadingDiv"></div>`)
                $('#loadingDiv').show();
            },
            success: function (data) {
                PDFFunction(
                    $(pdfdiv)[0].style.top,
                    $(pdfdiv)[0].style.left,
                    `/media/chapterBuilder/${courseID}/${chapterID}/${data.media_name}`,
                    $(pdfdiv)[0].style.height,
                    $(pdfdiv)[0].style.width,
                );
                pdfdiv.remove();
            },
            error: function (data, status, errorThrown) {
                alert(data.responseJSON.message);
            },
            complete: function () {
                $('#loadingDiv').remove();
            }
        });
        let div = $('#pdf-actions1').parent();
        $('#pdf-actions1').css({
            'display': 'none'
        });

        $(div).hover(function () {
            $(this).css(
                {
                    "border": "1px solid red",

                });


        }, function () {
            $(this).css("border", '0')
        });


        $(div).resizable({
            containment: $('#tabs-for-download'),
            grid: [20, 20],
            autoHide: true,
            minWidth: 500,
            minHeight: 500


        })


        $('.pdf').css({
            'resize': ' both'
        })


    }

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                let div = $(input).parent().parent().parent();
                var data = new FormData();

                $.each(input.files, function (i, file) {
                    // console.log(Math.round((file.size / 1024))) // get image size
                    data.append('file-' + i, file);
                });
                if ($(div).find('object').length > 0) {
                    if ($('#tabs-for-download').find('object[data$="' + $(div).find('object').attr('data') + '"]').length == 1) {
                        tobedeletedfiles.pdf.push($(div).find('object').attr('data'));
                    }
                }
                data.append('csrfmiddlewaretoken', csrf_token);
                data.append('type', 'pdf');
                data.append('chapterID', chapterID);
                data.append('courseID', courseID);
                $.ajax({
                    url: save_file_url,
                    data: data,
                    contentType: false,
                    processData: false,
                    enctype: 'multipart/form-data',
                    method: 'POST',
                    type: 'POST',
                    beforeSend: function () {
                        div.append(`<div class="loader" id="loadingDiv"></div>`)
                        $('#loadingDiv').show();
                    },
                    success: function (data) {
                        PDFFunction(
                            $(div)[0].style.top,
                            $(div)[0].style.left,
                            `/media/chapterBuilder/${courseID}/${chapterID}/${data.media_name}`,
                            $(div)[0].style.height,
                            $(div)[0].style.width,
                        );
                        div.remove();
                    },
                    error: function (data, status, errorThrown) {
                        alert(data.responseJSON.message);
                        alert("Failed to upload PDF");
                    },
                    complete: function () {
                        $('#loadingDiv').remove();
                    }
                });

                $('#picture-drag').css({
                    'display': 'none'
                })

                $(div).hover(function () {
                    $(this).css("border", "1px solid red");
                }, function () {
                    $(this).css("border", '0')
                })

                $('.pdf').resizable({
                    containment: $('#tabs-for-download'),
                    grid: [20, 20],
                    autoHide: true,
                    minWidth: 150,
                    minHeight: 150
                });

                $('.pdf').css({
                    'resize': 'both'
                })
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('.pdfdiv').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        stop: function (e, ui) {
            // var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        },
    });

    $(".pdfInp").off().change(function (e) {
        readURL(this);
    });
}

function VideoFunction(top = null, left = null, link = null, height = null, width = null) {
    const Videos = new video(top, left, link, height, width);
    Videos.renderDiagram();
    $('.fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });
    $('.fa-upload').off().unbind().click(function (e) {
        trigger = parseInt(e.target.id) + 1;
        $('#' + trigger).trigger('click');
    });
    $('.videolink').off().bind("click", function (e) {
        var link_id = parseInt(e.currentTarget.id) + 1
        var div = $(this).parent().parent();
        var prevlink = $(this).parent().parent().find('iframe').attr('src');
        if (prevlink == undefined) {
            prevlink = "http://";
        }
        var link = prompt("Url (Youtube, DailyMotion)", prevlink);
        if (link == null) {
            return false
        } else if (!link.startsWith('http://') && !link.startsWith('https://')) {
            link = 'http://' + link
        }
        video_link = getEmbedVideo(link)
        div.find('p, iframe, video').remove();
        div.append(video_link);
    });

    $('.video-div').on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
    })

    $('.video-div').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 150,
        minHeight: 150,
        stop: function (e, ui) {
            // var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        },
    });

    // $('.video-div').on('drop', function (e) {
    //     e.stopPropagation();
    //     e.preventDefault();


    //     $(this).css({
    //         'padding': '5px'
    //     })

    //     const files = e.originalEvent.dataTransfer.files;
    //     var file = files[0];
    //     upload(file);
    // });

    // function upload(file) {
    //     var data = new FormData();

    //     data.append("FileName", file);
    //     data.append('chapterID', chapterID);
    //     data.append('courseID', courseID);
    //     data.append('type', 'video');
    //     $.ajax({
    //         xhr: function () {
    //             var xhr = new window.XMLHttpRequest();

    //             xhr.upload.addEventListener("progress", function (evt) {
    //                 $('#progress-bar').css("display", "block");

    //                 if (evt.lengthComputable) {
    //                     var percentComplete = evt.loaded / evt.total;
    //                     percentComplete = parseInt(percentComplete * 100);
    //                     console.log(percentComplete);
    //                     // $('#progress-bar-fill').css('width', percentComplete + '%');
    //                     $("#progress-bar").attr('aria-valuenow', percentComplete).css('width', percentComplete + '%').text(percentComplete + '%');

    //                     if (percentComplete === 100) {
    //                         // $('#progress-bar').css("display", "none");
    //                         let div = $('#video-drag').parent().parent();
    //                         $('#video-drag').css({
    //                             'display': 'none'
    //                         });

    //                         div.append(`
    //                                 <video width="400" height="200" controls>
    //                                 <source src="../uploads/${data.media_name}" type="video/mp4">
    //                                 Your browser does not support the video tag.
    //                             </video>
    //                         `);

    //                         $(div).hover(function () {
    //                             $(this).css("border", "1px solid red");
    //                         }, function () {
    //                             $(this).css("border", '0')
    //                         })

    //                         $('.video-div').resizable({
    //                             containment: $('.editor-canvas'),
    //                             grid: [20, 20],
    //                             autoHide: true,
    //                             minWidth: 150,
    //                             minHeight: 150
    //                         });
    //                     }

    //                 }
    //             }, false);

    //             return xhr;
    //         },
    //         url: save_video_url,
    //         data: data,
    //         contentType: false,
    //         processData: false,
    //         method: 'POST',
    //         type: 'POST',
    //         success: function (data) {
    //             console.log(data);
    //         }

    //     });

    // }

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                let div = $(input).parent().parent().parent();
                div.find('video').remove();
                var data = new FormData();
                $.each(input.files, function (i, file) {
                    data.append('file-' + i, file);
                });
                data.append('csrfmiddlewaretoken', csrf_token);
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
                    beforeSend: function () {
                        div.append(`<div class="loader" id="loadingDiv"></div>
                        <p id = "percentcomplete"></p>
                        `)
                        $('#loadingDiv').show();
                    },
                    error: function (errorThrown) {
                        alert("Failed to upload Video" + errorThrown)
                        div.find('#loadingDiv').remove();
                        div.find('#percentcomplete').remove();
                    },
                    success: function (data) {
                        div.find('#loadingDiv').remove();
                        div.find('#percentcomplete').remove();
                        div.find('p').remove();
                        div.find('.progress').remove();
                        if (data.hasOwnProperty('html')) {
                            var html = $(data.html);
                            $(html).css('height', '100%')
                            $(html).css('width', '100%')

                            div.append(`
                                <video width="100%" height="100%">
                                    <source src="${data.link}">
                                </video>
                            `);
                        } else {
                            div.append(`
                                <video width="100%" height="100%" controls>
                                    <source src="${'/media/chapterBuilder/' + courseID + '/' + chapterID + '/' + data.media_name}"  type="video/mp4">
                                </video>
                            `)
                        }
                    },
                    xhr: function () {
                        var xhr = new window.XMLHttpRequest();

                        xhr.upload.addEventListener("progress", function (evt) {
                            $('#progress-bar').css("display", "block");

                            if (evt.lengthComputable) {
                                var percentComplete = evt.loaded / evt.total;
                                percentComplete = parseInt(percentComplete * 100);
                                $('#percentcomplete').text(percentComplete + '%')
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

                                    $(div).hover(function () {
                                        $(this).css("border", "1px solid red");
                                    }, function () {
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

    $(".video-form").off().change(function (e) {
        readURL(this);
    });
}

function _3dFunction(top = null, left = null, file = null, height = null, width = null) {
    const _3d = new _3Dobject(
        top,
        left,
        file,
        height, width);
    _3d.renderDiagram();

    // $('#_3dfile-link').on('change', function (e) {
    //     $('#mtl-file').prop('disabled', false);
    // });

    $('._3dobj-div').on('click', '.fa-upload', function (e) {
        // trigger = parseInt(e.target.id) + 1;
        // $('#' + trigger).trigger('click');
        $('#_3dfile-link').val('');
        // $('#mtl-file').val('');
        // $('#mtl-file').prop('disabled', true);
        $('#link-3d-submit').val(parseInt(e.target.id))
        $('#link-3d-modal').modal();
    });

    $('.fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('._3dobj-div').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 150,
        minHeight: 150,
        stop: function (e, ui) {
            var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        },
    });

    $('.3dobj').on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        //   $(this).css('border',"2px solid #39F")
    });

    function readURL(upload_btn) {
        if ($('#_3dfile-link')[0].files.length != 0) {
            var obj = $('#_3dfile-link')[0].files[0];
        } else {
            alert("Please select a file to upload")
            return false
        }
        // if ($('#mtl-file')[0].files.length != 0) {
        //     var mtl = $('#mtl-file')[0].files[0];
        // } else {
        //     var mtl = null
        // }

        let div = $('#' + upload_btn.val()).parent().parent();
        var data = new FormData();

        if ($(div).find('iframe').length > 0) {
            if ($('#tabs-for-download').find('iframe[src$="' + $(div).find('iframe').attr('src') + '"]').length == 1) {
                tobedeletedfiles._3d.push($(div).find('iframe').attr('src'));
            }
        }

        data.append('csrfmiddlewaretoken', csrf_token);
        data.append('objfile', obj);
        // data.append('mtlfile', mtl);
        data.append('type', '3d');
        data.append('chapterID', chapterID);
        data.append('courseID', courseID);
        $.ajax({
            url: save_3d_url,
            data: data,
            contentType: false,
            processData: false,
            enctype: 'multipart/form-data',
            method: 'POST',
            type: 'POST',
            beforeSend: function () {
                div.append(`<div class="loader" id="loadingDiv"></div>`)
                $('#loadingDiv').show();
            },
            error: function (errorThrown) {
                alert("Failed to upload File")
                div.find('#loadingDiv').remove();
            },
            success: function (data) {
                _3dFunction(div.css('top'),
                    div.css('left'), '/media/chapterBuilder/' + courseID + '/' + chapterID + '/' + data.objname, div.css('height'), div.css('width'));
                div.remove()
            },
            error: function (data, status, errorThrown) {
                alert(data.responseJSON.message);
            }
        });

        $('#_3dobj-drag').css({
            'display': 'none'
        })

        $(div).hover(function () {
            $(this).css("border", "1px solid red");
        }, function () {
            $(this).css("border", '0')
        })

        $('._3dobj').resizable({
            containment: $('#tabs-for-download'),
            grid: [20, 20],
            autoHide: true,
            minWidth: 150,
            minHeight: 150
        });

        $('._3dobj').css({
            'resize': 'both'
        });
    }

    $("#link-3d-submit").unbind().off().click(function (e) {
        $('#link-3d-modal').modal('hide');
        readURL($(this));
    });
}

// End of Element Function

$(document).ready(function () {
    $("#import_zip_link").on('click', function (e) {
        e.preventDefault();
        $("#importzipfile:hidden").trigger('click');
    });

    $('#loadingDiv').hide();


    // title click function
    $(".tlimit").on("click", function () {
        $("#title_id").css({
            'display': 'block'
        });
    });

    // Making sidebar tools draggable
    $(".draggable").draggable({
        helper: "clone",
        revert: "invalid",
        cursor: "pointer",
        cursorAt: {
            top: 56,
            left: 56
        },
    });

    $(".editor-canvas").droppable({
        drop: function (event, ui) {
            $(this).removeClass("over");
            dropfunction(event, ui)
        },
        over: function (event, ui) {
            $(this).addClass("over");
        },
        out: function (event, ui) {
            $(this).removeClass("over");
        },
    });
    // $("body").on('DOMSubtreeModified', "#tab", function() {
    //     console.log('changed');
    // });

    // background color for pages
    $('#tabs-for-download').click(function () {
        setThumbnailok = true
        var theInput = $('#tabs-for-download').find('.page-background')[0];
        var theColor = theInput.value;
        theInput.addEventListener("input", function () {
            $('.current').css('background-color', theInput.value)
            data.pages[window.currentPage][0].backgroundcolor = theInput.value
        }, false);
    })

    $("#add-page-btn").on("click", function () {
        newpagefunction();
    });
    setslider()

    $('.tabs-to-click > ul > li:first').remove()

    // if(localStorage.getItem(`chapter_${chapterID}_currentPage`) && localStorage.getItem(`chapter_${chapterID}_currentPage`) <= data.numberofpages && localStorage.getItem(`chapter_${chapterID}_currentPage`) > 0){
    //     window.firstload = false
    //     changePage(localStorage.getItem(`chapter_${chapterID}_currentPage`));
    // }else{
    //     changePage('1');
    // }
    changePage('1');

    // Button Form Submit
    $('#btn-submit').on('click', function () {
        var btn_name = $('#btn-name').val();
        var btn_link = $('#btn-link').val();
        var btn_id = $('#button_id').val();
        if (btn_link != "") {
            $('#' + btn_id).attr({
                "href": `http://${btn_link}`
            });
        } else {
            $('#' + btn_id).removeAttr('href');
        }
        $('#' + btn_id).parent().parent().find('.resizable-text-only').text(btn_name);
        $('#btn-modal').modal('hide');
    })

    // ======================================================================

    // quiz Form Submit
    $('#quiz-submit').on('click', function () {
        var quiz_name;
        var quiz_span_name = $('#quiz-name').val();
        var quiz_link = $('#quiz-link').val();
        var quiz_id = $('#quiz_id').val();
        if($('#quiz-btn-name').val() == 'Select Quiz' && quiz_link != ""){
            quiz_name = "Play Quiz"
        } else {
           quiz_name = $('#quiz-btn-name').val()
        }
        
        if (quiz_link != "") {
            $('#' + quiz_id).attr({
                "href": `${quiz_link}`
            });
        } else {
            $('#' + quiz_id).removeAttr('href');
        }
        $('#' + quiz_id).parent().parent().find('.resizable-text-only').text(quiz_name);
        $('#' + quiz_id).parent().parent().find('.quiz-name').text(quiz_span_name)
        $('#quiz-modal').modal('hide');
        if(tempVarStorage){
            tempVarStorage = undefined
        }
    })

    $('#myTable').on('click', '.selectquiz', function () {
        $('#quiz-name').val($(this).closest('td').prev('td').text().trim())
        $('#quiz-link').val(`/quiz/quiz${$(this).val().trim()}/take/`)
        $('#quiz-btn-name').parent().show()
        $('#quiz-name').parent().parent().show()
        $('#quiz-submit').click()
    })
    // ======================================================================

    // survey Form Submit
    $('#survey-submit').on('click', function () {
        var survey_name;
        var survey_link = $('#survey-link').val();
        var survey_id = $('#survey_id').val();
        var survey_span_name = $('#survey-name').val();

        if($('#survey-btn-name').val() == 'Select Survey' && survey_link != ""){
            survey_name = "Take Survey"
        } else {
            survey_name = $('#survey-btn-name').val()
        }        
        
        if (survey_link != "") {
            $('#' + survey_id).attr({
                "href": `${survey_link}`
            });
        } else {
            $('#' + survey_id).removeAttr('href');
        }
        $('#' + survey_id).parent().parent().find('.resizable-text-only').text(survey_name);
        $('#' + survey_id).parent().parent().find('.survey-name').text(survey_span_name)
        $('#survey-modal').modal('hide');
        if(tempVarStorage){
            tempVarStorage = undefined
        }
    })

    $('#mySurveyTable').on('click', '.selectsurvey', function () {
        $('#survey-name').val($(this).closest('td').prev('td').text().trim())
        $('#survey-link').val(`/students/questions_student_detail/detail/${$(this).val().trim()}`)

        $('#survey-btn-name').parent().show()
        $('#survey-name').parent().parent().show()
        $('#survey-submit').click()
    });

    $("#importzipfile").change(function (e) {
        var confirmation = confirm('All current data will be replaced! Are you sure you want to continue?')
        if (confirmation == false) {
            return false
        }
        let input = this.files[0];
        var fileExtension = ['zip'];
        if ($.inArray($(this).val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            alert(fileExtension.join(', ') + " formats allowed only");
            return false
        }
        var filedata = new FormData();
        filedata.append("filename", input);
        filedata.append("chapterID", chapterID);
        filedata.append("courseID", courseID);
        filedata.append("csrfmiddlewaretoken", csrf_token);
        $.ajax({
            url: import_zip_url,
            contentType: false,
            processData: false,
            data: filedata,
            enctype: 'multipart/form-data',
            method: 'POST',
            beforeSend: function () {
                $('#tabs-for-download').append(`<div class="loader" id="loadingDiv"></div>
                <p id = "percentcomplete"></p>
                `)
                $('#loadingDiv').show();
            },
            success: function (success_data) {
                $('#tab').empty();
                $('.tabs-to-click > ul').empty();
                data = success_data;
                if (localStorage.getItem(`chapter_${chapterID}_currentPage`) && localStorage.getItem(`chapter_${chapterID}_currentPage`) <= data.numberofpages && localStorage.getItem(`chapter_${chapterID}_currentPage`) > 0) {
                    window.firstload = false
                    // changePage(localStorage.getItem(`chapter_${chapterID}_currentPage`));
                    window.currentPage = localStorage.getItem(`chapter_${chapterID}_currentPage`)
                    display(data, localStorage.getItem(`chapter_${chapterID}_currentPage`))
                } else {
                    // changePage('1');
                    window.currentPage = '1'
                    display(data, 1)
                }
                // window.currentPage = '1'
                // display(data,1)
                setslider()
                $('.pagenumber[value=' + window.currentPage + ']').addClass('current')
            },
            error: function (errorThrown) {
                console.log(errorThrown)
                alert(errorThrown.responseJSON.message)
            },
            complete: function () {
                $('#loadingDiv').remove();
            }
        });
    });
    
    
    
});
$('#quiz_create_link').click(function(e){
    $('#iframeholder iframe').on('load', function(){
        var iframe = $('#iframeholder iframe').contents();
        $('#iframeholder iframe').contents().find("#quiz_form_ajax").on('click', '#quiz_submit_button',function(){
            setTimeout(() => {
                modalcloseFunction()
            }, 1500)
        });
    });
   
})
$('#survey_create_link').click(function(e){
    $('#iframeholder iframe').on('load', function(){
        var iframe = $('#iframeholder iframe').contents();
        $('#iframeholder iframe').contents().find("#survey_form_ajax").on('click', '#survey_submit_button',function(){
            setTimeout(() => {
                modalcloseFunction()
            }, 1500)
        });
    });
   
})
function modalcloseFunction(){
    $('#closeiframebtn').click();
    tempVarStorage.click()
}

let sidebarWidth = $(".sidebar").width(); // get width of sidebar
let toolbarheight = $('.editor-toolbar').height();


function clearPage(page_number){
    $('#tab').empty();
    if(page_number in data.pages){
        data.pages[page_number] = ''
    }
}

function dropfunction(event, ui) {
    let top = ui.helper.position().top;
    let left = ui.helper.position().left;
    
    $(this).removeClass("over");
    if (ui.helper.offset().top < $('#tab').offset().top) {
        top = $('#tab').position().top
    }

    if (ui.helper.offset().top + (0.25 * $('#tab').height()) > $('#tab').height()) {
        top = $('#tab').height() - (0.25 * $('#tab').height())
    }

    if (ui.helper.offset().left + (0.20 * $('#tab').width()) > $('#tab').width() && !ui.helper.hasClass('button')) {   // 0.25 is multiplied to sum the height of element to the current pointer position
        left = $('#tab').width() - (0.40 * $('#tab').width()) + sidebarWidth
    }
    else if (ui.helper.offset().left > $('#tab').width() && ui.helper.hasClass('button')) {
        left = $('#tab').width() - (0.15 * $('#tab').width()) + sidebarWidth
    }
    if (ui.helper.hasClass('textbox')) {
        TextboxFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            "20%", "35%");
    } else if (ui.helper.hasClass('picture')) {
        PictureFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert(left - sidebarWidth, $('#tabs-for-download').width())) + '%',
            null, '40%', '30%'
        );
    } else if (ui.helper.hasClass('video')) {
        VideoFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            null, '30%', '40%'
        );
    } else if (ui.helper.hasClass('buttons')) {
        ButtonFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            null, '13%', '15%'
        );
    } else if (ui.helper.hasClass('quiz')) {
        QuizFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            null, '13%', '15%'
        );
    } else if (ui.helper.hasClass('survey')) {
        SurveyFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            null, '13%', '15%'
        );
    } else if (ui.helper.hasClass('grid-1')) {
        clearPage(window.currentPage)
        PictureFunction(
            top = 0 + '%',
            left = 0 + '%',
            null,
            width = "100%", height = "50%");


        // ===============for textbox inside grid-1============
        TextboxFunction(
            top = "50%",
            left = 0 + '%',
            height = "45%", width = '100% '
        );
    } else if (ui.helper.hasClass('grid')) {
        clearPage(window.currentPage)
        VideoFunction(
            top = 0 + '%',
            left = 0 + '%',
            null,
            height = "50%", width = "100%");


        // ===============for textbox inside grid-1============
        TextboxFunction(
            top = "52%",
            left = 0 + '%',
            height = "45%", width = "100%"
        );
    } else if (ui.helper.hasClass('title-slide')) {
        clearPage(window.currentPage)
        PictureFunction(
            top = 0 + '%',
            left = 0 + '%',
            null,
            width = "49%", height = "60%");
        PictureFunction(
            top = 0 + '%',
            left = "51%",
            null,
            width = "49%", height = "60%");
        TextboxFunction(
            top = "62%",
            left = 0 + '%',
            height = "35%", width = "100%",
        );
    } else if (ui.helper.hasClass('title-content-details')) {
        clearPage(window.currentPage)
        TextboxFunction(
            top = "0%",
            left = 0 + '%',
            height = "10%", width = "100%",
            
        );
        TextboxFunction(
            top = "13%",
            left = 0 + '%',
            height = "84%", width = "100%",
            
        );
    } else if (ui.helper.hasClass('pdf-text')) {
        PDFFunction(
            top = "0%",
            left = 0 + '%',
            link = null,
            height = "60%", width = "100%");


        // ===============for textbox inside grid-1============
        TextboxFunction(
            top = "62%",
            left = 0 + '%',
            height = "35%", width = "100%"
        );

    } else if (ui.helper.hasClass('3dobject')) {
        _3dFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            null, '30%', '40%'
        );
    } else if (ui.helper.hasClass('Pdf')) {
        PDFFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            null, '30%', '40%'
        );
    }
    $('.fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });
}

function displaypagenumbers() {
    $('.pagenumber').each(function (key, value) {
        $(this).parent().find('p').text(key + 1);
    })
}

function setslider() {
    if (data.pages) {
        $.each(data.pages, function (key, value) {
            if (value[0]['thumbnail'] == "") {
                $(".tabs-to-click ul").append(`
                    <div class="canvas-relative" style="position:relative"> 
                
                        <li class="tabs-link pagenumber" value="${key}" onclick="changePage('tab${key}')"></li>
                        <div style="position:absolute; top:0px;left:0;right:0; margin-top:5px;padding-left:5px">
                                <p style="display:inline-block">${key}</p> 
                                <span style="float:right" >
                                    <button class="clone-page-btn"  value="${key}">
                                    <span  data-title= "Clone Page" >
                                    <i class="fa fa-clone " aria-hidden="true"></i>
                                    </span>
                                    
                                    </button>
                                </span>

                                <span style="float:right">
                                    <button class="delete-page-btn"   value="${key}">
                                    <span data-title= "Delete Page">
                                    <i class="fa fa-times " aria-hidden="true"></i>
                                    </span>

                                   
                                    </button>
                                </span>
                            </div>
                        
                        <hr class="white-hr"/>
                    </div>
                        `);
            } else {
                $(".tabs-to-click ul").append(`
                    <div class="canvas-relative" style="position:relative"> 
                    <li class="tabs-link pagenumber" value="${key}" onclick="changePage('tab${key}')" 
                        style = "
                            background-image: url('${value[0]['thumbnail']}'); 
                            background-position: center;
                            background-size: contain;
                            background-repeat: no-repeat;
                        ">
                    </li>
                    <div style="position:absolute; top:0px;left:0;right:0; margin-top:5px;padding-left:5px">
                        <p style="display:inline-block">${key}</p> 
                        <span style="float:right" >
                        <button class="clone-page-btn"  value="${key}">
                        <span  data-title= "Clone Page" >
                        <i class="fa fa-clone " aria-hidden="true"></i>
                        </span>
                        
                        </button>
                    </span>

                    <span style="float:right">
                        <button class="delete-page-btn"   value="${key}">
                        <span data-title= "Delete Page">
                        <i class="fa fa-times " aria-hidden="true"></i>
                        </span>

                       
                        </button>
                    </span>
                    </div>
                            
                    <hr class="white-hr"/>
                    </div>
                `);
            }
        });
        // displaypagenumbers()
    }
}

function newpagefunction(new_page_num) {
    if ($(".tabs-to-click ul li").last().length == 0) {
        var num_tabs = 1
    } else if (new_page_num) {
        var num_tabs = new_page_num
    } else {
        var num_tabs = $(".tabs-to-click ul li").last().val() + 1;
    }
    $(".tabs-to-click ul").append(`
        <div class="canvas-relative" style="position:relative"> 
            <li class="tabs-link pagenumber current" value="${num_tabs}" onclick="changePage('tab${num_tabs}')"></li>
            <div style="position:absolute; top:0px;left:0;right:0; margin-top:5px;padding-left:5px">
                    <p style="display:inline-block"></p> 
                    <span style="float:right" >
                                    <button class="clone-page-btn"  value="${num_tabs}">
                                    <span  data-title= "Clone Page" >
                                    <i class="fa fa-clone " aria-hidden="true"></i>
                                    </span>
                                    
                                    </button>
                                </span>

                                <span style="float:right">
                                    <button class="delete-page-btn"   value="${num_tabs}">
                                    <span data-title= "Delete Page">
                                    <i class="fa fa-times " aria-hidden="true"></i>
                                    </span>

                                   
                                    </button>
                                </span>
                </div>
            
            <hr class="white-hr"/>
        

        </div>
    `);
    // $(".tabs").append(
    //     `<p id='tab${num_tabs}' style="display:block; background-color: rgb(255, 255, 255);" class="tab-content-no droppable editor-canvas ui-droppable current">
    //             <input type = "color" value = "#ffffff" class="page-background">
    //     </p>`
    // );

    $('#tab').attr('value', num_tabs)
    // $('#copy_tab').attr('value', num_tabs)

    $(".editor-canvas").droppable({
        drop: function (event, ui) {
            dropfunction(event, ui);
        }
    });
    displaypagenumbers();
    if (!window.firstload) {
        changePage('tab' + num_tabs)
    }

}

function displaypagenumbers() {
    $('.pagenumber').each(function (key, value) {
        $(this).parent().find('p').text(key + 1);
    })
}

function display(data = "", currentPage = '1') {
    $('#tab').empty()
    $('#tab').css('background-color', '#fff')
    $('#chaptertitle').text(chaptertitle);
    if (data.pages) {
        $.each(data.pages, function (key, value) {
            if (key == window.currentPage) {
                // $('.tabs-to-click > ul > div > li')[key - 1].click()
                $.each(value, function (count) {
                    // -------------------------------
                    $.each(value[count], function (div, div_value) {
                        if (div == 'textdiv') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)
                                TextboxFunction(
                                    css_value.tops,
                                    css_value.left,
                                    css_value.height,
                                    css_value.width,
                                    css_value.content
                                );
                            });
                        }
                        if (div == 'pic') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)
                                PictureFunction(
                                    css_value.tops,
                                    css_value.left,
                                    css_value['background-image'],
                                    css_value.width,
                                    css_value.height,
                                );
                            });
                        }

                        if (div == 'btn-div') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)

                                ButtonFunction(
                                    css_value.tops,
                                    css_value.left,
                                    css_value.link,
                                    css_value.height,
                                    css_value.width,
                                    css_value.btn_name,
                                    css_value.font_size
                                );
                            });
                        }

                        if (div == 'quizdiv') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)

                                QuizFunction(
                                    css_value.tops,
                                    css_value.left,
                                    css_value.link,
                                    css_value.height,
                                    css_value.width,
                                    css_value.quiz_btn_name,
                                    css_value.quiz_name,
                                    css_value.font_size
                                );
                            });
                        }
                        if (div == 'surveydiv') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)

                                SurveyFunction(
                                    css_value.tops,
                                    css_value.left,
                                    css_value.link,
                                    css_value.height,
                                    css_value.width,
                                    css_value.survey_btn_name,
                                    css_value.survey_name,
                                    css_value.font_size
                                );
                            });
                        }
                        if (div == 'pdf') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)
                                PDFFunction(
                                    css_value.tops,
                                    css_value.left,
                                    css_value['link'],
                                    css_value.height,
                                    css_value.width,
                                );
                            });
                        }

                        if (div == 'video') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)
                                let link;
                                if (css_value.hasOwnProperty('online_link') && css_value.online_link) {
                                    link = css_value.online_link
                                } else {
                                    link = css_value.local_link
                                }
                                VideoFunction(
                                    css_value.tops,
                                    css_value.left,
                                    link,
                                    css_value.height,
                                    css_value.width,
                                );
                            });
                        }

                        if (div == '_3d') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)
                                _3dFunction(
                                    css_value.tops,
                                    css_value.left,
                                    css_value['link'],
                                    css_value.height,
                                    css_value.width,
                                );
                            });
                        }

                        if (div == 'thumbnail') {
                            $($('.tabs-to-click').find('li')[key - 1]).css({
                                'background-image': 'url("' + div_value + '")',
                                'background-position': 'center',
                                'background-size': 'contain',
                                'background-repeat': 'no-repeat',
                            })
                        }

                        if (div == 'backgroundcolor') {
                            $('#tab').css('background-color', div_value)
                        }
                    });
                });
                return
            }

        });
    }
}

function updateData(prev_page, prev_data) {
    if (prev_page == 0) {
        return
    }
    var promise = new Promise((resolve, reject) => {
        setThumbnails(prev_page)
        resolve('success')
    })
    promise.then((successmessage) => {
        // $('#tab').empty()
        setTimeout(function () {
            storethumbnails(prev_page)
        }, 1000)
    })
    var textdiv = [];
    var picdiv = [];
    var buttondiv = [];
    var pdf = [];
    var video = [];
    var _3d = [];
    var quizdiv = [];
    var surveydiv = [];

    const obj = $(prev_data).children();

    let tops;
    let left;
    let width;
    let height;
    let content;
    let numberofpages = $('.pagenumber').length;
    $.each(obj, function (i, value) {
        if (value.classList.contains('textdiv')) {
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
        if (value.classList.contains('pic')) {
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
        if (value.classList.contains('btn-div')) {
            buttondiv.push(
                {
                    'tops': $(this)[0].style.top,
                    'left': $(this)[0].style.left,
                    'width': $(this)[0].style.width,
                    'height': $(this)[0].style.height,
                    'link': $(this).find("a").attr('href'),
                    'btn_name': $(this).find(".resizable-text-only").text(),
                    'font_size': $(this).find('.resizable-text-only').css('font-size')
                }
            );
        }
        if (value.classList.contains('pdfdiv')) {
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
        if (value.classList.contains('video-div')) {
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
        if (value.classList.contains('_3dobj-div')) {
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
        if (value.classList.contains('quiz-div')) {
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
        if (value.classList.contains('survey-div')) {
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
    if (!data.pages) {
        var pages = {}
        backgroundcolor = $("#tab").css('background-color')
        pages[prev_page] = [{
            'textdiv': textdiv,
            'pic': picdiv,
            'btn-div': buttondiv,
            'pdf': pdf,
            'video': video,
            '_3d': _3d,
            'quizdiv': quizdiv,
            'surveydiv': surveydiv,
            'backgroundcolor': backgroundcolor
        }]

        data = {
            'numberofpages': numberofpages,
            'chaptertitle': $('#chaptertitle').text(),
            'pages': pages,
            'canvasheight': positionConvert($('#tabs-for-download').css('height'), $('body').height()),
            'canvaswidth': positionConvert($('#tabs-for-download').css('width'), $('body').width()),
        };
    } else {
        backgroundcolor = $("#tab").css('background-color')
        data.pages[prev_page] = [{
            'textdiv': textdiv,
            'pic': picdiv,
            'btn-div': buttondiv,
            'pdf': pdf,
            'video': video,
            '_3d': _3d,
            'quizdiv': quizdiv,
            'surveydiv': surveydiv,
            'backgroundcolor': backgroundcolor
        }]
    }
}

function storethumbnails(prev_page) {
    thumbnail = ($('.pagenumber[value= ' + prev_page + ']')[0].style['background-image']).replace(/^url\(["']?/, '').replace(/["']?\)$/, '');
    data.pages[prev_page][0].thumbnail = thumbnail
}

function changePage(page_number) {
    let prev_page = window.currentPage.replace(/^\D+/g, '')
    if (window.firstload) {
        // newpagefunction()
        window.firstload = false
        if (data.pages) {
            $('.pagenumber[value=1]').addClass('current')
            // $('#add-page-btn').click();
            display(data)
            return
        } else {
            newpagefunction()
        }
    } else {
        window.currentPage = page_number.replace(/^\D+/g, '')
        let prev_data = $('#tab').clone()
        // var promise = new Promise((resolve,reject) => {
        //     setThumbnails(prev_page)
        //     resolve('success')
        // })
        updateData(prev_page, prev_data)

        $('#copy_tab').html($('#tab').html())
        $('#copy_tab').attr('value', prev_page)
        $('#tab' + window.currentPage).css('display', 'block')
        if (prev_page != window.currentPage) {
            $('.tabs-to-click ul li[value= ' + window.currentPage + ']').addClass('current')
            $('.tabs-to-click ul li[value= ' + prev_page + ']').removeClass('current')
            // promise.then((successmessage) => {
            //     // $('#tab').empty()
            //     setTimeout(function(){
            //         console.log('hello')
            //         storethumbnails(prev_page)
            //     },1000)
            // })
        }
        display(data)
    }
    // localStorage.setItem(`chapter_${chapterID}_currentPage`, window.currentPage);
}

$('#tab').on('click', '.file-upload-icon', function(){
    $(this).closest('.ui-draggable').find('.fa-upload').click();
})

// Media File deletion
function deleteFile() {
    $.ajax({
        url: delete_file_url,
        data: {
            'csrfmiddlewaretoken': csrf_token,
            'old': JSON.stringify(tobedeletedfiles),
        },
        method: 'POST',
        type: 'POST',

        error: function (errorThrown) {
            alert("Failed to delete existing file")
        },
        success: function (data) {
        },
    });
}

// delete page function
$('.tabs-to-click').on('click', '.delete-page-btn', function () {
    var confirmation = confirm("Are you sure you want to delete?")
    if (confirmation == false) {
        return false
    }

    if ($(this).parent().parent().parent().find('li')[0].classList.contains('current')) {
        setThumbnailok = false
        if ($(this).parent().parent().parent().prev().find('li').length != 0)
            $(this).parent().parent().parent().prev().find('li')[0].click();
        else if ($(this).parent().parent().parent().next().find('li').length != 0)
            $(this).parent().parent().parent().next().find('li')[0].click()
        else {
            alert("cannot delete only page");
            return false
        }
    }
    $(this).parent().parent().parent().remove();
    delete data.pages[this.value]

    numberofloops = Object.keys(data.pages).length + 1
    for (x = this.value; x <= numberofloops; x++) {
        $('.pagenumber[value="' + (parseInt(x) + 1) + '"').parent().find('.clone-page-btn').attr({
            "value": parseInt(x),
        });
        $('.pagenumber[value="' + (parseInt(x) + 1) + '"').parent().find('.delete-page-btn').attr({
            "value": parseInt(x),
        });
        $('.pagenumber[value="' + (parseInt(x) + 1) + '"').attr({
            "value": x,
            "onclick": "changePage('tab" + x + "')"
        })
        data.pages[x] = (data.pages[parseInt(x) + 1])
        delete data.pages[parseInt(x) + 1]
    }
    var promise = new Promise((resolve, reject) => {
        displaypagenumbers()
        resolve('success')
    })
    promise.then((successmessage) => {
        setTimeout(function () {
            window.currentPage = $('.pagenumber.current').attr('value')
        }, 200)
    })
});

// clone Page function
$('.tabs-to-click').on('click', '.clone-page-btn', function () {
    var prev_data = $('#tab').clone()
    $(this).attr('disabled', true)
    var promise = new Promise((resolve, reject) => {
        updateData(window.currentPage, prev_data)
        resolve('success')
    })
    source = this.value
    destination = parseInt(source) + 1
    // numberofloops = Object.keys(data.pages).length
    $.each($('.pagenumber'), function () {
        if (this.value > source) {
            let new_value = parseInt(this.value) + 1
            $(this).attr({
                "value": new_value,
                "onclick": "changePage('tab" + new_value + "')"
            });
            $(this).parent().find('.clone-page-btn').attr({
                "value": new_value,
            });
            $(this).parent().find('.delete-page-btn').attr({
                "value": new_value,
            });
        }
    });
    numberofloops = Object.keys(data.pages).length
    promise.then((successmessage) => {
        setTimeout(() => {
            // window.currentPage = 'tab'+(parseInt(window.currentPage) + 1)
            for (x = numberofloops; x >= (parseInt(this.value) + 1); x--) {
                data.pages[parseInt(x) + 1] = data.pages[x]
                // delete data.pages[parseInt(x)]
            }
            data.pages[destination] = data.pages[source]
            // $('.current.pagenumber').removeClass('current')
            var num_tabs = parseInt(this.value) + 1;
            let copy = $(this).parent().parent().parent().clone();
            // for cloning page navigation tabs
            copy.find('.pagenumber').removeClass('current')
            copy.find('.clone-page-btn').val(num_tabs);
            copy.find('.clone-page-btn').attr('disabled', false)
            copy.find('.delete-page-btn').val(num_tabs);
            copy.find('.pagenumber').val(num_tabs);
            copy.find('.pagenumber').attr('onclick', 'changePage("tab' + num_tabs + '")');
            $(this).parent().parent().parent().after(copy);
            if (source < window.currentPage) {
                window.currentPage = 'tab' + (parseInt(window.currentPage) + 1)
            }
            // changePage('tab'+num_tabs)
            // ===================================================================================
            $(".editor-canvas").droppable({
                drop: function (event, ui) {
                    dropfunction(event, ui)
                }
            });

            displaypagenumbers();

        }, 200)
        setTimeout(() => {
            $(this).attr('disabled', false)
        }, 2000)
    })
});



// $('#tabs-for-download').on('click', '.textdiv', function () {
//     $this = $('.note-editable:focus')
//     if ($('.note-editable:focus').html() == "Type Something Here...") {
//         $('.note-editable:focus').html("")
//     }
//     $($this).on('focusout', function () {
//         if ($($this).html() == "") {
//             $($this).html("Type Something Here...")
//         }
//     })
// });

async function resizeImage(url, width, height, callback, dive) {
    var sourceImage = new Image();

    sourceImage.onload = function () {
        // Create a canvas with the desired dimensions
        var canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;

        // Scale and draw the source image to the canvas
        canvas.getContext("2d").drawImage(sourceImage, 0, 0, width, height);

        // Convert the canvas to a data URL in PNG format
        callback(canvas.toDataURL(), dive);
    }

    sourceImage.src = url;
}

async function setThumbnails(prev_page) {
    if (!setThumbnailok) {
        return false
    }
    $('#tab').find('.pdfdiv').each(function () {
        $(this).css({
            'background-image': `url('${pdf_icon}')`,
            'background-position': 'center',
            'background-size': 'contain',
            'background-repeat': 'no-repeat'
        })
    })
    $('#tab').find('.video-div').each(function () {
        $(this).css({
            'background-image': `url('${video_icon}')`,
            'background-position': 'center',
            'background-size': 'contain',
            'background-repeat': 'no-repeat'
        })
    });
    $('#tab').find('._3dobj-div').each(function () {
        $(this).css({
            'background-image': `url('${_3d_icon}')`,
            'background-position': 'center',
            'background-size': 'contain',
            'background-repeat': 'no-repeat'
        })
    })

    html2canvas($('#tab')[0]).then(canvas => {
        $('.pagenumber[value= ' + prev_page + ']').each(function () {
            if (canvas.toDataURL('image/png', 0.00,).startsWith('data:image')) {
                resizeImage(canvas.toDataURL('image/png', 0.00), 60, 30, setThumbnailscallback, $(this));
            }
        });
    });
    setThumbnailok = false
}

function setThumbnailscallback(data, dive) {
    dive.css({
        'background-image': 'url("' + data + '")',
        'background-position': 'center',
        'background-size': 'contain',
        'background-repeat': 'no-repeat',
    });
}