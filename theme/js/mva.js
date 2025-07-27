const validUserSelectedSchemes = new Set(["auto", "light", "dark"]);

function onColorSchemeChange() {
    let userSelectedScheme = localStorage.getItem('userColorScheme');
    if (!validUserSelectedSchemes.has(userSelectedScheme)) {
        userSelectedScheme="auto"
    }
    if (userSelectedScheme != "auto") {
        document.documentElement.setAttribute('data-color-scheme', userSelectedScheme)
    } else {
        let preferredScheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-color-scheme', preferredScheme)
    }
    document.documentElement.setAttribute('data-user-color-scheme', userSelectedScheme)
}

function setUserColorScheme(scheme) {
    if (validUserSelectedSchemes.has(scheme)) {
        if (scheme != "auto") {
            localStorage.setItem('userColorScheme', scheme);
        } else {
            localStorage.removeItem('userColorScheme');
        }
        onColorSchemeChange();
    }
}

function replaceSectionHeader() {
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
}

function makeInlinedCodeNonbreak() {
    document.querySelectorAll('p tt.docutils.literal').forEach(function (el) {
        var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        var node;
        while (node = walker.nextNode()) {
            node.nodeValue = node.nodeValue.replace(/ /g, '\u00A0');
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const colorSchemeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = _ => onColorSchemeChange();
    colorSchemeQuery.addEventListener('change', handleChange);

    document.documentElement.addEventListener("htmx:afterSwap", () => {
        replaceSectionHeader();
        makeInlinedCodeNonbreak();
    })

    replaceSectionHeader();
    makeInlinedCodeNonbreak();
});
