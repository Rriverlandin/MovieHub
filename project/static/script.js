// =========================
// MovieHub JavaScript
// =========================

let movies = [
  { id: 1, title: "Inception", year: 2010, rating: 9, genre: "Sci-Fi", poster: "🌀", watched: true, favorite: true },
  { id: 2, title: "Parasite", year: 2019, rating: 9, genre: "Thriller", poster: "🏚️", watched: true, favorite: true },
  { id: 3, title: "Whiplash", year: 2014, rating: 8, genre: "Drama", poster: "🥁", watched: true, favorite: false },
  { id: 4, title: "Dune", year: 2021, rating: 8, genre: "Sci-Fi", poster: "🏜️", watched: false, favorite: false },
  { id: 5, title: "Amélie", year: 2001, rating: 8, genre: "Romance", poster: "🍒", watched: true, favorite: true },
];

const posterOptions = ["🎬", "🌀", "🏚️", "🥁", "🏜️", "🍒", "🚀", "🗡️", "👻", "🎭", "🔫", "💔"];

let editingId = null;
let selectedPoster = "🎬";

const movieGrid = document.getElementById("movieGrid");
const emptyState = document.getElementById("emptyState");
const searchInput = document.getElementById("searchInput");
const modal = document.getElementById("movieModal");
const modalTitle = document.getElementById("modalTitle");
const movieForm = document.getElementById("movieForm");
const posterGrid = document.getElementById("posterGrid");
const fieldRating = document.getElementById("fieldRating");
const ratingValue = document.getElementById("ratingValue");


// =========================
// Render
// =========================

function renderStats() {
  document.getElementById("statTotal").textContent = movies.length;
  document.getElementById("statWatched").textContent = movies.filter(m => m.watched).length;
  document.getElementById("statFavorites").textContent = movies.filter(m => m.favorite).length;
}

function buildPerforation() {
  const wrap = document.createElement("div");
  wrap.className = "mh-perf";
  wrap.setAttribute("aria-hidden", "true");
  for (let i = 0; i < 10; i++) {
    wrap.appendChild(document.createElement("span"));
  }
  return wrap;
}

function buildCard(movie) {
  const card = document.createElement("div");
  card.className = "movie-card";
  card.dataset.title = movie.title;
  card.dataset.genre = movie.genre;
  card.dataset.id = movie.id;

  card.innerHTML = `
    <div class="mh-poster">
      <span>${movie.poster || "🎬"}</span>
      ${movie.favorite ? `<span class="mh-fav-badge">❤️</span>` : ""}
    </div>
  `;

  card.appendChild(buildPerforation());

  const body = document.createElement("div");
  body.className = "mh-card-body";
  body.innerHTML = `
    <h3>${movie.title}</h3>
    <p class="mh-meta">${movie.year}${movie.genre ? ` · ${movie.genre}` : ""}</p>
    <div class="mh-rating">⭐ <span>${movie.rating}/10</span></div>
    <div class="mh-toggles">
      <button class="mh-chip favorite-btn ${movie.favorite ? "is-on mh-chip-fav" : ""}">
        ${movie.favorite ? "❤️" : "🤍"} Favorite
      </button>
      <button class="mh-chip watched-btn ${movie.watched ? "is-on mh-chip-watched" : ""}">
        ✔ Watched
      </button>
    </div>
    <div class="mh-actions">
      <button class="edit-btn">✎ Edit</button>
      <button class="delete-btn mh-danger">🗑 Delete</button>
    </div>
  `;
  card.appendChild(body);

  // wire up events
  body.querySelector(".favorite-btn").addEventListener("click", () => toggleFavorite(movie.id));
  body.querySelector(".watched-btn").addEventListener("click", () => toggleWatched(movie.id));
  body.querySelector(".edit-btn").addEventListener("click", () => openEditModal(movie.id));
  body.querySelector(".delete-btn").addEventListener("click", () => handleDelete(movie.id));

  return card;
}

