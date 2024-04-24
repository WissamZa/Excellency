function myconfirm() {
    if (confirm('Are You sure you want to delete?')) {
        document.getElementById("delete").click();
    } else {
        return false;
    }
}
var submitForms = function () {
    document.getElementById("get_form").submit();
    document.getElementById("post_form").submit();
}

var check = function () {
    if (document.getElementById('password').value ==
        document.getElementById('confirm_password').value) {
        document.getElementById('message').style.color = 'green';
        document.getElementById('message').innerHTML = 'متطابقة';
    } else {
        document.getElementById('message').style.color = 'red';
        document.getElementById('message').innerHTML = 'غير متطابقة';
    }
}

var product_img = document.querySelector('.product-img img');
var product_thumbnail = document.querySelectorAll('.product-thumbnail');

product_thumbnail.forEach((product) => {
    product.addEventListener('click', () => {
        product_thumbnail.forEach((product) => {
            product.classList.remove('active');
        });
        product.classList.add('active');

        let img = product.querySelector('img').getAttribute('src');
        let index = product.querySelector('img').getAttribute('data-index');

        product_img.setAttribute('src', img);
        product_img.setAttribute('data-index', index);

        product_img.classList.add('product-down-animation');
        setTimeout(() => {
            product_img.classList.remove('product-down-animation');
        }, 500);
    });
});