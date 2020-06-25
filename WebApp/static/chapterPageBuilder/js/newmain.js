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
    var cincopaRegExp = /(mediacdnl3.cincopa.com)/g;
    var cincopaMatch = url.match(cincopaRegExp);
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
    } else if (cincopaMatch && cincopaMatch[0].length === 22) {
        $video_element = $('<iframe webkitallowfullscreen mozallowfullscreen allowfullscreen>')
            .attr('frameborder', 0)
            .attr('src', url)
            .attr('width', '100%').attr('height', '100%');
    } else {
        // this is not a known video link. Now what, Cat? Now what?
        return false;
    }
    return $video_element[0];
}

function getVimeoVideoID(url) {
    var vimRegExp = /\/\/(player\.)?vimeo\.com\/([a-z]*\/)*(\d+)[?]?.*/;
    var vimMatch = url.match(vimRegExp);
    if (vimMatch && vimMatch[3].length) {
        return vimMatch[3]
    }
}

function getVimeoThumbnail(url, divid) {
    var vimRegExp = /\/\/(player\.)?vimeo\.com\/([a-z]*\/)*(\d+)[?]?.*/;
    var vimMatch = url.match(vimRegExp);
    if (vimMatch && vimMatch[3].length) {
        $.ajax({
            url: 'https://api.vimeo.com//videos/' + vimMatch[3] + '/pictures/',
            processData: false,
            method: 'GET',
            headers: {
                'Authorization': 'bearer 3b42ecf73e2a1d0088dd677089d23e32',
            },
            success: function (response) {
                $('#' + divid).find('iframe').css({
                    'background-image': `url(${response.data[0].sizes[1].link})`,
                    'background-position': 'center',
                    'background-size': 'contain',
                    'background-repeat': 'no-repeat'
                })
            },
        });
    }
}

