const form = document.getElementById('actionForm');
const message = document.getElementById('message');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  message.textContent = 'Performing action...';

  try {
    const response = await fetch('/action', { method: 'POST' });
    const data = await response.json();

    if (response.ok) {
      message.textContent = data.message;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    message.textContent = `Error: ${error.message}`;
  }
});
