(function () {
  var root = document.querySelector(".carousel");
  if (!root) return;

  var viewport = root.querySelector(".carousel-viewport");
  var track = root.querySelector(".carousel-track");
  var prev = root.querySelector(".carousel-prev");
  var next = root.querySelector(".carousel-next");
  var originals = Array.prototype.slice.call(track.querySelectorAll(".carousel-slide"));
  if (!viewport || !track || !prev || !next || originals.length < 2) return;

  var count = originals.length;
  var prependCount = 2;
  var appendCount = 4;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var intervalMs = 5000;
  var index = 0;
  var timer = null;
  var pendingSnap = null;

  function cloneSlide(slide) {
    var copy = slide.cloneNode(true);
    copy.classList.add("is-clone");
    copy.setAttribute("aria-hidden", "true");
    copy.alt = "";
    return copy;
  }

  var anchor = track.firstChild;
  for (var i = 0; i < prependCount; i++) {
    track.insertBefore(cloneSlide(originals[count - prependCount + i]), anchor);
  }
  for (var j = 0; j < appendCount; j++) {
    track.appendChild(cloneSlide(originals[j % count]));
  }

  function metrics() {
    var styles = getComputedStyle(track);
    var gap = parseFloat(styles.columnGap || styles.gap);
    if (!isFinite(gap)) gap = 0;
    var slide = track.querySelector(".carousel-slide").getBoundingClientRect().width;
    var view = viewport.getBoundingClientRect().width;
    return {
      step: slide + gap,
      peek: (view - 3 * slide - 2 * gap) / 2,
    };
  }

  function offsetFor(realIndex) {
    var m = metrics();
    return m.peek - (realIndex + prependCount) * m.step;
  }

  function setTransition(on) {
    track.style.transition = on && !reduceMotion ? "" : "none";
  }

  function markVisible() {
    originals.forEach(function (slide, i) {
      var delta = (i - index + count) % count;
      var inView = delta <= 3 || delta === count - 1;
      if (inView) slide.removeAttribute("aria-hidden");
      else slide.setAttribute("aria-hidden", "true");
    });
  }

  function place(realIndex, animate) {
    index = (realIndex % count + count) % count;
    setTransition(animate);
    track.style.transform = "translateX(" + offsetFor(index) + "px)";
    if (!animate) track.getBoundingClientRect();
    setTransition(true);
    markVisible();
  }

  function step(delta) {
    var target = index + delta;
    var wrapped = target < 0 || target >= count;
    setTransition(true);
    track.style.transform = "translateX(" + offsetFor(target) + "px)";
    index = (target % count + count) % count;
    markVisible();
    pendingSnap = wrapped ? index : null;
    stop();
    start();
  }

  track.addEventListener("transitionend", function (event) {
    if (event.target !== track || event.propertyName !== "transform") return;
    if (pendingSnap === null) return;
    var dest = pendingSnap;
    pendingSnap = null;
    place(dest, false);
  });

  function start() {
    if (reduceMotion || timer || document.hidden) return;
    timer = window.setInterval(function () {
      step(1);
    }, intervalMs);
  }

  function stop() {
    if (!timer) return;
    window.clearInterval(timer);
    timer = null;
  }

  prev.addEventListener("click", function () {
    step(-1);
  });
  next.addEventListener("click", function () {
    step(1);
  });

  root.addEventListener("mouseenter", stop);
  root.addEventListener("mouseleave", start);
  root.addEventListener("focusin", stop);
  root.addEventListener("focusout", function (event) {
    if (!root.contains(event.relatedTarget)) start();
  });
  root.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      step(-1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      step(1);
    }
  });

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) stop();
    else start();
  });

  window.addEventListener("resize", function () {
    place(index, false);
  });

  place(0, false);
  start();
})();
