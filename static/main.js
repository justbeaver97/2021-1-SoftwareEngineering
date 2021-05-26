function handleSubmit() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const profile_image_name = document.getElementById('profile_image_name').value;

    localStorage.setItem("title",title);
    localStorage.setItem("description",description);
    localStorage.setItem("profile_image_name",profile_image_name);

    return;
}