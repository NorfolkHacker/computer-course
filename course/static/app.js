(function () {
  var KEY = "course-done";
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }
  var done = load();
  document.documentElement.classList.add("js");

  // Distro tabs (Linux course): one bar per group, choice remembered across pages.
  var TAB_KEY = "linux-distro";
  var LABELS = { debian: "Debian · Ubuntu · Mint", fedora: "Fedora · RHEL", arch: "Arch · Manjaro" };
  function getTab() { try { return localStorage.getItem(TAB_KEY); } catch (e) { return null; } }
  function setTab(t) { try { localStorage.setItem(TAB_KEY, t); } catch (e) {} }
  var groups = document.querySelectorAll(".platforms.tabs");
  function showTabs(choice) {
    groups.forEach(function (g) {
      var panes = g.querySelectorAll(":scope > [data-tab]");
      var names = Array.prototype.map.call(panes, function (p) { return p.dataset.tab; });
      var pick = names.indexOf(choice) >= 0 ? choice : names[0];
      panes.forEach(function (p) { p.classList.toggle("active", p.dataset.tab === pick); });
      g.querySelectorAll(".tabbar button").forEach(function (b) {
        var on = b.dataset.tab === pick;
        b.classList.toggle("active", on);
        b.setAttribute("aria-selected", on ? "true" : "false");
      });
    });
  }
  groups.forEach(function (g) {
    var bar = document.createElement("div");
    bar.className = "tabbar";
    bar.setAttribute("role", "tablist");
    g.querySelectorAll(":scope > [data-tab]").forEach(function (p) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("role", "tab");
      b.dataset.tab = p.dataset.tab;
      b.textContent = LABELS[p.dataset.tab] || p.dataset.tab;
      b.addEventListener("click", function () { setTab(b.dataset.tab); showTabs(b.dataset.tab); });
      bar.appendChild(b);
    });
    g.insertBefore(bar, g.firstChild);
  });
  if (groups.length) showTabs(getTab());

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
