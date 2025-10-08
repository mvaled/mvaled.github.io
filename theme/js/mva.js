const validUserSelectedSchemes = new Set(["auto", "light", "dark"]);

function onColorSchemeChange() {
    let userSelectedScheme = localStorage.getItem('userColorScheme');
    if (!validUserSelectedSchemes.has(userSelectedScheme)) {
        userSelectedScheme = "auto"
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
            if (id != "footnotes") {
                // Check if we already processed this header
                if (!header.querySelector('.section-anchor')) {
                    // Create an invisible anchor element that provides the clickable area
                    var anchor = document.createElement('a');
                    anchor.classList.add('section-anchor');
                    anchor.href = `#${id}`;
                    anchor.setAttribute('aria-label', 'Link to this section');

                    // Make the entire header clickable by wrapping it
                    var wrapper = document.createElement('a');
                    wrapper.classList.add('section-link');
                    wrapper.href = `#${id}`;
                    wrapper.setAttribute('aria-label', 'Link to this section');

                    // Move all header content into the wrapper
                    while (header.firstChild) {
                        wrapper.appendChild(header.firstChild);
                    }

                    // Add the wrapper back to the header
                    header.appendChild(wrapper);
                }
            }
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

function wrapFootnoteReferences() {
    document.querySelectorAll('a.footnote-reference').forEach(function (el) {
        if (!el.querySelector('sup')) {
            el.innerHTML = '<sup>' + el.innerHTML + '</sup>';
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
        wrapFootnoteReferences();
    })

    replaceSectionHeader();
    makeInlinedCodeNonbreak();
    wrapFootnoteReferences();
});