function renderMovies() {
  movieGrid.innerHTML = "";
  const query = searchInput.value.trim().toLowerCase();

  const visible = movies.filter(m =>
    m.title.toLowerCase().includes(query) || m.genre.toLowerCase().includes(query)
  );

  emptyState.hidden = visible.length !== 0;

  visible.forEach((movie, index) => {
    const card = buildCard(movie);
    // fade-in animation, staggered
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    movieGrid.appendChild(card);
    setTimeout(() => {
      card.style.transition = "0.4s ease";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, index * 80);
  });

  renderStats();
}


// =========================
// Search Movies
// =========================

if (searchInput) {
  searchInput.addEventListener("keyup", renderMovies);
}


// =========================
// Favorite / Watched toggles
// =========================

function toggleFavorite(id) {
  const movie = movies.find(m => m.id === id);
  if (movie) movie.favorite = !movie.favorite;
  renderMovies();
}

function toggleWatched(id) {
  const movie = movies.find(m => m.id === id);
  if (movie) movie.watched = !movie.watched;
  renderMovies();
}


// =========================
// Confirm Delete
// =========================

function handleDelete(id) {
  const confirmDelete = confirm("Are you sure you want to delete this movie?");
  if (!confirmDelete) return;
  movies = movies.filter(m => m.id !== id);
  renderMovies();
}


// =========================
// Add / Edit modal
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
      buildPosterGrid();
    });
    posterGrid.appendChild(btn);
  });
}

function openAddModal() {
  editingId = null;
  selectedPoster = "🎬";
  modalTitle.textContent = "Add movie";
  document.getElementById("saveMovieBtn").textContent = "Add to collection";
  movieForm.reset();
  fieldRating.value = 7;
  ratingValue.textContent = 7;
  buildPosterGrid();
  modal.hidden = false;
  document.getElementById("fieldTitle").focus();
}

function openEditModal(id) {
  const movie = movies.find(m => m.id === id);
  if (!movie) return;
  editingId = id;
  selectedPoster = movie.poster;
  modalTitle.textContent = "Edit movie";
  document.getElementById("saveMovieBtn").textContent = "Save changes";

  document.getElementById("fieldTitle").value = movie.title;
  document.getElementById("fieldYear").value = movie.year;
  document.getElementById("fieldGenre").value = movie.genre;
  fieldRating.value = movie.rating;
  ratingValue.textContent = movie.rating;
  document.getElementById("fieldFavorite").checked = movie.favorite;
  document.getElementById("fieldWatched").checked = movie.watched;

  buildPosterGrid();
  modal.hidden = false;
  document.getElementById("fieldTitle").focus();
}

function closeModal() {
  modal.hidden = true;
}

fieldRating.addEventListener("input", () => {
  ratingValue.textContent = fieldRating.value;
});

document.getElementById("addMovieBtn").addEventListener("click", openAddModal);
document.getElementById("closeModalBtn").addEventListener("click", closeModal);
modal.addEventListener("click", (e) => {
  if (e.target === modal) closeModal();
});

movieForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const title = document.getElementById("fieldTitle").value.trim();
  if (!title) return;

  const data = {
    title,
    year: Number(document.getElementById("fieldYear").value) || new Date().getFullYear(),
    genre: document.getElementById("fieldGenre").value.trim(),
    rating: Number(fieldRating.value),
    poster: selectedPoster,
    favorite: document.getElementById("fieldFavorite").checked,
    watched: document.getElementById("fieldWatched").checked,
  };

  if (editingId) {
    const movie = movies.find(m => m.id === editingId);
    Object.assign(movie, data);
  } else {
    movies.unshift({ id: Date.now(), ...data });
  }

  closeModal();
  renderMovies();
});


// =========================
// Init
// =========================

document.addEventListener("DOMContentLoaded", () => {
  console.log("🎬 MovieHub Loaded");
  renderMovies();
});
