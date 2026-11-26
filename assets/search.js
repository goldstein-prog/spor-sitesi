(function () {
  var q = document.getElementById("q"), res = document.getElementById("res"), idx = null;
  function norm(s) { return s.toLocaleLowerCase("tr").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ı/g, "i"); }
  function load(cb) {
    if (idx) return cb();
    fetch(window.BASE + "/assets/index.json").then(function (r) { return r.json(); }).then(function (d) {
      idx = d.map(function (x) { x.k = norm(x.n + " " + x.c); return x; }); cb();
    });
  }
  q.addEventListener("input", function () {
    var v = norm(q.value.trim());
    if (v.length < 2) { res.innerHTML = ""; return; }
    load(function () {
      var hits = idx.filter(function (x) { return x.k.indexOf(v) >= 0; }).slice(0, 8);
      res.innerHTML = hits.length ? hits.map(function (x) {
        return '<a href="' + x.u + '"><span>' + x.n + '<small>' + x.c + '</small></span><b>' + x.v + '</b></a>';
      }).join("") : '<div class="none">Sonuç yok</div>';
    });
  });
  document.addEventListener("click", function (ev) { if (!res.contains(ev.target) && ev.target !== q) res.innerHTML = ""; });
})();
