let profileCart = document.querySelector(".profile-cart");
let profileImage = document.querySelector(".profile-img");
let clickToCreatePost = document.querySelector(".click-to-create-post");
let createPost = document.querySelector(".create-post");
let createPostClickOutside = document.querySelector(".create-post-click-outside");
let selectImage = document.querySelector(".select-image");
let selectImageImg = document.querySelector(".select-image .img");
let selectImageInput = document.querySelector("#select-image-input");
let selectedImage = document.querySelector(".selected-image");

window.addEventListener("scroll", function () {
    profileCart.classList.remove("cart-show")
    profileCart.style.transform = "scale(0)";
    profileCart.style.transition = "transform 0.2s";
})
selectImageInput.addEventListener("change", function () {
    selectImageImg.style.display = "none";
    selectedImage.style.display = "block";
     let reader = new FileReader();
    reader.readAsDataURL(selectImageInput.files[0]);
    reader.onload = () => { 
         selectedImage.setAttribute("src", reader.result);
    }
})

selectImage.addEventListener("click", function () {
    selectImageInput.click();
})
clickToCreatePost.addEventListener("click", function () {
    createPost.style.display = "flex";
    createPostClickOutside.style.display = "block";
    profileCart.classList.remove("cart-show")
    profileCart.style.transform = "scale(0)";
    profileCart.style.transition = "transform 0.2s";
})
createPostClickOutside.addEventListener("click", function () {
    createPost.style.display = "none";
    createPostClickOutside.style.display = "none";
})
profileImage.addEventListener("click", function () {
    profileCart.classList.toggle("cart-show");
    if (profileCart.classList.contains("cart-show")) {
        profileCart.style.transform = "scale(1)";
        profileCart.style.transition = "transform 0.5s";
    } else {
        profileCart.style.transform = "scale(0)";
        profileCart.style.transition = "transform 0.5s";
    }
})
