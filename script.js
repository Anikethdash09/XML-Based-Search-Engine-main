const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-terms');
const searchResponse = document.getElementById('search-response');
const searchTypeAnd = document.getElementById('search-type-and');
const searchTypeOr = document.getElementById('search-type-or');

searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const query = searchInput.value;
  const searchType = searchTypeAnd.checked ? 'AND' : 'OR'; // Get the selected search type
  fetchSearchResults(query, searchType); // Pass the search type to the function
});

// Add an event listener to the radio buttons to update the search type
searchTypeAnd.addEventListener('change', () => {
  searchTypeOr.checked = false;
});

searchTypeOr.addEventListener('change', () => {
  searchTypeAnd.checked = false;
});

function fetchSearchResults(query, searchType) {
  searchResponse.innerHTML = '';
  fetch('http://127.0.0.1:5000/search', {
    method: 'POST',
    contentType: "application/json",
    body: new URLSearchParams({
      'query': query,
      'search_type': searchType // Include the selected search type in the request body
    })
  })
    .then((response) => {
        console.log(response);
      if (response.ok) {
        response.json().then((data) => {
          if (data.results.length === 0) {
            searchResponse.innerHTML = 'No results found';
          } else {
            const resultList = document.createElement('ul');
            for (let i = 0; i < data.results.length; i++) {
              const resultItem = document.createElement('li');
             resultItem.innerHTML = `
                    <a href="${data.results[i].url}" target="_blank">${data.results[i].title}</a>
                    <p>${data.results[i].url}</p>
                  `;
              resultList.appendChild(resultItem);
            }
            searchResponse.appendChild(resultList);
          }
        });
      } else {
        searchResponse.innerHTML = 'Error: ' + response.status + ' ' + response.statusText;
      }
    })
    .catch((error) => {
      searchResponse.innerHTML = 'Error: ' + error.message;
    });
}