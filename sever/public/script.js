import { initialLetters } from "./utils.js";

let letters = initialLetters;
const leftSection = document.querySelector(".section-left");
const rightSection = document.querySelector(".section-right");

const initKeyboardUI = (lettersSelected, update) => {
  if (leftSection.hasChildNodes() && update) {
    leftSection.innerHTML = "";
  }
  if (rightSection.hasChildNodes() && update) {
    rightSection.innerHTML = "";
  }
  if (lettersSelected.length === 1) {
    const outputElement = document.querySelector(".output");
    if (lettersSelected[0] === "Delete") {
      outputElement.value = outputElement.value.slice(0, -1);
    } else if (lettersSelected[0] === "space") {
      outputElement.value += " ";
    } else if (lettersSelected[0] === "Enter") {
      outputElement.value = `${outputElement.value}\n`;
    } else {
      outputElement.value += lettersSelected[0];
    }

    initKeyboardUI(initialLetters, false);
    letterPrinted();
    return;
  } else {
    lettersSelected.map((letter, i) => {
      const letterElement = document.createElement("p");
      letterElement.innerHTML = letter;
      if (i < Math.round(lettersSelected.length / 2)) {
        leftSection.appendChild(letterElement);
      } else {
        rightSection.appendChild(letterElement);
      }
    });
  }
};

initKeyboardUI(letters, false);

const letterPrinted = () => (letters = initialLetters);
