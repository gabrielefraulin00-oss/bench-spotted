
const CACHE_NAME = "bench-spotted-v2";

const FILES_TO_CACHE = [
    "/",
    "/static/manifest.json"
];


self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE_NAME)
        .then(cache => {
            return cache.addAll(FILES_TO_CACHE);
        })

    );

});


self.addEventListener("activate", event => {

    event.waitUntil(

        caches.keys().then(keyList => {
            return Promise.all(
                keyList.map(key => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        })

    );

});


self.addEventListener("fetch", event => {

    // Only intercept GET requests — POST/PUT/DELETE etc. go straight to network
    if (event.request.method !== "GET") {
        return;
    }

    event.respondWith(

        caches.match(event.request)
        .then(response => {

            return response || fetch(event.request);

        })

    );

});