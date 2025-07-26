document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('div.section[id]').forEach(function (section) {
        var header = section.querySelector('h1, h2, h3, h4, h5, h6');
        if (header) {
            header.classList.add('section-header');
            var id = section.id;
            var link = document.createElement('a');
            link.classList.add('section-link');
            link.href = `#${id}`;
            link.textContent = header.textContent;
            header.textContent = '';
            header.appendChild(link);
        }
    });
});
