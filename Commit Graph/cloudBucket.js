  fetch('https://us-central1-mystic-span-415322.cloudfunctions.net/notion-export', {
    method: 'GET', // or 'POST' if needed
    headers: {
      'Content-Type': 'application/json',
      // Add any additional headers as needed
    },
  })
    .then(response => response.json())
    .then(data => {
      // Handle the JSON data returned by the Cloud Function
      console.log(data);
    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error('Error:', error);
    });
  