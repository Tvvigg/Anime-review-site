"use strict";
const $showList = $("#shows-list");

const $searchForm = $("#search-form");

const api = "https://kitsu.io/api/edge/anime?filter[text]=";

async function getShowsByTerm(term) {
  //gets result object from api
  const response = await axios.get(`${api}${term}`);

  //puts results into a usable object
  return response.data.map((result) => {
    const show = result.show;
    return {
      id: show.id,
      titles: show.titles,
      synopsis: show.synopsis,
      image: show.coverImage ? show.coverImage.original : MISSING_IMAGE_URL,
    };
  });
}

/** Given list of shows, create markup for each and to DOM */

function populateShows(shows) {
  // const $showsList = $("#shows-list");
  $showList.empty();

  for (let show of shows) {
    const $show = $(
      `<div data-show-id="${show.id}" class="Show col-md-12 col-lg-6 mb-4">
         <div class="media">
         <img src="${show.image}" alt="${show.titles}">
          <div class="media-body">
             <h5 class="text-primary">${show.titles}</h5>
             <div><small>${show.synopsis}</small></div>
             <button class="btn btn-outline-light btn-sm Show-getEpisodes">
               Episodes
             </button>
           </div>
         </div>  
       </div>
      `
    );

    $showList.append($show);
  }
}

/** Handle search form submission: get shows from API and display.
 *    Hide episodes area (that only gets shown if they ask for episodes)
 */

async function searchForShowAndDisplay() {
  const term = $("#search-query").val();
  const shows = await getShowsByTerm(term);

  $("#episodes-area").hide();

  populateShows(shows);
}

$searchForm.on("submit", async function (evt) {
  evt.preventDefault();
  await searchForShowAndDisplay();
});
