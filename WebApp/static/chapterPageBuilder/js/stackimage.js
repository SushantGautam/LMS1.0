$(document).ready(function(){

        // Index of current image which is on display 
        let imageIndex = 0; 

        // Object array of all the images of class stack 
        let images = document.getElementsByClassName('stack'); 

        // Detect mouse is over image
        let isMouseOverImage = false; 

        // Object of parent element containing all images 
        let scrollImages = document.getElementById('scroll-image');

        // current scoll co-ordinates
        let x, y; 

        // This function sets the scroll to x, y 
        function noScroll() { 
            window.scrollTo(x, y); 
        } 

        // The following event id fired once when mouse hover over the images 
        scrollImages.addEventListener( "mouseenter", function() { 
            // store the current page offset to x,y 
            x = window.pageXOffset; 
            y = window.pageYOffset; 
            window.addEventListener("scroll", noScroll); 
            isMouseOverImage = true; 
        }); 

        // when mouse is no longer over the images 
        scrollImages.addEventListener( "mouseleave", function() { 
            isMouseOverImage = false; 
            window.removeEventListener( "scroll", noScroll); 
        }); 

        // when mouse wheel over the images 
        scrollImages.addEventListener( 
                    "wheel", function(e) { 
                            
            // check if over image or not 
            if (isMouseOverImage) { 
                let nextImageIndex = 0; 

                // finds the next image index limit scroll between first and last image
                if (e.deltaY > 0) {
                    nextImageIndex = imageIndex + 1;
                    if(nextImageIndex >= images.length) nextImageIndex = imageIndex
                } else {
                    nextImageIndex = imageIndex - 1;
                    if(nextImageIndex < 0) nextImageIndex = 0
                }

                // set the z index of current image to 0
                images[imageIndex].style.zIndex = "0"; 
                    
                // set z index of next image to 1, to appear on top of old image 
                images[nextImageIndex].style.zIndex = "1"; 
                imageIndex = nextImageIndex; 

                document.getElementById("progressbar").setAttribute("style", "height:" + (imageIndex + 1) * 100 / images.length + "%");

            } 
        }); 
});