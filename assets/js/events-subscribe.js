(function () {
  "use strict";

  var form = document.getElementById("events-subscribe-form");
  var btn = document.getElementById("subscribe-btn");
  var successEl = document.getElementById("subscribe-success");
  var errorEl = document.getElementById("subscribe-error");

  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    var email = document.getElementById("subscribe-email").value.trim();
    if (!email) return;

    var checked = Array.from(
      form.querySelectorAll('input[name="congress"]:checked')
    ).map(function (cb) {
      return cb.value;
    });

    if (checked.length === 0) {
      alert("Please select at least one congress.");
      return;
    }

    btn.disabled = true;
    btn.textContent = "Subscribing…";

    var apiKey = window.BUTTONDOWN_API_KEY || "";
    var payload = {
      email_address: email,
      tags: checked,
      metadata: { congresses: checked.join(",") },
    };

    fetch("https://api.buttondown.email/v1/subscribers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + apiKey,
      },
      body: JSON.stringify(payload),
    })
      .then(function (res) {
        if (res.ok || res.status === 201) {
          form.style.display = "none";
          successEl.style.display = "block";
        } else if (res.status === 409) {
          // Already subscribed — treat as success
          form.style.display = "none";
          successEl.style.display = "block";
        } else {
          throw new Error("Status " + res.status);
        }
      })
      .catch(function () {
        btn.disabled = false;
        btn.textContent = "Subscribe";
        errorEl.style.display = "block";
      });
  });
})();
