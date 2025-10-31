import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Global score variable
score = 0

# Word list with hints
words_with_hints = {
    'breeze': 'A light and gentle wind 🌬️',
    'canvas': 'Used by painters to create art 🎨',
    'crystal': 'A shiny, transparent mineral 💎',
    'elegant': 'Graceful and stylish ✨',
    'meadow': 'A field full of grass and flowers 🌼',
    'twilight': 'Time between sunset and darkness 🌆',
    'guitar': 'A string instrument 🎸',
    'shadow': 'It follows you but isn’t alive 🕶️',
    'island': 'Land surrounded by water 🏝️',
    'whisper': 'A soft spoken word or sound 🤫',
    'abyss': 'a deep chasm',
    'epiphany': 'A sudden realization'

}

# Hangman stages (ASCII Art)
stages = [
    """
     _______
    |/      |
    |
    |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |       |
    |       |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|
    |       |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |      /
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |      / \\
    |___
    """
]

# Function to choose a word and its hint
def choose_word_and_hint():
    word = random.choice(list(words_with_hints.keys()))
    hint = words_with_hints[word]
    return word, hint

# Function to display the word with guessed letters
def display(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

# Main game function
def hangman():
    global score

    print(Fore.CYAN + Style.BRIGHT + "\n🎯 Welcome to Minimal Hangman 🎯\n")

    word, hint = choose_word_and_hint()
    guessed_letters = []
    tries = 0
    max_tries = len(stages) - 1

    print(Fore.LIGHTMAGENTA_EX + f"💡 Hint: {hint}")

    while tries < max_tries:
        print(Fore.YELLOW + stages[tries])
        print("\nWord: ", Fore.GREEN + display(word, guessed_letters))
        print(Fore.LIGHTWHITE_EX + f"🏅 Score: {score}")
        guess = input(Fore.BLUE + "\nGuess a letter: ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print(Fore.RED + "Please enter a single valid letter.")
            continue

        if guess in guessed_letters:
            print(Fore.MAGENTA + "You've already guessed that letter!")
            continue

        guessed_letters.append(guess)

        if guess in word:
            print(Fore.GREEN + "Good guess!")
            score += 10
            if all(letter in guessed_letters for letter in word):
                score += 50
                print(Fore.CYAN + "\n🎉 You won! The word was:", word)
                print(Fore.GREEN + f"🏆 Final Score: {score}")
                break
        else:
            print(Fore.RED + "Wrong guess!")
            score -= 5
            tries += 1
    else:
        score -= 20
        print(Fore.RED + stages[tries])
        print(Fore.RED + "\n💀 Game Over! The word was:", word)
        print(Fore.YELLOW + f"🎯 Final Score: {score}")

    print(Fore.CYAN + Style.BRIGHT + "\nThanks for playing Hangman 🤍\n")

# Run the game
if __name__ == "__main__":
    hangman()
