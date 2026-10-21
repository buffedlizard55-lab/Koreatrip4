// ============================================================================
// KOREA ITINERARY SITE — APP.JS
// Mobile menu, accessibility, and page-specific interactivity
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  initMobileMenu();
  initSkipLink();
  initCurrentPageHighlight();
});

// Mobile navigation toggle
function initMobileMenu() {
  const btn = document.querySelector(".menu-btn");
  const links = document.querySelector(".nav-links");

  if (!btn || !links) return;

  btn.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    btn.setAttribute("aria-expanded", open);
    btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });

  // Close menu when clicking a link
  links.querySelectorAll("a").forEach((a) => {
    a.addEventListener("click", () => {
      links.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
      btn.setAttribute("aria-label", "Open menu");
    });
  });

  // Close on Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && links.classList.contains("open")) {
      links.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    }
  });
}

// Skip link focus styling
function initSkipLink() {
  const skip = document.querySelector(".skip-link");
  if (!skip) return;
  skip.addEventListener("focus", () => {
    skip.style.left = "0.5rem";
    skip.style.top = "0.5rem";
    skip.style.width = "auto";
    skip.style.height = "auto";
    skip.style.padding = "0.5rem 1rem";
    skip.style.background = "#000";
    skip.style.color = "#fff";
    skip.style.zIndex = "9999";
    skip.style.borderRadius = "4px";
    skip.style.textDecoration = "none";
  });
  skip.addEventListener("blur", () => {
    skip.style.left = "-9999px";
  });
}

// Highlight current page in nav
function initCurrentPageHighlight() {
  const path = window.location.pathname.split("/").pop() || "index.html";
  const links = document.querySelectorAll(".nav-links a");
  links.forEach((a) => {
    const href = a.getAttribute("href");
    if (href && path === href.split("/").pop()) {
      a.classList.add("active");
      a.setAttribute("aria-current", "page");
    }
  });
}