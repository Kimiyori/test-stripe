const checkoutButton = document.getElementById("checkout-button");

checkoutButton.addEventListener('click', function () {
    fetch(session_url, {
    method: "POST",
    headers: {
      "Accept": "application/json",
    "Content-Type": "application/json",
      'X-CSRFToken': csrftoken
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (session) {
      return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(function (result) {
      // If redirectToCheckout fails due to a browser or network
      // error, you should display the localized error message to your
      // customer using error.message.
      if (result.error) {
        alert(result.error.message);
      }
    })
    .catch(function (error) {
      console.error("Error:", error);
    });
});