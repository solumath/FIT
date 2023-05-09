document.addEventListener('DOMContentLoaded', function() {
    //sticky navbar and arrow up when scrolling
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 140) {
            document.documentElement.classList.add("scrolled");
        } else {
            document.documentElement.classList.remove("scrolled");
        }
    });
    
    // mobile menu to open and close when one of the options is clicked
    var coll = document.getElementsByClassName("collapsible");
    var menu = document.getElementById("menu-toggle");
    var menulist = document.getElementById("menu");
    console.log(coll);
    console.log(menu);
    
    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            for (j = 0; j < coll.length; j++) {
                coll[j].classList.toggle("active");
            }
            menu.classList.toggle("active");
            menulist.classList.toggle("active");
        });
    }
});