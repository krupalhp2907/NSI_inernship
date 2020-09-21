const wordEl = document.getElementById('word');
const wrongLettersEl = document.getElementById('wrong-letters');
const playAgainBtn = document.getElementById('play-button');
const popup = document.getElementById('popup-container');
const notification = document.getElementById('notification-container');
const finalMessage = document.getElementById('final-message');
const finalMessageRevealWord = document.getElementById('final-message-reveal-word');
const gameStatusEl = document.getElementById("game_status");

gameStatusEl.value = "playing";

const hangmanEl = document.getElementById("hangman");
var hangman = new HangmanSvg(hangmanEl);


// Use these words for your application
const words = ['application', 'programming', 'interface', 'wizard', 'frizar'];
var COUNT = 0;
var total = words.length;

let selectedWord = words[nextGame(COUNT, total)];

let playable = true;

const correctLetters = [];
const wrongLetters = [];

// Show hidden word
function displayWord() {
    wordEl.innerHTML = `
    ${selectedWord
            .split('')
            .map(
                letter => `
          <span class="letter">
            ${correctLetters.includes(letter) ? letter : ''}
          </span>
        `
            )
            .join('')}
  `;

    const innerWord = wordEl.innerText.replace(/[ \n]/g, '');

    if (innerWord === selectedWord) {
        finalMessage.innerText = 'Congratulations! You won! 😃';
        popup.style.display = 'flex';
        gameStatusEl.value = "win";

        playable = false;
    }
}

// Update the wrong letters
function updateWrongLettersEl() {
    // Display wrong letters
    wrongLettersEl.innerHTML = `
    ${wrongLetters.length > 0 ? '<p>Wrong</p>' : ''}
    ${wrongLetters.map(letter => `<span class="wrong-letter">${letter}</span>`)}
  `;

    let parts = hangman.draw();

    // Check if lost
    if (parts < 0) {
        finalMessage.innerText = 'Unfortunately you lost. 😕';
        finalMessageRevealWord.innerText = `...the word was: ${selectedWord}`;
        popup.style.display = 'flex';
        gameStatusEl.value = "lose";
        playable = false;
    }
}

// Show notification
function showNotification() {
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 2000);
}

// Keydown letter press
window.addEventListener('keydown', e => {
    if (playable) {
        if (e.keyCode >= 65 && e.keyCode <= 90) {
            const letter = e.key.toLowerCase();

            if (selectedWord.includes(letter)) {
                if (!correctLetters.includes(letter)) {
                    correctLetters.push(letter);

                    displayWord();
                } else {
                    showNotification();
                }
            } else {
                if (!wrongLetters.includes(letter)) {
                    wrongLetters.push(letter);

                    updateWrongLettersEl();
                } else {
                    showNotification();
                }
            }
        }
    }
});

// Restart game and play again
playAgainBtn.addEventListener('click', () => {
    playable = true;

    //  Empty arrays
    correctLetters.splice(0);
    wrongLetters.splice(0);

    COUNT += 1
    selectedWord = words[nextGame(COUNT, total)];



    hangmanEl.innerHTML = "";
    hangman.reset();
    displayWord();

    wrongLettersEl.innerHTML = "";

    gameStatusEl.value = "playing";

    popup.style.display = 'none';
});

displayWord();
