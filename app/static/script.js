// element selectors
const whoText = document.querySelector("#input-who");
const whatText = document.querySelector("#input-what");
const submitButton = document.querySelector("#query");
const loader = document.querySelector("#loader");
const form = document.querySelector(".form");
const results = document.querySelector(".results");
const gifterTitle = document.querySelector("h1");
const homeButton = document.querySelector("#home");
const filterButtons = document.querySelectorAll(".filter");

// event listeners
// submitButton.addEventListener("click", showLoader);
homeButton.addEventListener("click", goHome);

$(document).ready(function() {
  console.log(results.innerHTML.trim());
  if (results.innerHTML.trim() != "") {
    showLoader();
  }
  else {
    gifterTitle.style.opacity = "1";
    gifterTitle.style.fontSize = "65px";
    form.classList.add("active");
  }
});

// happy gifting button page transition
function showLoader() {
    form.classList.remove("active");
    loader.classList.add("active");
    setTimeout(showResults, 800);
}

function showResults() {
  loader.classList.remove("active");
  results.classList.add("active");
  gifterTitle.classList.add("newPos");
  homeButton.classList.add("active");
}

// return to form
function goHome() {
  window.history.back();
}

// return to home transition
function showHome() {
  results.classList.remove("active");
  gifterTitle.classList.remove("newPos");
  homeButton.classList.remove("active");
  form.classList.add("active");
}
