# etan's character quiz

A simple Python program for "which character are you" personality quizzes. Answer multiple-choice questions, and the app tells you how closely you match *each* character, as a percentage.

> [!NOTE]
> Percentages don't add up to 100% because the percentage is based on how close you are to that character. 
> Because of how some quizzes are made, 100% may not be possible.

## Running it

### Prerequisites

You will need:

- Python
- A terminal (windows command prompt, macos terminal, etc.)
- A keyboard to input your choices
- A positive attitude :^)

### (actually) running it

```
python main.py
```

You'll get a menu:

1. **Take a quiz** — pick one of the quizzes in `quizzes/` by title, answer each question (type `undo` instead of a number to go back and change your previous answer), get your results.
2. **Create a new quiz** — interactive wizard walks you through building your own quiz and saves it into `quizzes/`.
3. **Settings** — toggle app behavior (see below).
4. **Quit** - This one is self explanatory.

### Configuring some settings

Choose **3. Settings** from the main menu to toggle:

- **Word wrap** — wrap question/answer/result text to your current terminal width (re-measured every time you start a quiz).
- **Shuffle question order** — ask the quiz's questions in random order each time.
- **Shuffle answer choice order** — randomize each question's choice order each time.
- **Show points added to each attribute after answering** — after each answer, show the attribute points that choice just added (e.g. `(+3 bravery, +1 ambition)`).
- **Show current closest character after each question** — after each answer, print your current leading character and its running match %.
- **Typewriter animation for quiz question text** — the title/description show instantly and wait for Enter before the quiz starts; each question types out letter by letter, each answer choice appears one line at a time. Also animates results.

Toggling a setting saves immediately to `settings.json` in the project root.

## Making your own quiz

### Option A: the builder (recommended)

Run `python main.py`, choose **2. Create a new quiz**, and answer the
prompts:

1. Title and description.
2. The list of attributes, comma-separated (e.g. `bravery, wit, kindness`).
3. Each character: id, name, description, then a point value per attribute (0–5 is a reasonable scale, blank = 0).
4. Each question: the question text, then each answer choice's text and its point value per attribute (blank = 0). Add as many questions and choices as you like.
5. A filename to save under `quizzes/`.

The new quiz appears in the "Take a quiz" list right away.

### Option B: hand-write the JSON

Quizzes are plain JSON files in `quizzes/`. Schema:

```json
{
  "title": "Quiz Title",
  "description": "One-line description shown before the quiz starts.",
  "attributes": ["attr1", "attr2"],
  "characters": [
    {
      "id": "unique_id",
      "name": "Display Name",
      "description": "Shown when this character is your top match.",
      "profile": {"attr1": 5, "attr2": 2}
    }
  ],
  "questions": [
    {
      "text": "Question text?",
      "choices": [
        {"text": "Choice A", "points": {"attr1": 3}},
        {"text": "Choice B", "points": {"attr2": 3}}
      ]
    }
  ]
}
```

Notes:

- Any attribute left out of a `profile` or `points` dict is treated as `0`.
- Every question should have at least 2 choices, and every quiz at least 2 characters, for a meaningful result.
- `quiz_engine/models.py` has the `Quiz.from_dict` / `to_dict` logic if you want to load or generate quizzes programmatically instead.

### Option C: have an AI agent generate it

Point an AI coding agent (Claude Code, etc.) at this repo and tell it what quiz you want - it'll ask you for the characters, then write the JSON file into `quizzes/` for you.

This repo ships a skill for it at `.claude/skills/quiz-generator/SKILL.md`, which walks the agent through picking distinguishing attributes, scoring characters, writing balanced questions, and validating the result against the schema above.

## Importing quizzes

Got a quiz.json file? That's great! Just pop it in the `quizzes/`folder and run the program, it'll show and be available.

## Under the hood

### Project layout

```
cquiz/
  main.py                   # run this — CLI menu
  quiz_engine/
    models.py                # Quiz / Question / Choice / Character data model
    loader.py                # find/load/save quiz JSON files
    runner.py                # ask questions, score answers, print results
    builder.py                # interactive "make your own quiz" wizard
    settings.py               # Settings dataclass + load/save to settings.json
    settings_menu.py          # interactive settings toggle screen
  quizzes/
    anime_archetypes.json     # example quiz
    sitcom_friends.json       # example quiz
  settings.json                # user settings (gitignored, created on first change)
```

### How scoring works

1. A quiz defines a list of **attributes** (personality traits), e.g. `["bravery", "wit", "kindness", "ambition"]`.
2. Each **character** has a **profile**: a point value per attribute, describing what that character is like.
3. Each question's answer **choices** award points on one or more attributes (not directly to a character).
4. As you answer, your points per attribute add up into your own vector.
5. At the end, your vector is compared to every character's profile using cosine similarity, scaled to 0–100%. Results are printed ranked highest to lowest, with the top match called out (and any close runner-up noted). Only the top 10 characters are shown in the results bar chart.

## License

This project is licensed under the [MIT License](./LICENSE).
