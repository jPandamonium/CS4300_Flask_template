// element selectors
const whoText = document.querySelector("#input-who");
const whatText = document.querySelector("#input-what");
const submitButton = document.querySelector("#query");
const loader = document.querySelector("#loader");
const form = document.querySelector(".form");
const results = document.querySelector(".results");
const gifterTitle = document.querySelector("h1");
const homeButton = document.querySelector("#home");

// event listeners
// submitButton.addEventListener("click", showLoader);
//homeButton.addEventListener("click", showHome);

// on load animation


// happy gifting button page transition
function showLoader() {
    if (whoText.value == "" || whatText.value == "") return;
    loader.classList.add("active");
    form.classList.remove("active");
    setTimeout(showResults, 2000);
}

function showResults() {
  loader.classList.remove("active");
  results.classList.add("active");
  gifterTitle.classList.add("newPos");
  homeButton.classList.add("active");
}

// return to home transition
function showHome() {
  results.classList.remove("active");
  gifterTitle.classList.remove("newPos");
  homeButton.classList.remove("active");
  form.classList.add("active");
}

// append item to results
