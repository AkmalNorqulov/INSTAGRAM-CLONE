// INSTA-style continuous playback — IntersectionObserver


const videos = document.querySelectorAll('.reel-video');


const observer = new IntersectionObserver((entries) => {
entries.forEach(entry => {
const video = entry.target;
if (entry.isIntersecting) {
video.play();
} else {
video.pause();
}
});
}, { threshold: 0.8 }); // 80% ko‘ringanda play


videos.forEach(v => observer.observe(v));


// like buttons
for(const btn of document.querySelectorAll('.like-btn')){
btn.addEventListener('click', async function(event){
event.preventDefault();
const url = btn.dataset.url;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
const res = await fetch(url, {
method: 'POST',
headers: { 'X-CSRFToken': csrftoken, 'Accept': 'application/json' }
});
const data = await res.json();
btn.querySelector('.like-count').textContent = data.count;
});
}

