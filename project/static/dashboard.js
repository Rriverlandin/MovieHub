// =========================================================
// dashboard.js
// Handles: search filter, animated add/edit modal, poster picker.
// Favorite / Watched / Delete are plain <form> POSTs handled
// server-side in app.py, so no fetch/AJAX needed for those.
// =========================================================

const posterOptions = ["🎬", "🌀", "🏚️", "🥁", "🏜️", "🍒", "🚀", "🗡️", "👻", "🎭", "🔫", "💔"];
let selectedPoster = "🎬";

const modal = document.getElementById("movieModal");
const modalTitle = document.getElementById("modalTitle");
const movieForm = document.getElementById("movieForm");
const posterGrid = document.getElementById("posterGrid");
const fieldRating = document.getElementById("fieldRating");
const ratingValue = document.getElementById("ratingValue");
const fieldPoster = document.getElementById("fieldPoster");
const saveBtn = document.getElementById("saveMovieBtn");
const searchInput = document.getElementById("searchInput");
const movieGrid = document.getElementById("movieGrid");
const emptyState = document.getElementById("emptyState");

const ADD_ACTION = movieForm.getAttribute("action");


// =========================
// Search (client-side filter, no reload)
// =========================

if (searchInput) {
  searchInput.addEventListener("keyup", () => {
    const query = searchInput.value.trim().toLowerCase();
    const cards = movieGrid.querySelectorAll(".movie-card");
    let visibleCount = 0;

    cards.forEach(card => {
      const title = card.dataset.title || "";
      const genre = card.dataset.genre || "";
      const match = title.includes(query) || genre.includes(query);
      card.style.display = match ? "" : "none";
      if (match) visibleCount++;
    });

    emptyState.hidden = visibleCount !== 0;
  });
}


// =========================
// Poster picker
// =========================

function buildPosterGrid() {
  posterGrid.innerHTML = "";
  posterOptions.forEach(p => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "mh-poster-opt" + (p === selectedPoster ? " is-active" : "");
    btn.textContent = p;
    btn.addEventListener("click", () => {
      selectedPoster = p;
      fieldPoster.value = p;
      buildPosterGrid();
    });
    posterGrid.appendChild(btn);
  });
}

fieldRating.addEventListener("input", () => {
  ratingValue.textContent = fieldRating.value;
});


// =========================
// Add / Edit modal (animated via .is-open class)
// =========================

function openAddModal() {
  modalTitle.textContent = "Add movie";
  saveBtn.textContent = "Add to collection";
  movieForm.setAttribute("action", ADD_ACTION);
  movieForm.reset();
  selectedPoster = "🎬";
  fieldPoster.value = selectedPoster;
  fieldRating.value = 7;
  ratingValue.textContent = 7;
  buildPosterGrid();
  showModal();
}

function openEditModal(btn) {
  const { id, title, year, genre, rating, poster, favorite, watched } = btn.dataset;

  modalTitle.textContent = "Edit movie";
  saveBtn.textContent = "Save changes";
  movieForm.setAttribute("action", ADD_ACTION.replace(/\/movie\/add.*/, `/movie/${id}/edit`));

  document.getElementById("fieldTitle").value = title;
  document.getElementById("fieldYear").value = year;
  document.getElementById("fieldGenre").value = genre;
  fieldRating.value = rating;
  ratingValue.textContent = rating;
  selectedPoster = poster || "🎬";
  fieldPoster.value = selectedPoster;
  document.getElementById("fieldFavorite").checked = favorite === "true";
  document.getElementById("fieldWatched").checked = watched === "true";

  buildPosterGrid();
  showModal();
}

function showModal() {
  modal.classList.add("is-open");
  document.body.style.overflow = "hidden";
  setTimeout(() => document.getElementById("fieldTitle").focus(), 200);
}

function closeModal() {
  modal.classList.remove("is-open");
  document.body.style.overflow = "";
}

document.getElementById("addMovieBtn").addEventListener("click", openAddModal);
document.getElementById("closeModalBtn").addEventListener("click", closeModal);

modal.addEventListener("click", (e) => {
  if (e.target === modal) closeModal();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && modal.classList.contains("is-open")) closeModal();
});

document.querySelectorAll(".edit-btn").forEach(btn => {
  btn.addEventListener("click", () => openEditModal(btn));
});


// =========================
// Staggered fade-in for cards on load
// (CSS handles the animation itself via .movie-card's keyframe +
//  the inline animation-delay set in dashboard.html; nothing to do here.)
// =========================
