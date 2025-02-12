function searchImages(filenameSearch, textSearch) {
    let url = '/images';

    let searchInfo = document.getElementById('search_info');
    let searchResult = document.getElementById('search_result');
    let searchResultHTMLCode = '';

    if (filenameSearch || textSearch) {
        url += '?';
        if (filenameSearch) {
            url += `filename=${filenameSearch}`;
        }
        if (textSearch) {
            if (filenameSearch) {
                url += '&'; // Add & if both parameters are present
            }
            url += `text=${textSearch}`;
        }
    }

    fetch(url)
        .then(response => response.json())
        .then(images => {
            // ... display the images (using filename and text) ...
            console.log(images);

            images.forEach(element => {
                searchResultHTMLCode += `<div class="card"><div class="card-image"><figure class="image is-4by3"><img src="screenshots/${encodeURI(element['filename'])}" alt="Screenshot image"></figure></div><div class="card-content"><div class="media"><div class="media-content"><p class="title is-6">Filename: ${element['filename']}</p><p class="subtitle is-6">ID: ${element['id']}</p></div></div></div><footer class="card-footer"><a href="screenshots/${encodeURI(element['filename'])}" class="card-footer-item" target="_blank">Mostra</a></footer></div>`;
            });

            searchInfo.innerHTML = `<div class="notification is-info">Risultati per la ricerca della stringa "${textSearch}"</div>`;
            searchResult.innerHTML = searchResultHTMLCode;
        })
        .catch(error => {
            console.error('Error fetching images:', error);

            searchInfo.innerHTML = `<div class="notification is-danger">ERRORE! ${error}</div>`;
        });
}


// const filenameInput = document.getElementById('filenameInput');
const textInput = document.getElementById('textInput');
const searchButton = document.getElementById('searchButton');
const clearButton = document.getElementById('clearButton');

searchButton.addEventListener('click', (event) => {
    event.preventDefault()
    // const filenameSearch = filenameInput.value;
    const filenameSearch = '';
    const textSearch = textInput.value;
    searchImages(filenameSearch, textSearch);
    
});

clearButton.addEventListener('click', (event) => {
    event.preventDefault()
    
    textInput.value = '';

    let searchInfo = document.getElementById('search_info');
    let searchResult = document.getElementById('search_result');
    searchInfo.innerHTML = '';
    searchResult.innerHTML = '';

    console.clear();
});

// Initial load (all images):
// searchImages(); // No search terms initially