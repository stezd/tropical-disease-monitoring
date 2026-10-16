/* TropiCare pitch deck — injects brand, progress dots, page number, background,
   and fits the 1920×1080 slide to the window (no scaling when printing).
   Each slide: <body data-slide="02-masalah"> + <div class="slide">…</div>. */
(function () {
  var ORDER = [
    "01-cover",
    "02-masalah",
    "03-solusi",
    "04-kompetitor",
    "05a-fitur",
    "05b-mulai",
    "05c-kuesioner",
    "05d-hasil",
    "05e-keselamatan",
    "06-alur",
    "07-skalabilitas",
    "08-feasibility",
    "09-terima-kasih",
  ];
  var base = document.currentScript.src.replace(/[^/]*$/, "");
  var NS = "http://www.w3.org/2000/svg";

  function plus(x, y, s) {
    return (
      '<path transform="translate(' + x + " " + y + ") scale(" + s + ')" ' +
      'd="M-2.5 -9h5v6.5h6.5v5h-6.5v6.5h-5v-6.5h-6.5v-5h6.5z" fill="#fff" opacity=".6"/>'
    );
  }

  function dots(x, y, cols, rows) {
    var out = '<g fill="#fff" opacity=".55">';
    for (var r = 0; r < rows; r++)
      for (var c = 0; c < cols; c++)
        out += '<circle cx="' + (x + c * 22) + '" cy="' + (y + r * 22) + '" r="3"/>';
    return out + "</g>";
  }

  function background() {
    return (
      '<svg class="deck-bg" viewBox="0 0 1920 1080" aria-hidden="true" xmlns="' + NS + '">' +
      '<circle cx="1760" cy="140" r="330" fill="#a9d7d0" opacity=".38"/>' +
      '<circle cx="90" cy="1000" r="300" fill="#e4f4f1" opacity=".7"/>' +
      '<circle cx="1560" cy="1010" r="210" fill="#a9d7d0" opacity=".3"/>' +
      '<circle cx="260" cy="70" r="150" fill="#fff" opacity=".28"/>' +
      dots(1600, 190, 6, 4) +
      dots(70, 760, 5, 4) +
      plus(330, 190, 1.8) + plus(1500, 980, 1.5) + plus(960, 70, 1.1) +
      plus(1840, 560, 1.3) + plus(50, 520, 1.2) + plus(700, 1030, 1.0) +
      "</svg>"
    );
  }

  function chrome(slide, name) {
    var idx = ORDER.indexOf(name);
    var wrap = document.createElement("div");
    var dotsHtml = "";
    ORDER.forEach(function (n, i) {
      var cls = i < idx ? "done" : i === idx ? "cur" : "";
      dotsHtml += '<div class="st ' + cls + '">' + (i < idx ? "✓" : "") + "</div>";
      if (i < ORDER.length - 1)
        dotsHtml += '<div class="sl ' + (i < idx ? "done" : "") + '"></div>';
    });
    wrap.innerHTML =
      '<div class="brand"><div class="brand-mascot"><img src="' + base +
      'mascot.svg" alt=""></div><div>Tropi<span>Care</span></div></div>' +
      '<div class="progress">' + dotsHtml + "</div>" +
      '<div class="pageno">' + String(idx + 1).padStart(2, "0") + " / " +
      String(ORDER.length).padStart(2, "0") + "</div>";
    while (wrap.firstChild) slide.appendChild(wrap.firstChild);
  }

  function fit() {
    var slide = document.querySelector(".slide");
    if (!slide) return;
    var s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    if (window.matchMedia("print").matches || s > 0.995) s = 1;
    slide.style.transform = s === 1 ? "none" : "scale(" + s + ")";
  }

  function init() {
    var slide = document.querySelector(".slide");
    if (!slide) return;
    var name = document.body.getAttribute("data-slide") || "";
    slide.insertAdjacentHTML("afterbegin", background());
    chrome(slide, name);
    fit();
  }

  window.addEventListener("resize", fit);
  window.addEventListener("beforeprint", fit);
  window.addEventListener("afterprint", fit);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
