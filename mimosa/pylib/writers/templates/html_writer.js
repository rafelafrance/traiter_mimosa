document.querySelectorAll('thead')
    .forEach(thead => {
        thead.addEventListener('click', function(event) {
          if (! event.target.matches('button')) { return; }
          event.target.classList.toggle('closed');
          const index = event.target.dataset.index;
          const selector = `tbody[data-index="${index}"]`;
          document.querySelector(selector).classList.toggle('closed');
        });
    });

 document.querySelector('tbody')
    .addEventListener('click', function(event) {
        if (! event.target.matches('button')) { return; }
        const textId = event.target.dataset.textId;
        const selector = `[data-text-id="${textId}"]`;
        const elts = document.querySelectorAll(selector);
        elts.forEach(function(tr) {  tr.classList.toggle('closed'); });
    });
