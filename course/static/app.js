(function () {
  var KEY = "course-done";
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }
  var done = load();

  // Quizzes: click an option, get told right or wrong; right answer reveals the explanation.
  document.querySelectorAll(".q").forEach(function (fs) {
    var ans = +fs.dataset.answer;
    fs.querySelectorAll(".opt").forEach(function (b) {
      b.addEventListener("click", function () {
        var ok = +b.dataset.i === ans;
        b.classList.add(ok ? "right" : "wrong");
        b.setAttribute("aria-pressed", "true");
        if (ok) fs.classList.add("answered");
      });
    });
  });

  // Progress ticks.
  function paint() {
    document.querySelectorAll("button[data-done]").forEach(function (b) {
      var on = !!done[b.dataset.done];
      b.classList.toggle("on", on);
      b.textContent = on ? "✅ Done! (click to undo)" : "☐ I've done this lesson";
    });
    var cards = document.querySelectorAll(".card"), n = 0;
    cards.forEach(function (c) { var on = !!done[c.dataset.slug]; c.classList.toggle("done", on); if (on) n++; });
    var bar = document.querySelector(".progress");
    if (bar && cards.length) {
      bar.querySelector("span").textContent = n + " / " + cards.length + " done";
      bar.style.setProperty("--p", (n / cards.length * 100) + "%");
    }
  }
  document.querySelectorAll("button[data-done]").forEach(function (b) {
    b.addEventListener("click", function () {
      var s = b.dataset.done;
      if (done[s]) delete done[s]; else done[s] = 1;
      save(done); paint();
    });
  });
  paint();
})();
