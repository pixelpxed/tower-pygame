from dataclasses import dataclass


@dataclass(frozen=True)
class Monster:
    name: str
    kind: str
    power: int
    item: str | None
    image: str = ""

    def __post_init__(self) -> None:
        if self.kind not in {"enemy", "boss"}:
            raise ValueError(f"Invalid enemy kind: {self.kind!r}")
        if type(self.power) is not int or self.power < 0:
            raise ValueError("Enemy power must be a non-negative integer")
        if self.item not in (None, "stick", "lightsaber"):
            raise ValueError(f"Invalid enemy item: {self.item!r}")
