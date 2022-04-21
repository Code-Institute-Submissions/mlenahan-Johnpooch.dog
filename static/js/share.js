const shareBtn = document.getElementById('shareBtn')
const url = window.location.href;

shareBtn.addEventListener('click', event => {
    const queryString = window.location.search;
  // Check for Web Share api support
  if (navigator.share) {
    // Browser supports native share api
    navigator.share({
      text: 'Please read this great article: ',
      url: url
    }).then(() => {
      console.log('Thanks for sharing!');
    })
      .catch((err) => console.error(err));
  } else {
    // Fallback
    alert("The current browser does not support the share function. Please, manually share the link")
  }
});