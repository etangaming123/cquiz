from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Choice:
    text: str
    points: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"text": self.text, "points": self.points}

    @staticmethod
    def from_dict(data: dict) -> "Choice":
        return Choice(text=data["text"], points=dict(data.get("points", {})))


@dataclass
class Question:
    text: str
    choices: list[Choice]

    def to_dict(self) -> dict:
        return {"text": self.text, "choices": [c.to_dict() for c in self.choices]}

    @staticmethod
    def from_dict(data: dict) -> "Question":
        return Question(
            text=data["text"],
            choices=[Choice.from_dict(c) for c in data["choices"]],
        )


@dataclass
class Character:
    id: str
    name: str
    description: str
    profile: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "profile": self.profile,
        }

    @staticmethod
    def from_dict(data: dict) -> "Character":
        return Character(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            profile=dict(data.get("profile", {})),
        )


@dataclass
class Quiz:
    title: str
    description: str
    attributes: list[str]
    characters: list[Character]
    questions: list[Question]

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "attributes": self.attributes,
            "characters": [c.to_dict() for c in self.characters],
            "questions": [q.to_dict() for q in self.questions],
        }

    @staticmethod
    def from_dict(data: dict) -> "Quiz":
        return Quiz(
            title=data["title"],
            description=data.get("description", ""),
            attributes=list(data.get("attributes", [])),
            characters=[Character.from_dict(c) for c in data["characters"]],
            questions=[Question.from_dict(q) for q in data["questions"]],
        )
