document.documentElement.dataset.app = "project-tracker";

const parseAndSwap = async (response) => {
  const html = await response.text();
  const doc = new DOMParser().parseFromString(html, "text/html");
  const swaps = doc.querySelectorAll("template[data-swap-target]");

  swaps.forEach((swap) => {
    const selector = swap.dataset.swapTarget;
    const target = document.querySelector(selector);
    if (!target) {
      return;
    }

    const replacement = swap.innerHTML.trim();
    const replacementDoc = new DOMParser().parseFromString(
      `<body>${replacement}</body>`,
      "text/html",
    );
    const nextRoot = replacementDoc.body.firstElementChild;

    if (replacementDoc.body.childElementCount === 1 && nextRoot?.id && nextRoot.id === target.id) {
      target.outerHTML = replacement;
      return;
    }

    target.innerHTML = replacement;
  });
};

const submitAsyncForm = async (form) => {
  const confirmMessage = form.dataset.confirm;
  if (confirmMessage && !window.confirm(confirmMessage)) {
    return;
  }

  const response = await fetch(form.action, {
    method: form.method || "POST",
    body: new FormData(form),
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  });

  await parseAndSwap(response);
};

const loadAsyncLink = async (link) => {
  const response = await fetch(link.href, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  });

  await parseAndSwap(response);
};

document.addEventListener("submit", (event) => {
  const form = event.target.closest("form[data-async-form]");
  if (!form) {
    return;
  }

  event.preventDefault();
  submitAsyncForm(form).catch(() => {
    window.alert("The update could not be completed.");
  });
});

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[data-async-link]");
  if (!link) {
    return;
  }

  event.preventDefault();
  loadAsyncLink(link).catch(() => {
    window.alert("The form could not be loaded.");
  });
});
