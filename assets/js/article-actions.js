/* zyekh.com — Article Actions (Share, Download .md, Download .pdf, Scroll Progress & 1-Click Code Copy) */
document.addEventListener('DOMContentLoaded', function () {
  var shareBtn = document.getElementById('shareBtn');
  var downloadMdBtn = document.getElementById('downloadMdBtn');
  var downloadPdfBtn = document.getElementById('downloadPdfBtn');

  // 1. Reading Progress Bar
  var progressBar = document.querySelector('.reading-progress-bar');
  if (!progressBar) {
    progressBar = document.createElement('div');
    progressBar.className = 'reading-progress-bar';
    document.body.appendChild(progressBar);
  }
  var updateProgress = function () {
    var winScroll = document.documentElement.scrollTop || document.body.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = height > 0 ? (winScroll / height) * 100 : 0;
    progressBar.style.width = scrolled + '%';
  };
  window.addEventListener('scroll', function () {
    window.requestAnimationFrame(updateProgress);
  }, { passive: true });

  // 2. 1-Click Copy Code Snippets
  var codeBlocks = document.querySelectorAll('.article-content pre');
  codeBlocks.forEach(function (pre) {
    if (pre.parentElement && pre.parentElement.classList.contains('code-block-wrapper')) return;
    var wrapper = document.createElement('div');
    wrapper.className = 'code-block-wrapper';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    var copyBtn = document.createElement('button');
    copyBtn.type = 'button';
    copyBtn.className = 'copy-code-btn';
    copyBtn.setAttribute('aria-label', 'Copy code snippet to clipboard');
    copyBtn.textContent = '[ COPY ]';

    copyBtn.addEventListener('click', function () {
      var code = pre.querySelector('code');
      var textToCopy = code ? code.innerText : pre.innerText;
      if (navigator.clipboard) {
        navigator.clipboard.writeText(textToCopy).then(function () {
          copyBtn.textContent = '[ COPIED ]';
          copyBtn.classList.add('copied');
          setTimeout(function () {
            copyBtn.textContent = '[ COPY ]';
            copyBtn.classList.remove('copied');
          }, 2000);
        }).catch(function () {});
      }
    });

    wrapper.appendChild(copyBtn);
  });

  if (shareBtn) {
    shareBtn.addEventListener('click', function () {
      if (navigator.share) {
        navigator.share({ title: document.title, url: window.location.href }).catch(function () {});
        return;
      }
      if (navigator.clipboard) {
        navigator.clipboard.writeText(window.location.href);
        var orig = shareBtn.textContent;
        shareBtn.textContent = 'Link Copied!';
        setTimeout(function () { shareBtn.textContent = orig; }, 2000);
      }
    });
  }

  if (downloadPdfBtn) {
    downloadPdfBtn.addEventListener('click', function () {
      window.print();
    });
  }

  if (downloadMdBtn) {
    downloadMdBtn.addEventListener('click', function () {
      var titleEl = document.querySelector('.article-title');
      var title = titleEl ? titleEl.innerText : document.title;
      var catEl = document.querySelector('.meta-tag');
      var category = catEl ? catEl.innerText : '';
      var content = document.querySelector('.article-content');
      if (!content) return;

      var mdText = '# ' + title + '\n\n';
      if (category) mdText += '**Category**: ' + category + '\n\n';
      mdText += '**URL**: ' + window.location.href + '\n\n---\n\n';

      var elements = content.querySelectorAll('h2, h3, p, ul, ol, pre');
      elements.forEach(function (el) {
        var tag = el.tagName.toLowerCase();
        if (tag === 'h2') {
          mdText += '\n## ' + el.innerText.trim() + '\n\n';
        } else if (tag === 'h3') {
          mdText += '\n### ' + el.innerText.trim() + '\n\n';
        } else if (tag === 'p') {
          mdText += el.innerText.trim() + '\n\n';
        } else if (tag === 'ul' || tag === 'ol') {
          el.querySelectorAll('li').forEach(function (li) {
            mdText += '- ' + li.innerText.trim() + '\n';
          });
          mdText += '\n';
        } else if (tag === 'pre') {
          var code = el.querySelector('code');
          var lang = '';
          if (code) {
            var classes = Array.from(code.classList);
            for (var i = 0; i < classes.length; i++) {
              if (classes[i].indexOf('language-') === 0) {
                lang = classes[i].replace('language-', '');
                break;
              }
            }
          }
          mdText += '```' + lang + '\n' + el.innerText.trim() + '\n```\n\n';
        }
      });

      var filename = window.location.pathname.split('/').pop().replace('.html', '') || 'article';
      var blob = new Blob([mdText], { type: 'text/markdown;charset=utf-8;' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = filename + '.md';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }
});
