const home = document.getElementById('home');
const ico = document.getElementById("ico");
const script = document.getElementById('scripts')
const ico2 = document.getElementById("ico")

if (window.location.toString().includes("script")) {
  if (script && ico2) {
    script.classList.add('nav-active')
    ico.classList.add('ico-active')
  } else {
    console.error('falsy')
  }
} else {
  home.classList.add('nav-active')
  ico.classList.add('ico-active')
}

document.querySelectorAll('div.code').forEach(el => {
  // then highlight each
  hljs.highlightElement(el);
});