function getCincopaThumbnail(url, divid) {
    var ccRegExp = /\/\/(?:www\.)?(?:cincopa.com\/media-platform\/iframe.aspx\?fid=?.+)/g
    var ccRegExpForStart = /(![A-Z])\w.+/g;
    if (url.match(ccRegExp) && url.match(ccRegExpForStart)[0].length == 13) {
        var rid = url.match(ccRegExpForStart)[0].substring(1);
        $.get('https://api.cincopa.com/v2/asset.list.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&rid=' + rid, function (response) {
            if (response.items.length > 0) {
                $('#' + divid).find('iframe').css({
                    'background-image': `url(${response.items[0].thumbnail.url})`,
                    'background-position': 'center',
                    'background-size': 'contain',
                    'background-repeat': 'no-repeat'
                })
                // var img = `<img src = '${response.items[0].thumbnail.url}' width= "100%" height="100%" style = "object-fit: cover;"></img>`
                // $('#' + divid).append(img)
            }
        })
    }
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
                         <i class ="fa fa-trash" id=${id} data-toggle="tooltip" data-placement="bottom"  title='Delete item'></i>
                             <i data-toggle="tooltip" data-placement="bottom"  title='Drag item' class="fas fa-arrows-alt" id="draghere" ></i>
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
            if (!message) {
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
            $('.note-toolbar').css('display', 'none');

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
    constructor(top, left, pic = null, link = null, width = null, height = null) {
        let id = (new Date).getTime();
        let position = {top, left, width, height};
        let message = "";
        if (pic == null && link == null) {
            message = `
                <div class = "file-upload-icon">
                    <img src = "/static/chapterPageBuilder/images/uploadIcon.png" height = "100%" width = "100%"></img>
                </div>
                <p>Drag and drop images here...</p>
                <div class="progressc mx-auto loadingDiv" data-value='0' style="display:none">
                <span class="progress-left">
                            <span class="progress-barc border-primary"></span>
                </span>
                <span class="progress-right">
                            <span class="progress-barc border-primary"></span>
                </span>
                <div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center">
                <div class="h2 font-weight-bold percentcomplete">0<span class="small">%</span></div>
                </div>
                `
        }
        let img = '';
        if (pic != null) {
            img = `<img src = '${pic}' width= "100%" height="100%" style = "object-fit: cover;"></img>`
        }
        if (link != null) {
            getCincopaThumbnail(link, 'pic-' + id)
            img = `<iframe style="width:100%;height:100%;" src="${link}"
                         frameborder="0" allowfullscreen scrolling="no" allow="autoplay; fullscreen"></iframe>`
        }
        let html =
            `<div class='pic' id="pic-${id}">
            <div id="pic-actions">
                <i data-toggle="tooltip" data-placement="bottom"  title='Delete item' class="  fas fa-trash" id=${id} ></i>
              <span  data-toggle="tooltip" data-placement="bottom"  title='Upload File'><i class=" fas fa-upload" id=${id}></i></span>
              <span data-toggle="tooltip" data-placement="bottom"  title='Link Image'>
              <i  class= "fas fa-link imagelink" id=${id}></i>
              </span>
                
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
function play(id) {
    var cld = cloudinary.Cloudinary.new({cloud_name: 'nsdevil-com'});
    var vidElem = $(id)[0]
    var player = cld.videoPlayer(vidElem, {
        showJumpControls: true,
        showLogo: false,
        playbackRates: ['0.25', '0.5', '1', '1.25', '1.5', '2'],
    });
}

class video {
    constructor(top, left, link = null, height = null, width = null) {
        let id = (new Date).getTime();
        this.id = id
        this.link = link
        var now = Math.floor(Math.random() * 900000) + 100000;
        let position = {top, left, height, width};
        let videoobj;
        let message = "";

        if (link != null) {
            if (link.includes('.com')) {
                if (link.includes('vimeo.com')) {
                    getVimeoThumbnail(link, 'video-div-' + id)
                } else if (link.includes('cincopa.com/media-platform')) {
                    getCincopaThumbnail(link, 'video-div-' + id)
                }

                videoobj = `<iframe width="100%" height="94%" src="${link}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>`
            } else if (link.includes('/media/chapterBuilder/')) {
                videoobj = `
                <video controls muted id="video${id}" class="videodim" data-cld-public-id="${link}">
                        <source src="${link}"  type="video/mp4">
                    </video>
                `
            } else {
                videoobj = `
                    <video controls muted id="video${id}"
                        class="videodim cld-video-player cld-video-player-skin-dark example-player"
                        data-cld-public-id="${link}" data-public_id="${link}" data-cld-source-types='["mp4", "ogg", "webm"]'>
                        <source src="${link}"  type="video/mp4">
                    </video>
            `
            }
        } else {
            message = `
            <p>Add video here...<br> <a href ='https://converterpoint.com/' target = '_blank'>Need help converting?</a></p>`;
            if (server_name == 'Indonesian_Server') {
                videoobj = `<div class="progressc mx-auto" data-value='0' id="loadingDiv" style="display:none">
                <span class="progress-left">
                            <span class="progress-barc border-primary"></span>
                </span>
                <span class="progress-right">
                            <span class="progress-barc border-primary"></span>
                </span>
                <div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center">
                <div class="h2 font-weight-bold" id="percentcomplete">0<span class="small">%</span></div>
                </div>
                </div>`;
            } else {
                videoobj = `<div class = "file-upload-icon">
                    <img src = "/static/chapterPageBuilder/images/uploadIcon.png" height = "100%" width = "100%"></img>
                </div>`;
            }
        }
        let html =
            `<div class='video-div' id="video-div-${id}">
                <div id="video-actions">
                    <i data-toggle="tooltip" data-placement="bottom" title='Delete item' class="fas fa-trash" id=${id}></i>
                    <span  data-toggle="tooltip" data-placement="bottom"  title='Upload File'><i class=" fas fa-upload" id=${id}></i></span>
                   
                    <i data-toggle="tooltip" data-placement="bottom"  title='Link File' class="fas fa-link videolink" id=${id}></i>
                </div>
                <div>
                    <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                    <input type='file' name="userImage" accept="video/*" style="display:none" id=${id + 1} class="video-form" />
                    </form>
                    ${videoobj}
                    <p id="video-drag">${message}</p>
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


// =====================For Audio===========================================
class Audio {
    constructor(top, left, link = null, height = null, width = null) {
        let id = (new Date).getTime();
        this.id = id
        this.link = link
        var now = Math.floor(Math.random() * 900000) + 100000;
        let position = {top, left, height, width};
        let audioobj;
        let message = "";

        if (link != null) {
            if (link.includes('.com')) {
                audioobj = `<iframe width="100%" height="94%" src="${link}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>`
            } else if (link.includes('/media/chapterBuilder/')) {
                audioobj = `
                <audio controls muted id="audio${id}" class="audiodim" data-cld-public-id="${link}">
                        <source src="${link}"  type="audio/mpeg">
                    </audio>
                `
            } else {
                audioobj = `
                    <audio controls muted id="audio${id}"
                        class="audiodim cld-video-player cld-video-player-skin-dark example-player"
                        data-cld-public-id="${link}" data-public_id="${link}" data-cld-source-types='["mp3", "ogg", "mpeg"]'>
                        <source src="${link}"  type="audio/mp3">
                    </audio>
            `
            }
        } else {
            message = `
            Add Audio here...<br> `;
            audioobj = `<div class="progressc mx-auto" data-value='0' id="loadingDiv" style="display:none">
                <span class="progress-left">
                            <span class="progress-barc border-primary"></span>
                </span>
                <span class="progress-right">
                            <span class="progress-barc border-primary"></span>
                </span>
                <div class="progress-value w-100 h-100 rounded-circle d-flex align-items-center justify-content-center">
                <div class="h2 font-weight-bold" id="percentcomplete">0<span class="small">%</span></div>
                </div>
                </div>`;

        }
        let html =
            `<div class='audio-div'>
                <div id="audio-actions">
                    <i data-toggle="tooltip" data-placement="bottom"  title='Delete item' class="fas fa-trash" id=${id}></i>
                    <span  data-toggle="tooltip" data-placement="bottom"  title='Upload File'><i class=" fas fa-upload" id=${id}></i></span>
                    <i data-toggle="tooltip" data-placement="bottom"  title='Link File' class="fas fa-link audiolink" id=${id}></i>

                </div>
                <div>
                    <p id="audio-drag">${message}</p>
                    
                    <form id="form1" enctype="multipart/form-data" action="/" runat="server">
                    <input type='file' name="userImage" accept="audio/*" style="display:none" id=${id + 1} class="audio-form" />
                    </form>
                    ${audioobj}
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
                            <i data-toggle="tooltip" data-placement="bottom"  title='Delete item' class="fas fa-trash" id=${id}></i>
                            <span  data-toggle="tooltip" data-placement="bottom"  title='Link Button'><i class="fas fa-link"  id=${id}></i></span>
                            
                            <i data-toggle="tooltip" data-placement="bottom"  title='Drag item' class="fas fa-arrows-alt" id="draghanle"></i>
                        
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
                            <i data-toggle="tooltip" data-placement="bottom"  title='Delete item' class="fas fa-trash"  class="fas fa-trash" id=${id}></i>
                            <span  data-toggle="tooltip" data-placement="bottom"  title='Link Button'><i class="fas fa-link"  id=${id}></i></span>
                            
                            <i data-toggle="tooltip" data-placement="bottom" title="Drag Item" class="fas fa-arrows-alt" id="draghanle"></i>
                        
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
                            <i data-toggle="tooltip" data-placement="bottom"  title='Delete item' class="fas fa-trash" id=${id}></i>
                            <span  data-toggle="tooltip" data-placement="bottom"  title='Link Button'><i class="fas fa-link"  id=${id}></i></span> 
                            <i data-toggle="tooltip" data-placement="bottom"  title='Drag item' class="fas fa-arrows-alt" id="draghanle"></i>
                        
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
                <i data-toggle="tooltip" data-placement="bottom"  title='Delete item' class="fas fa-trash" id=${id}></i>
                <span  data-toggle="tooltip" data-placement="bottom"  title='Upload File'><i class=" fas fa-upload" id=${id}></i></span>
                
                <span  data-toggle="tooltip" data-placement="bottom"  title='Link Button'><i  class= "fas fa-link pdflink" id=${id}></i></span> 
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
                    <i data-toggle="tooltip" data-placement="bottom"  title='Delete Button' class="fas fa-trash" id=${id}></i>
                    <span  data-toggle="tooltip" data-placement="bottom"  title='Upload File'><i class=" fas fa-upload" id=${id}></i></span>
                    
                    <span  data-toggle="tooltip" data-placement="bottom"  title='Link Button'><i  class= "fas fa-link _3dlink" id=${id}></i></span> 
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

class BaseLayout {
    constructor(top, left, height = null, width = null) {
        let position = {top, left, height, width};

        let html = `<div class="baselayout">
                    <div class="layout-actions">
                        <i title="delete-button" class="fas fa-trash" data-toggle="tooltip" data-placement="bottom"></i>
                    </div>
                    <div class="layout-icon-placement">
                        <div>    
                      
                                <span data-toggle="tooltip" data-placement="top" title="Text-box" class="layout-icons layout-text">
                                <img class="opacity-layout-icons" src = "/static/chapterPageBuilder/icons/newicon/text.svg "></img>
                                </span>
                                <span data-toggle="tooltip" data-placement="top" title="Upload Image" class="layout-icons layout-image">
                                <img  class="opacity-layout-icons" src = "/static/chapterPageBuilder/icons/picture.svg "></img>
                                </span>
                                <span data-toggle="tooltip" data-placement="top"  title="Upload Video" class="layout-icons layout-video">
                                <img class="opacity-layout-icons" src = "/static/chapterPageBuilder/icons/newicon/video.svg "></img>
                                
                                </span>

                        </div>
                        <div>

                                <span data-toggle="tooltip" data-placement="top" title="Upload Audio" class="layout-icons layout-audio">
                                <img class="opacity-layout-icons" src = "/static/chapterPageBuilder/icons/newicon/audio.png "></img>
                                </span>
                                <span data-toggle="tooltip" data-placement="top" title="Upload PDF" class="layout-icons layout-pdf">
                                <img class="opacity-layout-icons" src = "/static/chapterPageBuilder/icons/newicon/pdf.svg "></img>
                                </span>
                                <span data-toggle="tooltip" data-placement="top" title="Upload 3D-FILE" class="layout-icons layout-3d">
                                <img class="opacity-layout-icons" src = "/static/chapterPageBuilder/icons/newicon/3d-cube.svg "></img>
                                </span>

                        </div>
                      
                    </div>
               
            </div>`


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
        $('[data-toggle="tooltip"]').tooltip();
    }
}

// ====================== End of initializing elements ========================

// Element Functions
function LayoutFunction(top = null, left = null, height = "100%", width = "100%") {
    const layout = new BaseLayout(top, left, height, width);
    layout.renderDiagram();

    $('.fa-trash').click(function (e) {
        $(this).closest('.baselayout').remove();
    });
    $('.baselayout').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 75,
        minHeight: 25,
        autoHide: true,
        stop: function (e, ui) {
            //   var parent = ui.element.parent();
            h = positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            w = positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%"
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        }
    });

    $('.layout-icons').on('click', function (event) {
        event.stopPropagation();
        event.stopImmediatePropagation();
        $(this).closest('.baselayout').remove()
        if ($(this).hasClass('layout-text')) {
            TextboxFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                $(this).closest('.baselayout').css('height'), $(this).closest('.baselayout').css('width'))
        } else if ($(this).hasClass('layout-image')) {
            PictureFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                null, null, $(this).closest('.baselayout').css('width'), $(this).closest('.baselayout').css('height'))
        } else if ($(this).hasClass('layout-video')) {
            VideoFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                null, $(this).closest('.baselayout').css('height'), $(this).closest('.baselayout').css('width'))
        } else if ($(this).hasClass('layout-audio')) {
            AudioFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                null, $(this).closest('.baselayout').css('height'), $(this).closest('.baselayout').css('width'))
        } else if ($(this).hasClass('layout-pdf')) {
            PDFFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                null, $(this).closest('.baselayout').css('height'), $(this).closest('.baselayout').css('width'))
        } else if ($(this).hasClass('layout-3d')) {
            _3dFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                null, $(this).closest('.baselayout').css('height'), $(this).closest('.baselayout').css('width'))
        } else if ($(this).hasClass('layout-quiz')) {
            QuizFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                null, $(this).closest('.baselayout').css('height'), $(this).closest('.baselayout').css('width'),
                "Select Quiz", "", font_size = "75px")
        } else if ($(this).hasClass('layout-survey')) {
            SurveyFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                null, $(this).closest('.baselayout').css('height'), $(this).closest('.baselayout').css('width'),
                "Select Survey", "", font_size = "75px")
        } else if ($(this).hasClass('layout-button')) {
            ButtonFunction($(this).closest('.baselayout').css('top'), $(this).closest('.baselayout').css('left'),
                null, $(this).closest('.baselayout').css('height'), $(this).closest('.baselayout').css('width'),
                "Button", "", font_size = "75px")
        }
        $('[data-toggle="tooltip"]').tooltip()
    })
}

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

    $('.textdiv .fa-trash').click(function (e) {
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

function PictureFunction(top = null, left = null, pic = null, link = null, width = null, height = null) {
    const Pic = new picture(
        top,
        left,
        pic,
        link,
        width, height);
    Pic.renderDiagram();

    $('.pic .fa-upload').off().unbind().click(function (e) {
        trigger = parseInt(e.target.id) + 1;
        $('#' + trigger).trigger('click');
    });

    $('.pic .fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('.imagelink').off().bind("click", function (e) {
        var link_id = parseInt(e.currentTarget.id) + 1
        var div = $('#' + e.currentTarget.id).parent().parent();
        // var prevlink = $(this).parent().parent().find('background-image').replace('url(','').replace(')','').replace(/\"/gi, "");
        var prevlink = $(this).closest('.pic').find('img').attr('src')
        if (prevlink == undefined) {
            prevlink = "";
        }
        var link = prompt("Link of image", prevlink);
        if (link == null) {
            return false
        } else if (!link.startsWith('http://') && !link.startsWith('https://')) {
            link = '' + link
        }
        var ccRegExp = /\/\/(?:www\.)?(?:cincopa.com\/media-platform\/iframe.aspx\?fid=?.+)/g
        var ccRegExpForStart = /(![A-Z])\w.+/g;
        if (link.match(ccRegExp) && link.match(ccRegExpForStart)[0].length == 13) {
            PictureFunction(
                $(div)[0].style.top,
                $(div)[0].style.left,
                null,
                link,
                $(div)[0].style.width,
                $(div)[0].style.height,
            );
        } else {
            PictureFunction(
                $(div)[0].style.top,
                $(div)[0].style.left,
                link,
                null,
                $(div)[0].style.width,
                $(div)[0].style.height,
            );
        }
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
        // file = input.files[0]
        var options = {
            url: "https://media.cincopa.com/post.jpg?uid=1453562&d=AAAAcAg-tYBAAAAAAoAxx3O&hash=zrlp2vrnt51spzlhtyl3qxlglcs1ulnl&addtofid=0",
            chunk_size: 10, // MB
            onUploadComplete: function (e, options) {
                // var html = `<iframe style="width:100%;height:100%;" src="//www.cincopa.com/media-platform/iframe.aspx?fid=A8AAAoODp5Za!${options.rid}"
                //  frameborder="0" allowfullscreen scrolling="no" allow="autoplay; fullscreen"></iframe>`;
                // div.find('#loadingDiv').remove();
                // div.find('p').remove();
                // div.find('.file-upload-icon').remove();
                // // div.find('.progress').remove();
                // div.append(html);
                var request = new XMLHttpRequest()

                request.open('GET', `https://api.cincopa.com/v2/gallery.add_item.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&fid=${imagegalleryid}&rid=${options.rid}`, true)
                request.onload = function () {
                    // Begin accessing JSON data here
                    var data = JSON.parse(this.response)
                    if (request.status >= 200 && request.status < 400) {
                        console.log(data.success)
                    } else {
                        console.log('error')
                    }
                }
                request.send()
                $.get(`https://api.cincopa.com/v2/asset.set_meta.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&rid=${options.rid}&tags=${server_name},center_${centerName},course_${courseName},chapterid_${chapterID},userid_${user}`, function () {
                    console.log('success')
                }).fail(function () {
                    console.log('failed')
                })
                div.remove()
                PictureFunction(
                    $(div)[0].style.top,
                    $(div)[0].style.left,
                    null,
                    "//www.cincopa.com/media-platform/iframe.aspx?fid=A8AAAoODp5Za!" + options.rid,
                    $(div)[0].style.width,
                    $(div)[0].style.height,
                );
            },
            onUploadProgress: function (e) {
                $("#loadingDiv").attr('data-value', parseInt(e.percentComplete));
                $("#percentcomplete").html(parseInt(e.percentComplete) + '%');
                addprogress();
            },
            onUploadError: function (e) {
                console.log(e);
                $(".status-bar").html("Error accured while uploading");
            }
        };
        uploader = new cpUploadAPI(file, options);
        uploader.start();

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
                file = input.files[0]
                $(div).find('.file-upload-icon').hide()
                $(div).find('p').hide()
                $(div).find('.loadingDiv').show();
                var options = {
                    url: "https://media.cincopa.com/post.jpg?uid=1453562&d=AAAAcAg-tYBAAAAAAoAxx3O&hash=zrlp2vrnt51spzlhtyl3qxlglcs1ulnl&addtofid=0",
                    chunk_size: 10, // MB
                    onUploadComplete: function (e, options) {
                        // var html = `<iframe style="width:100%;height:100%;" src="//www.cincopa.com/media-platform/iframe.aspx?fid=A8AAAoODp5Za!${options.rid}"
                        //  frameborder="0" allowfullscreen scrolling="no" allow="autoplay; fullscreen"></iframe>`;
                        // div.find('#loadingDiv').remove();
                        // div.find('p').remove();
                        // div.find('.file-upload-icon').remove();
                        // // div.find('.progress').remove();
                        // div.append(html);
                        var request = new XMLHttpRequest()

                        request.open('GET', `https://api.cincopa.com/v2/gallery.add_item.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&fid=${imagegalleryid}&rid=${options.rid}`, true)
                        request.onload = function () {
                            // Begin accessing JSON data here
                            var data = JSON.parse(this.response)
                            if (request.status >= 200 && request.status < 400) {
                                console.log(data.success)
                            } else {
                                console.log('error')
                            }
                        }
                        request.send()
                        $.get(`https://api.cincopa.com/v2/asset.set_meta.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&rid=${options.rid}&tags=${server_name},center_${centerName},course_${courseName},chapterid_${chapterID},userid_${user}`, function () {
                            console.log('success')
                        }).fail(function () {
                            console.log('failed')
                        })
                        div.remove()
                        PictureFunction(
                            $(div)[0].style.top,
                            $(div)[0].style.left,
                            null,
                            "//www.cincopa.com/media-platform/iframe.aspx?fid=" + imagegalleryid + "!" + options.rid,
                            $(div)[0].style.width,
                            $(div)[0].style.height,
                        );
                    },
                    onUploadProgress: function (e) {
                        $(div).find('.loadingDiv').attr('data-value', parseInt(e.percentComplete));
                        $(div).find('.percentcomplete').html(parseInt(e.percentComplete) + '%');
                        addprogress();
                    },
                    onUploadError: function (e) {
                        console.log(e);
                        $(".status-bar").html("Error accured while uploading");
                    }
                };
                uploader = new cpUploadAPI(file, options);
                uploader.start();

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

    $('.btn-div .fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('.btn-div button').off().on('click', function (e) {
        e.preventDefault()
        link = $(this).closest('.btn-div').find('a')[0].href
        if (link) {
            window.open(link, '_blank');
        } else {
            $(this).closest('.btn-div').find('.fa-link').click()
        }
    });

    $('.btn-div .fa-link').bind("click", function (e) {
        var btn_id = parseInt(e.currentTarget.id) + 1

        $('#btn-form input[type=text]').val('');
        $('#btn-name').val($(this).closest('.btn-div').find('a').text().trim());
        var link = $(this).closest('.btn-div').find('a').attr('href');
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
        link = $(this).closest('.quiz-div').find('a')[0].href
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

    $('.quiz-div .fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).closest('.quiz-div').remove();
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
        $('#quiz-btn-name').val($(this).closest('.quiz-div').find('.resizable-text-only').text().trim());
        var link = $(this).closest('.quiz-div').find('a').attr('href');
        if (link != undefined) {
            link = link.replace('http://', '');
        } else {
            $('#quiz-btn-name').parent().hide()
            $('#quiz-name').parent().parent().hide()
        }
        $('#quiz-link').val(link);
        $('#quiz-name').val($(this).closest('.quiz-div').find('.quiz-name').text().trim());
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
        link = $(this).closest('.survey-div').find('a')[0].href
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

    $('.survey-div .fa-trash').click(function (e) {
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
        $('#survey-btn-name').val($(this).closest('.survey-div').find('.resizable-text-only').text().trim());
        var link = $(this).closest('.survey-div').find('a').attr('href');
        if (link != undefined) {
            link = link.replace('http://', '');
        } else {
            $('#survey-btn-name').parent().hide()
            $('#survey-name').parent().parent().hide()
        }
        $('#survey-link').val(link);
        $('#survey-name').val($(this).closest('.survey-div').find('.survey-name').text().trim());
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
    $('.pdfdiv .fa-upload').off().click(function (e) {
        trigger = parseInt(e.target.id) + 1;
        $('#' + trigger).trigger('click');
    });

    $('.pdfdiv .fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('.pdflink').off().bind("click", function (e) {
        var link_id = parseInt(e.currentTarget.id) + 1
        var div = $(this).parent().parent();
        var prevlink = $(this).parent().parent().find('iframe').attr('src');
        if (prevlink == undefined) {
            prevlink = "http://";
        }
        var link = prompt("Url", prevlink);
        if (link == null) {
            return false
        }
        PDFFunction(
            $(div)[0].style.top,
            $(div)[0].style.left,
            link,
            $(div)[0].style.height,
            $(div)[0].style.width,
        );
        div.remove()

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
    if (Videos.link && !Videos.link.includes('.com') && !Videos.link.includes('/media/chapterBuilder/')) {
        play('#video' + Videos.id)
    }

    $('.video-div .fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });
    $('.video-div .fa-upload').off().unbind().click(function (e) {
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
        div.find('p, iframe, video, .progress').remove();
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

    function readURL(input) {
        if (input.files && input.files[0]) {
            if (!input.files[0].type.match('video.*')) {
                alert('Not a valid video.')
                return
            }
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

                // If indonesian server then upload video to cincopa
                if (server_name == 'Indonesian_Server') {
                    var file = input.files[0];
                    $('#loadingDiv').show();
                    var options = {
                        url: "https://media.cincopa.com/post.jpg?uid=1453562&d=AAAAcAg-tYBAAAAAAoAxx3O&hash=zrlp2vrnt51spzlhtyl3qxlglcs1ulnl&addtofid=0",
                        chunk_size: 10, // MB
                        onUploadComplete: function (e, options) {
                            var request = new XMLHttpRequest()

                            request.open('GET', `https://api.cincopa.com/v2/gallery.add_item.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&fid=${videogalleryid}&rid=${options.rid}`, true)
                            request.onload = function () {
                                // Begin accessing JSON data here
                                var data = JSON.parse(this.response)
                                if (request.status >= 200 && request.status < 400) {
                                    console.log(data.success)
                                } else {
                                    console.log('error')
                                }
                            }
                            request.send()
                            $.get(`https://api.cincopa.com/v2/asset.set_meta.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&rid=${options.rid}&tags=${server_name},center_${centerName},course_${courseName},chapterid_${chapterID},userid_${user}`, function () {
                                console.log('success')
                            }).fail(function () {
                                console.log('failed')
                            })
                            var html = `<iframe style="width:100%;height:100%;" src="//www.cincopa.com/media-platform/iframe.aspx?fid=A4HAcLOLOO68!${options.rid}"
                             frameborder="0" allowfullscreen scrolling="no" allow="autoplay; fullscreen"></iframe>`;
                            div.find('#loadingDiv').remove();
                            div.find('p').remove();
                            // div.find('.progress').remove();
                            div.append(html);
                        },
                        onUploadProgress: function (e) {
                            $("#loadingDiv").attr('data-value', parseInt(e.percentComplete));
                            $("#percentcomplete").html(parseInt(e.percentComplete) + '%');
                            addprogress();
                        },
                        onUploadError: function (e) {
                            console.log(e);
                            $(".status-bar").html("Error accured while uploading");
                        }
                    };
                    uploader = new cpUploadAPI(file, options);
                    uploader.start();

                    // else upload to vimeo
                } else {
                    $.ajax({
                        url: save_video_url,
                        data: data,
                        beforeSend: function (request) {
                            request.setRequestHeader("Connection", 'keep-alive');
                        },
                        maxChunkSize: 10000000,
                        contentType: false,
                        processData: false,
                        method: 'POST',
                        type: 'POST',
                        beforeSend: function () {
                            div.append(`<div class="loader" id="loadingDiv"></div>
                        <p id = "percentcomplete"></p>
                        `)
                            $('#loadingDiv').show();
                            div.find('.file-upload-icon').css('display', 'none');
                        },
                        error: function (errorThrown) {
                            if (errorThrown.responseText.message)
                                alert("Failed to upload Video." + errorThrown.responseText.message)
                            else
                                alert('Failed to Upload. ' + errorThrown.status)
                            div.find('#loadingDiv').remove();
                            div.find('#percentcomplete').remove();
                            div.find('.file-upload-icon').css('display', 'block');
                        },
                        success: function (data) {
                            console.log(data)
                            div.find('#loadingDiv').remove();
                            div.find('#percentcomplete').remove();
                            div.find('p').remove();
                            div.find('.file-upload-icon').remove();
                            div.find('.progress').remove();
                            if (data.hasOwnProperty('html')) {
                                var html = $(data.html);
                                $(html).css('height', '100%')
                                $(html).css('width', '100%')

                                div.append(html);
                            } else {
                                VideoFunction(
                                    $(div)[0].style.top,
                                    $(div)[0].style.left,
                                    data.media_name,
                                    $(div)[0].style.height,
                                    $(div)[0].style.width,
                                );
                                div.remove();
                            }
                        },
                        xhr: function () {
                            var xhr = new window.XMLHttpRequest();

                            xhr.upload.addEventListener("progress", function (evt) {
                                $('#progress-bar').css("display", "block");
                                $('#loadingDiv').show();

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
                }

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

function AudioFunction(top = null, left = null, link = null, height = null, width = null) {
    const Audios = new Audio(top, left, link, height, width);
    Audios.renderDiagram();
    if (Audios.link && !Audios.link.includes('.com') && !Audios.link.includes('/media/chapterBuilder/')) {
        play('#audio' + Audios.id)
    }

    $('.audio-div .fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });
    $('.audio-div .fa-upload').off().unbind().click(function (e) {
        trigger = parseInt(e.target.id) + 1;
        $('#' + trigger).trigger('click');
    });
    $('.audiolink').off().bind("click", function (e) {
        var link_id = parseInt(e.currentTarget.id) + 1
        var div = $(this).parent().parent();
        var prevlink = $(this).parent().parent().find('iframe').attr('src');
        if (prevlink == undefined) {
            prevlink = "http://";
        }
        var link = prompt("Url", prevlink);
        if (link == null) {
            return false
        } else if (!link.startsWith('http://') && !link.startsWith('https://')) {
            link = 'http://' + link
        }
        var ccRegExp = /\/\/(?:www\.)?(?:cincopa.com\/media-platform\/iframe.aspx\?fid=?.+)/g
        var ccRegExpForStart = /(![A-Z])\w.+/g;
        if (link.match(ccRegExp) && link.match(ccRegExpForStart)[0].length == 13) {
            AudioFunction(
                $(div)[0].style.top,
                $(div)[0].style.left,
                link,
                $(div)[0].style.height,
                $(div)[0].style.width,
            );
            div.remove()
        } else {
            alert("Link is not Valid")
        }
    });

    $('.audio').on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
    })

    $('.audio-div').resizable({
        containment: $('#tabs-for-download'),
        grid: [20, 20],
        autoHide: true,
        minWidth: 150,
        minHeight: 50,
        stop: function (e, ui) {
            // var parent = ui.element.parent();
            ui.element.css({
                width: positionConvert(ui.element.width(), $('#tabs-for-download').width()) + "%",
                height: positionConvert(ui.element.height(), $('#tabs-for-download').height()) + "%"
            });
        },
    });

    function readURL(input) {
        if (input.files && input.files[0]) {
            if (!input.files[0].type.match('audio.*')) {
                alert('Not a valid audio.')
                return
            }
            var reader = new FileReader();
            reader.onload = function (e) {
                let div = $(input).parent().parent().parent();
                div.find('auido').remove();
                var data = new FormData();
                $.each(input.files, function (i, file) {
                    data.append('file-' + i, file);
                });
                data.append('csrfmiddlewaretoken', csrf_token);
                data.append('chapterID', chapterID);
                data.append('courseID', courseID);
                data.append('type', 'audio');

                var file = input.files[0];
                $('#loadingDiv').show();
                var options = {
                    url: "https://media.cincopa.com/post.jpg?uid=1453562&d=AAAAcAg-tYBAAAAAAoAxx3O&hash=zrlp2vrnt51spzlhtyl3qxlglcs1ulnl&addtofid=0",
                    chunk_size: 10, // MB
                    onUploadComplete: function (e, options) {
                        var request = new XMLHttpRequest()

                        request.open('GET', `https://api.cincopa.com/v2/gallery.add_item.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&fid=${audiogalleryid}&rid=${options.rid}`, true)
                        request.onload = function () {
                            // Begin accessing JSON data here
                            var data = JSON.parse(this.response)
                            if (request.status >= 200 && request.status < 400) {
                                console.log(data.success)
                            } else {
                                console.log('error')
                            }
                        }
                        request.send()
                        $.get(`https://api.cincopa.com/v2/asset.set_meta.json?api_token=1453562iobwp33x0qrt34ip4bjiynb5olte&rid=${options.rid}&tags=${server_name},center_${centerName},course_${courseName},chapterid_${chapterID},userid_${user}`, function () {
                            console.log('success')
                        }).fail(function () {
                            console.log('failed')
                        })
                        var html = `<iframe style="width:100%;height:100%;" src="//www.cincopa.com/media-platform/iframe.aspx?fid=AgLA8o--2Nr0!${options.rid}"
                         frameborder="0" allowfullscreen scrolling="no" allow="autoplay; fullscreen"></iframe>`;
                        div.find('#loadingDiv').remove();
                        div.find('p').remove();
                        // div.find('.progress').remove();
                        div.append(html);
                    },
                    onUploadProgress: function (e) {
                        $("#loadingDiv").attr('data-value', parseInt(e.percentComplete));
                        $("#percentcomplete").html(parseInt(e.percentComplete) + '%');
                        addprogress();
                    },
                    onUploadError: function (e) {
                        console.log(e);
                        $(".status-bar").html("Error accured while uploading");
                    }
                };
                uploader = new cpUploadAPI(file, options);
                uploader.start();

                $('#audio-drag').css({
                    'display': 'none'
                });

            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $(".audio-form").off().change(function (e) {
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

    $('._3dobj-div .fa-trash').click(function (e) {
        $('#' + e.currentTarget.id).parent().parent().remove();
    });

    $('._3dlink').off().bind("click", function (e) {
        var link_id = parseInt(e.currentTarget.id) + 1
        var div = $(this).parent().parent();
        var prevlink = $(this).parent().parent().find('iframe').attr('src');
        if (prevlink == undefined) {
            prevlink = "http://";
        }
        var link = prompt("Url", prevlink);
        if (link == null) {
            return false
        }
        _3dFunction(
            $(div)[0].style.top,
            $(div)[0].style.left,
            link,
            $(div)[0].style.height,
            $(div)[0].style.width,
        );
        div.remove()

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

    $('._3dobj').on('dragover', function (e) {
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
                _3dFunction(
                    $(div)[0].style.top,
                    $(div)[0].style.left,
                    '/media/chapterBuilder/' + courseID + '/' + chapterID + '/' + data.objname,
                    $(div)[0].style.height,
                    $(div)[0].style.width,
                );
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

    // background color for pages
    $('#tabs-for-download').click(function () {
        setThumbnailok = true
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
        if (btn_link != "" && !btn_link.includes("http")) {
            $('#' + btn_id).attr({
                "href": `http://${btn_link}`
            });
        } else if (btn_link.includes("http")) {
            $('#' + btn_id).attr({
                "href": `${btn_link}`
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
        if ($('#quiz-btn-name').val() == 'Select Quiz' && quiz_link != "") {
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
        if (tempVarStorage) {
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

        if ($('#survey-btn-name').val() == 'Select Survey' && survey_link != "") {
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
        if (tempVarStorage) {
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

    $('#quiz_create_link').click(function (e) {
        $('#iframeholder iframe').on('load', function () {
            var iframe = $('#iframeholder iframe').contents();
            $('#iframeholder iframe').contents().find("#quiz_form_ajax").on('click', '#quiz_submit_button', function () {
                setTimeout(() => {
                    modalcloseFunction()
                }, 1000)
            });
        });
    })

    $('#survey_create_link').click(function (e) {
        $('#iframeholder iframe').on('load', function () {
            var iframe = $('#iframeholder iframe').contents();
            $('#iframeholder iframe').contents().find("#survey_form_ajax").on('click', '#survey_submit_button', function () {
                setTimeout(() => {
                    modalcloseFunction()
                }, 1000)
            });
        });
    })
});

function modalcloseFunction() {
    $('#closeiframebtn').click();
    tempVarStorage.click()
}

let sidebarWidth = $(".sidebar").width(); // get width of sidebar
let toolbarheight = $('.editor-toolbar').height();


function clearPage(page_number) {
    $('#tab').empty();
    if (page_number in data.pages) {
        data.pages[page_number] = ''
    }
}

function dropfunction(event, ui) {
    let top = ui.helper.position().top - $('.ols-objects').height() - $('.component-container').height();
    let left = ui.helper.position().left;

    $(this).removeClass("over");
    if (ui.helper.offset().top < $('#tab').offset().top) {
        top = $('#tab').position().top
    }

    // if (ui.helper.offset().top + (0.25 * $('#tab').height()) > $('#tab').height()) {
    //     top = $('#tab').height() - (0.25 * $('#tab').height())
    // }

    if (ui.helper.offset().left + (0.20 * $('#tab').width()) > $('#tab').width() && !ui.helper.hasClass('button')) {   // 0.25 is multiplied to sum the height of element to the current pointer position
        left = $('#tab').width() - (0.40 * $('#tab').width()) + sidebarWidth
    } else if (ui.helper.offset().left > $('#tab').width() && ui.helper.hasClass('button')) {
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
            null, null, '40%', '30%'
        );
    } else if (ui.helper.hasClass('video')) {
        VideoFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            null, '30%', '40%'
        );
    } else if (ui.helper.hasClass('audio')) {
        AudioFunction(
            (positionConvert(top, $('#tabs-for-download').height())) + '%',
            (positionConvert((left - sidebarWidth), $('#tabs-for-download').width())) + '%',
            null, '15%', '40%'
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
        LayoutFunction(
            top = 0 + '%',
            left = 0 + '%',
            height = "50%", width = "100%");
        LayoutFunction(
            top = 50 + '%',
            left = 0 + '%',
            height = "50%", width = "100%");
    } else if (ui.helper.hasClass('grid')) {
        clearPage(window.currentPage)
        LayoutFunction(
            top = 0 + '%',
            left = 0 + '%',
            height = "50%", width = "100%");


        // ===============for textbox inside grid-1============
        LayoutFunction(
            top = "52%",
            left = 0 + '%',
            height = "45%", width = "100%"
        );
    } else if (ui.helper.hasClass('title-slide')) {
        clearPage(window.currentPage)
        LayoutFunction(
            top = 0 + '%',
            left = 0 + '%',
            height = "60%", width = "49%");
        LayoutFunction(
            top = 0 + '%',
            left = "51%",
            height = "60%", width = "49%");
        LayoutFunction(
            top = "62%",
            left = 0 + '%',
            height = "35%", width = "100%",
        );
    } else if (ui.helper.hasClass('title-content-details')) {
        clearPage(window.currentPage)
        LayoutFunction(
            top = "0%",
            left = 0 + '%',
            height = "10%", width = "100%",
        );
        LayoutFunction(
            top = "13%",
            left = 0 + '%',
            height = "84%", width = "100%",
        );
    } else if (ui.helper.hasClass('pdf-text')) {
        clearPage(window.currentPage)
        LayoutFunction(
            top = "0%",
            left = 0 + '%',
            height = "60%", width = "100%");


        // ===============for textbox inside grid-1============
        LayoutFunction(
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

    $('[data-toggle="tooltip"]').tooltip();
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
                    <li class="small-canvases pagenumber" data-before="${key}" style="position: relative;"
                        onclick="changePage('tab${key}')" value="${key}">
                        <div class="mini-canvas-btns" style="position:absolute; top:0px;left:0;right:0; ">
                            
                            <span style="float:right">
                                <button class="clone-button clone-page-btn" value="${key}">
                                <span data-title="Clone Page">
                                <i class="fa fa-clone " aria-hidden="true"></i>
                                </span>
                                
                                </button>
                            </span>
        
                            <span style="float:right">
                                <button class="delete-button delete-page-btn" value="${key}">
                                <span data-title="Delete Page">
                                <i class="fa fa-times " aria-hidden="true"></i>
                                </span>
        
                               
                                </button>
                            </span>
                        </div>
        
                    </li> 
                    
            `);
            } else {
                $(".tabs-to-click ul").append(`
                    <li class="small-canvases pagenumber" data-before="${key}" style="
                    position: relative;
                    background-image: url('${value[0]['thumbnail']}'); 
                    background-position: center;
                    background-size: contain;
                    background-repeat: no-repeat;
                    "
                        onclick="changePage('tab${key}')" value="${key}">
                        <div class="mini-canvas-btns" style="position:absolute; top:0px;left:0;right:0; ">
                            
                            <span style="float:right">
                                <button class="clone-button clone-page-btn" value="${key}">
                                <span data-title="Clone Page">
                                <i class="fa fa-clone " aria-hidden="true"></i>
                                </span>
                                
                                </button>
                            </span>
        
                            <span style="float:right">
                                <button class="delete-button delete-page-btn" value="${key}">
                                <span data-title="Delete Page">
                                <i class="fa fa-times " aria-hidden="true"></i>
                                </span>
        
                               
                                </button>
                            </span>
                        </div>
        
                    </li> 
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
    $('.small-canvases::before').css('content', num_tabs)
    $(".tabs-to-click ul").append(`
            <li class="small-canvases pagenumber current" data-before="${num_tabs}" style="position: relative;"
                onclick="changePage('tab${num_tabs}')" value="${num_tabs}">
                <div class="mini-canvas-btns" style="position:absolute; top:0px;left:0;right:0; ">
                    
                    <span style="float:right">
                        <button class="clone-button clone-page-btn" value="${num_tabs}">
                        <span data-title="Clone Page">
                        <i class="fa fa-clone " aria-hidden="true"></i>
                        </span>
                        
                        </button>
                    </span>

                    <span style="float:right">
                        <button class="delete-button delete-page-btn" value="${num_tabs}">
                        <span data-title="Delete Page">
                        <i class="fa fa-times " aria-hidden="true"></i>
                        </span>

                       
                        </button>
                    </span>
                </div>

            </li>
    `)

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
    const additionalCanvas = document.querySelector('.additional-canvas');
    additionalCanvas.scrollTop = additionalCanvas.scrollHeight;

}

function displaypagenumbers() {
    $('.pagenumber').each(function (key, value) {
        $(this).attr('data-before', key + 1);
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
                                    css_value.link,
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
                        if (div == 'audio') {
                            $.each(div_value, function (css, css_value) {
                                css_string = JSON.stringify(css_value)
                                let link;
                                if (css_value.hasOwnProperty('online_link') && css_value.online_link) {
                                    link = css_value.online_link
                                } else {
                                    link = css_value.local_link
                                }
                                AudioFunction(
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
    var audio = [];
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
                    'background-image': $(this).find("img").attr('src'),
                    'link': $(this).find("iframe").attr('src')
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
            local_link = $(this).find('video').attr('data-cld-public-id');

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
        if (value.classList.contains('audio-div')) {
            online_link = $(this).find('iframe').attr('src');
            local_link = $(this).find('audio').attr('data-cld-public-id');

            audio.push(
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
            'audio': audio,
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
            'audio': audio,
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
            pickr.setColor(data.pages[currentPage][0].backgroundcolor)
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
        if (data.pages[currentPage]) {
            pickr.setColor(data.pages[currentPage][0].backgroundcolor)
        } else {
        }
    }
    // localStorage.setItem(`chapter_${chapterID}_currentPage`, window.currentPage);
}

$('#tab').on('click', '.file-upload-icon', function () {
    $(this).closest('.ui-draggable').find('.fa-upload').click();
})

// Media File deletion
function deleteFile(tobedeletedfiles = tobedeletedfiles, filetype = 0) {
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
            if (filetype == 4 || filetype == 5) {
                retrieveServerMedias(10)
            } else if (filetype == 2 && server_name != "Indonesian_Server") {
                retrieveServerMedias(10)
            } else {
                retrieveMedias(filetype)
            }
        },
    });
}

// delete page function
$('.tabs-to-click').on('click', '.delete-page-btn', function () {
    var confirmation = confirm("Are you sure you want to delete?")
    if (confirmation == false) {
        return false
    }

    if ($(this).closest('li')[0].classList.contains('current')) {
        setThumbnailok = false
        if ($(this).closest('li').prev().length != 0)
            $(this).closest('li').prev()[0].click();
        else if ($(this).closest('li').next().length != 0)
            $(this).closest('li').next()[0].click()
        else {
            alert("cannot delete only page");
            return false
        }
    }
    $(this).closest('.pagenumber').remove();
    delete data.pages[this.value]

    numberofloops = Object.keys(data.pages).length + 1
    for (x = this.value; x <= numberofloops; x++) {
        $('.pagenumber[value="' + (parseInt(x) + 1) + '"').find('.clone-page-btn').attr({
            "value": parseInt(x),
        });
        $('.pagenumber[value="' + (parseInt(x) + 1) + '"').find('.delete-page-btn').attr({
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
    $(this).attr('disabled', true)  // clone button disabled for preventing multiple clicks
    var promise = new Promise((resolve, reject) => {
        updateData(window.currentPage, prev_data)
        resolve('success')
    })
    source = this.value
    destination = parseInt(source) + 1
    // numberofloops = Object.keys(data.pages).length

    // Loop through all side navigation slides and update value of clone, delete and onchange button.
    $.each($('.pagenumber'), function () {
        if (this.value > parseInt(source)) {
            let new_value = parseInt(this.value) + 1
            $(this).attr({
                "value": new_value,
                "onclick": "changePage('tab" + new_value + "')"
            });
            $(this).find('.clone-page-btn').attr({
                "value": new_value,
            });
            $(this).find('.delete-page-btn').attr({
                "value": new_value,
            });
        }
    });

    numberofloops = Object.keys(data.pages).length  // number of pages before cloning in json.

    promise.then((successmessage) => {
        setTimeout(() => {
            // window.currentPage = 'tab'+(parseInt(window.currentPage) + 1)
            for (x = numberofloops; x >= (parseInt(source) + 1); x--) {
                // swap index of data['pages']
                // For instance => data['pages']['10'] will be swapped to data['pages']['11']
                data.pages[parseInt(x) + 1] = data.pages[x]
                // delete data.pages[parseInt(x)]
            }
            data.pages[destination] = data.pages[source]
            // $('.current.pagenumber').removeClass('current')
            var num_tabs = parseInt(source) + 1;
            let copy = $(this).closest('li').clone();
            // for cloning page navigation tabs
            copy.removeClass('current')
            copy.find('.clone-page-btn').val(num_tabs);
            copy.find('.clone-page-btn').attr('disabled', false)
            copy.find('.delete-page-btn').val(num_tabs);
            console.log(copy)
            copy.val(num_tabs);
            copy.attr('onclick', 'changePage("tab' + num_tabs + '")');
            $(this).closest('li').after(copy);
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
    // $('#tab').find('.video-div').each(function () {
    //     $(this).css({
    //         'background-image': `url('${video_icon}')`,
    //         'background-position': 'center',
    //         'background-size': 'contain',
    //         'background-repeat': 'no-repeat'
    //     })
    // });
    $('#tab').find('.audio-div').each(function () {
        $(this).css({
            'background-image': `url('${audio_icon}')`,
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
    });

    html2canvas($('#tab')[0], {logging: true, letterRendering: 1, allowTaint: false, useCORS: true}).then(canvas => {
        $('.pagenumber[value= ' + prev_page + ']').each(function () {
            if (canvas.toDataURL('image/png', 0.00,).startsWith('data:image')) {
                resizeImage(canvas.toDataURL('image/png', 0.00), 120, 60, setThumbnailscallback, $(this));
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

$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()

        $("#sortable-slides").sortable({
            // axis: "y",   // only moves in top/bottom direction
            cursor: "move", // icon to display while sorting
            start: function (event, ui) {
                $(ui.item).css("opacity", "0.6");
            },
            stop: function (event, ui) {
                $(ui.item).css("opacity", "1.0");
            },
            change: function (event, ui) {
                ui.placeholder.css({visibility: 'visible', border: '1px dashed orange'});
            },
            update: function (event, ui) {  //  After Sort
                //  Empty array to store the sorted order of slides.
                //  Example:
                //  Before sorting. Pages: 1, 2, 3, 4
                // After Sort. Pages: 3, 1, 2, 4
                let new_keys = [];
                displaypagenumbers();   //  change pagenumbers after sorting ends
                $.each($(this).find('li'), function (index) {
                    new_value = parseInt(index) + 1;    //  Array index starts from 0. Page number from 1 so increment +1
                    new_keys.push($(this)[0].value);    //  Push sorted page numbers in array in order.
                    //  Change value of slides.
                    $(this).attr({
                        "value": new_value,
                        "onclick": "changePage('tab" + new_value + "')"
                    });
                    $(this).find('.clone-page-btn').attr({
                        "value": new_value,
                    });
                    $(this).find('.delete-page-btn').attr({
                        "value": new_value,
                    });
                });

                temp = data.pages;  //  Store page data in temporary variable
                data.pages = {};    //  Empty all data

                //  change all keys of data in sorted order
                for (let i = 0; i < Object.keys(temp).length; i++) {    //  Loop through the number of pages
                    /*
                        Example:
                        new_keys = [3, 1, 2, 4]
                        data['pages'][1] = temp[3]
                        Stores content of page 3 in page 1.
                     */
                    data.pages[i + 1] = temp[new_keys[i]]
                }

                //  Change currentPage variable.
                window.currentPage = $('.pagenumber.current')[0].value.toString()
            }
        });
        $("#sortable-slides").disableSelection();
    })

    //  Check If the clicked element is slide 'li'.
    // If clicked target is delete/clone button, then do not change slides.
    $('.tabs-to-click li[onclick]').each(function () {
        $(this).data('onclick', this.onclick);

        this.onclick = function (event) {
            if (!event.target.classList.contains('pagenumber')) {
                return false;
            }

            $(this).data('onclick').call(this, event || window.event);
        };
    });
});

