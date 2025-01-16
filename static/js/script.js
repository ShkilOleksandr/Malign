document.addEventListener('DOMContentLoaded', () => {
    const footer = document.getElementById('dynamic-footer');
    const imageUrl = 'https://picsum.photos/300/200';

    // Fetch the image
    fetch(imageUrl)
        .then(response => {
            if (response.ok) {
                return imageUrl;
            }
            throw new Error('Failed to fetch image');
        })
        .then(imageUrl => {
            footer.style.backgroundImage = `url(${imageUrl})`;
        })
        .catch(error => {
            console.error('Error fetching the image:', error);
            footer.textContent = 'Failed to load background image.';
        });
});
