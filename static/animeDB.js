"use strict";

const $showList = $("#shows-list");

const $searchForm = $("#search-form");

const api = "https://kitsu.io/api/edge/anime?filter[text]=";

async function getShowsByTerm(term) {
  //gets result object from api
  const response = await axios.get(
    `https://kitsu.io/api/edge/anime?filter[text]=${term}`
  );
  console.log(response);

  //puts results into a usable object
  let anime = response.data.data.map((item) => {
    const id = item.id;
    const title = item.attributes.canonicalTitle;
    const description = item.attributes.description;
    const image = item.attributes.posterImage.original;
    const rating = item.attributes.ageRating;
  });
  console.log(anime);
  return anime;
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
