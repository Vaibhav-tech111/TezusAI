const text = document.querySelector('.tezus-text');
const phrases = ["Tezus is listening...", "Thinking...", "Generating response...", "Ready for your command"];
let index = 0;

setInterval(() => {
  text.textContent = phrases[index];
  index = (index + 1) % phrases.length;
}, 4000);
