(function(){
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, {threshold:0.15, rootMargin:'0px 0px -60px 0px'});
  document.querySelectorAll('.reveal, .reveal-stagger').forEach(function(el){ io.observe(el); });

  if(!reduced){
    var parallaxData = Array.prototype.map.call(document.querySelectorAll('[data-parallax]'), function(el){
      return { el: el, speed: parseFloat(el.getAttribute('data-parallax')) || 0.1, lastOffset: 0 };
    });
    var ticking = false;
    function updateParallax(){
      parallaxData.forEach(function(d){
        // rect.top already includes last frame's transform, so subtract it back
        // out first — otherwise each tick compounds on the previous offset and
        // the element drifts far past its intended position over a long scroll.
        var rect = d.el.getBoundingClientRect();
        var staticTop = rect.top - d.lastOffset;
        var offset = (staticTop - window.innerHeight/2) * d.speed;
        d.el.style.transform = 'translateY(' + offset + 'px)';
        d.lastOffset = offset;
      });
      ticking = false;
    }
    window.addEventListener('scroll', function(){
      if(!ticking){ requestAnimationFrame(updateParallax); ticking = true; }
    }, {passive:true});
    updateParallax();
  }

  var contactForm = document.getElementById('contact-form');
  if(contactForm){
    contactForm.addEventListener('submit', function(e){
      e.preventDefault();
      var success = document.getElementById('form-success');
      if(success){ success.classList.add('visible'); }
      contactForm.reset();
    });
  }
})();
