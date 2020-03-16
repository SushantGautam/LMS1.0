//This is the service worker with the Advanced caching

const CACHE = "pwabuilder-adv-cache";
const precacheFiles = [
    /* Add an array of files to precache for your app */
    '/offline.html', '/static/images/logo_orange.png',
    // '/',
    // '/profile',
    // '/quiz',
    // '/survey/surveyinfo',
    // '/forum',
    // '/memberinfo',
    // '/courseinfo',
    // '/inninginfo',
    // '/groupmapping',
    // '/inninggroup',
    // '/students/',
    // '/students/calendar',
    // '/students/courseinfo/mycourses',
    // '/students/myassignments',
    // '/students/quiz/progress',
    // '/students/forum',
    // '/students/questions_student/',
    // '/students/profile',
    // '/teachers/',
    // '/teachers/courseinfo/mycourses',
    // '/teachers/myassignments/',
    // '/teachers/quiz/',
    // '/teachers/forum/',
    // '/teachers/question_teachers/',
    // '/teachers/profile',


];

// TODO: replace the following with the correct offline fallback page i.e.: const offlineFallbackPage = "offline.html";
const offlineFallbackPage = "offline.html";

// const networkFirstPaths = [
//     /* Add an array of regex of paths that should go network first */
//     // Example: /\/api\/.*/
//     /\/students*/,
//     /\/teachers*/,
//     /\/quiz*/,
//     /\/survey*/,
//     /\/forum*/,
//     /\/memberinfo*/,
//     /\/inninginfo*/,
//     /\/groupmapping*/,
//     /\/inninggroup*/,
//     /\/Achievement*/,
//     /\//,
// ];

const avoidCachingPaths = [
    /* Add an array of regex of paths that shouldn't be cached */
    // Example: /\/api\/.*/
    /\/login*/,
    /\/logout*/,
    /\/admin*/,
    /\/register*/,
    /\/collect*/,
    /\/gtag*/,
    /\/analytics*/,
    /\/students\/questions_student_detail\/detail*/,

];

function pathComparer(requestUrl, pathRegEx) {
    return requestUrl.match(new RegExp(pathRegEx));
}

function comparePaths(requestUrl, pathsArray) {
    if (requestUrl) {
        for (let index = 0; index < pathsArray.length; index++) {
            const pathRegEx = pathsArray[index];
            if (pathComparer(requestUrl, pathRegEx)) {
                return true;
            }
        }
    }

    return false;
}

self.addEventListener("install", function (event) {
    console.log("[PWA Builder] Install Event processing");

    console.log("[PWA Builder] Skip waiting on install");
    self.skipWaiting();

    event.waitUntil(
        caches.open(CACHE).then(function (cache) {
            console.log("[PWA Builder] Caching pages during install");

            return cache.addAll(precacheFiles).then(function () {
                return cache.add(offlineFallbackPage);
            });
        })
    );
});

// Allow sw to control of current page
self.addEventListener("activate", function (event) {
    console.log("[PWA Builder] Claiming clients for current page");
    event.waitUntil(self.clients.claim());
});

// If any fetch fails, it will look for the request in the cache and serve it from there first
self.addEventListener("fetch", function (event) {
    if (event.request.method !== "GET") return;

    if (comparePaths(event.request.url, networkFirstPaths)) {
        if (event.request.url.includes("media") || event.request.url.includes("static")) {
            // console.log('contains media ' + event.request.url);
            TryfromCache(event.request);
            // console.log('Going for cacheFirstFetch ' + event.request.url);
            return networkFirstFetch(event);
        }
        // console.log('Going for networkFirstFetch ' + event.request.url);
        networkFirstFetch(event);
    } else {
        // console.log('Going for cacheFirstFetch ' + event.request.url);

        cacheFirstFetch(event);
    }
});

function cacheFirstFetch(event) {
    event.respondWith(
        fromCache(event.request).then(
            function (response) {
                // The response was found in the cache so we responde with it and update the entry

                // This is where we call the server to get the newest version of the
                // file to use the next time we show view
                event.waitUntil(
                    fetch(event.request).then(function (response) {
                        return updateCache(event.request, response);
                    })
                );

                return response;
            },
            function () {
                // The response was not found in the cache so we look for it on the server
                return fetch(event.request)
                    .then(function (response) {
                        // If request was success, add or update it in the cache
                        event.waitUntil(updateCache(event.request, response.clone()));

                        return response;
                    })
                    .catch(function (error) {
                        // The following validates that the request was for a navigation to a new document
                        if (event.request.destination !== "document" || event.request.mode !== "navigate") {
                            return;
                        }

                        console.log("[PWA Builder] Network request failed and no cache. Opening from offline page" + error);
                        // Use the precached offline page as fallback
                        return caches.open(CACHE).then(function (cache) {
                            cache.match(offlineFallbackPage);
                        });
                    });
            }
        )
    );
}

function networkFirstFetch(event) {
    event.respondWith(
        fetch(event.request)
            .then(function (response) {
                // If request was success, add or update it in the cache
                event.waitUntil(updateCache(event.request, response.clone()));
                return response;
            })
            .catch(function (error) {
                console.log("[PWA Builder] Network request Failed. Serving content from cache: " + error);
                return fromCache(event.request);
            })
    );
}

function fromCache(request) {
    // Check to see if you have it in the cache
    // Return response
    // If not in the cache, then return error page
    return caches.open(CACHE).then(function (cache) {
        return cache.match(request).then(function (matching) {
            if (!matching || matching.status === 404) {
                console.log("Opening Error Page")

                // return cache.match(offlineFallbackPage);
                if (request.destination !== "document" || request.mode !== "navigate") {
                    return Promise.reject("no-match");
                } else return caches.open(CACHE).then(function (cache) {
                    return cache.match(offlineFallbackPage);
                });


            }

            return matching;
        });
    });
}


function TryfromCache(request) {
    // Check to see if you have it in the cache
    // Return response
    // If not in the cache, then return error page
    return caches.open(CACHE).then(function (cache) {
        return cache.match(request).then(function (matching) {
            if (!matching || matching.status === 404) {
                // console.log('Try from cache couldnt find ' + request.url);

                return Promise.reject("no-match");
            }

            return matching;
        });
    });
}


function updateCache(request, response) {
    if (!comparePaths(request.url, avoidCachingPaths)) {
        return caches.open(CACHE).then(function (cache) {
            return cache.put(request, response);
        });
    }

    return Promise.resolve();
}


