"""Persistência substituível para CRM e avaliações."""

import json
from abc import ABC, abstractmethod
from pathlib import Path


class ReviewRepository(ABC):
    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def save(self, data):
        raise NotImplementedError


class JsonRepository(ReviewRepository):
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return {"vendas": [], "avaliacoes": []}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.path)
