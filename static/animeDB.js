"use strict";

const $showList = $("#shows-list");

const $searchForm = $("#search-form");

const $animeImage = $("#anime-image");

const api = "https://kitsu.io/api/edge/anime?filter[text]=";

async function getShowsByTerm(term) {
  //gets result object from api
  const response = await axios.get(
    `https://kitsu.io/api/edge/anime?filter[text]=${term}`
  );
  $showList.empty();
  for (let anime of response.data.data) {
    populateShows(anime);
  }
}

async function getShowByID(term) {
  const response = await axios.get();
}
/** Given list of shows, create markup for each and to DOM */

function populateShows(shows) {
  // const $showsList = $("#shows-list");
  const $show = $(
    `<div id="animeID" data-show-id="${shows.id}" class="Show col-md-12 col-lg-6 mb-4">
         <div class="media">
         <img src="${shows.attributes.coverImage.tiny}" alt="${shows.attributes.canonicalTitle}">
          <div class="media-body">
             <h5 class="text-primary">${shows.attributes.canonicalTitle}</h5>
             <div><small>${shows.attributes.synopsis}</small></div>
             <form method="POST" action="/animeList">
             <input type="hidden" name="animeId" value="${shows.id}" />
             <button type="submit" name="animeName" value="${shows.attributes.canonicalTitle}">Review Anime</button>
             </form>
          </div>
         </div>  
       </div>
      `
  );

  $showList.append($show);
}

function sendID() {
  let animeID = getElementById("animeID".value);
}

/** Handle search form submission: get shows from API and display. **/

async function searchForShowAndDisplay() {
  const term = $("#search-query").val();
  const shows = await getShowsByTerm(term);

  $("#episodes-area").hide();
}

$searchForm.on("submit", async function (evt) {
  evt.preventDefault();
  await searchForShowAndDisplay();
});
