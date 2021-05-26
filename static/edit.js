window.addEventListener('load', () => {
    const title = localStorage.getItem('title');
    const description = localStorage.getItem('description');
    const profile_image_name = localStorage.getItem('profile_image_name');

    document.getElementById("result-title").innerHTML = title;
    document.getElementById("result-description").innerHTML = description;
    document.getElementById("result-profile_image_name").innerHTML = profile_image_name;
})