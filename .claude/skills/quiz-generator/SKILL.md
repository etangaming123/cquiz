---
name: quiz-generator
description: Generate new cquiz JSON quiz files (personality/"which character are you" quizzes) for the cquiz project. Use when asked to create, write, or generate a new quiz, or add characters/questions to the quizzes/ directory.
---
# Quiz Generator

Build a valid `quizzes/*.json` file for this project. Read `quiz_engine/models.py` first if unsure of exact field names - this file must match `Quiz.from_dict` exactly.

## Step 1: Ask for characters (if not given)

If user hasn't named a source/theme and character list yet, ask now. Need:

- Theme/source (show, game, archetype set, original characters, etc.)
- List of characters to include (name each, minimum 2 - 4-8 is a good range)
- Optional: desired number of questions (default 8-12), tone/style

Don't guess a fandom's characters from memory if accuracy matters - ask user to confirm or list them.

## Step 2: Design attributes

Pick 4-8 short trait words (lowercase, one word or short phrase, e.g. `bravery`, `wit`, `loyalty`) that meaningfully **distinguish** the given characters from each other. Bad attribute: one every character scores the same on. Good attribute: splits the cast into clear highs and lows.

## Step 3: Build character profiles

For each character, assign a point 0-5 per attribute (`profile` dict). Rules:

- Every character needs a distinct profile — no two characters identical across all attributes.
- Every attribute must have meaningful variance across characters (not all 5s or all 0s).
- Omit an attribute from a profile only if it's genuinely 0 for that character (matches model default).

## Step 4: Write questions

Write 8-12 questions, each with 3-5 answer choices. Rules:

- Each choice's `points` dict awards 1-3 attributes, values 1-3 (keep smaller than profile scale so no single question dominates the result).
- Across all questions combined, every attribute must be awarded by multiple choices — an attribute that never appears in any choice can never be scored, making it dead weight.
- Vary which attribute-combinations choices hit — don't make every choice a single-attribute dump.
- Question and choice text should fit the theme/tone requested.

## Step 5: Assemble and save JSON

Exact schema (see `quiz_engine/models.py` / README "Option B"):

```json
{
  "title": "Quiz Title",
  "description": "One-line description shown before the quiz starts.",
  "attributes": ["attr1", "attr2"],
  "characters": [
    {
      "id": "unique_slug",
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

- `id`: lowercase slug, unique, no spaces (use underscores).
- Filename: `snake_case` derived from title, saved under `quizzes/` (e.g. `quizzes/my_quiz_title.json`).
- Look at an existing file in `quizzes/` (e.g. `dere_types.json`) for a concrete reference before writing.

## Step 6: Validate before finishing

Check, and fix if failed:

- Valid JSON (no trailing commas, matching brackets).
- At least 2 characters, every question has at least 2 choices.
- Every attribute in `attributes` appears in at least one character profile AND at least one choice.
- No duplicate character `id`s.
- Every character has at least one question/choice combo where they'd plausibly score highest (skim profiles vs. choice point distributions).

Optionally verify by running:

```
python -c "from quiz_engine.loader import load_quiz; load_quiz('quizzes/YOUR_FILE.json')"
```

from the project root - this calls `Quiz.from_dict` and will raise on schema errors.

Tell the user the quiz is ready and it'll appear in the "Take a quiz" menu right away.
