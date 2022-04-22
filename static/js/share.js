const shareBtn = document.getElementById('shareBtn');
const url = window.location.href;

shareBtn.addEventListener('click', event => {
  if (navigator.share) {
    navigator.share({
      text: 'Please read this great article: ',
      url: url
    }).then(() => {
      console.log('Thanks for sharing!');
    })
      .catch((err) => console.error(err));
  } else {
    alert("The current browser does not support the share function. Please, manually share the link");
  }
});