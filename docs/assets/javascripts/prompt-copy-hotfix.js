/* Deploy hotfix:
 * Provide a robust copyPrompt fallback if cached chat.js doesn't include it.
 */
(function () {
  function fallbackCopy(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "absolute";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
  }

  window.copyPrompt = function (btn) {
    const container = btn && btn.closest(".prompt-block-enhanced");
    if (!container) return;
    const contentNode = container.querySelector(".prompt-content");
    if (!contentNode) return;
    const content = contentNode.innerText;

    const originalIcon = btn.innerHTML;
    const doneIcon =
      '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4CAF50" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>';

    const success = function () {
      btn.innerHTML = doneIcon;
      setTimeout(function () {
        btn.innerHTML = originalIcon;
      }, 2000);
    };

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(content).then(success).catch(function () {
        fallbackCopy(content);
        success();
      });
      return;
    }

    fallbackCopy(content);
    success();
  };
})();
