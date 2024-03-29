"use strict";

const $showList = $("#shows-list");

const $searchForm = $("#search-form");

const $reviewForm = $("#review-form");

const $animeImage = $("#anime-image");

const api = "https://kitsu.io/api/edge/anime?filter[text]=";

async function getShowsByTerm(term) {
  //gets search result object from api
  const response = await axios.get(
    `https://kitsu.io/api/edge/anime?filter[text]=${term}`
  );
  $showList.empty();
  for (let anime of response.data.data) {
    populateShows(anime);
  }
}

async function getShowByID(id, i) {
  //Get show by show id.
  let animeDiv = document.getElementById(i);
  console.log(animeDiv);
  const response = await axios.get(`https://kitsu.io/api/edge/anime/${id}`);
  let img = response.data.data.attributes.coverImage;
  const animeImg = document.createElement("img");
  animeImg.src = img.tiny;
  animeDiv.after(animeImg);
}

/** Given list of shows, create markup for each and to DOM */

function populateShows(shows) {
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

/** Handle search form submission: get shows from API and display. **/

async function searchForShowAndDisplay() {
  const term = $("#search-query").val();
  const shows = await getShowsByTerm(term);
}

$searchForm.on("submit", async function (evt) {
  evt.preventDefault();
  await searchForShowAndDisplay();
});

window.addEventListener("DOMContentLoaded", (e) => {
  let animeImages = document.querySelectorAll("#animeId");
  let i = 0;
  animeImages.forEach((e) => {
    e.id = i;
    let id = e.value;
    getShowByID(id, i);
    i += 1;
  });
});
