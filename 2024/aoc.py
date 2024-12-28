from typing import Callable, Literal
import requests
import re
from enum import Enum, auto

AOC_COOKIE = open("session.cookie").read().strip()
YEAR = "2024"

example_re = re.compile(r"<pre><code>(.*?)</code></pre>", re.DOTALL)


class Response(Enum):
    SUCCESS = auto()
    WRONG = auto()
    TOO_HIGH = auto()
    TOO_LOW = auto()
    WAIT = auto()
    SOLVED = auto()


class AOCday:
    def __init__(self, day: int):
        self.day = day
        self.load_text()
        self.load_input()

    def load_input(self):
        req = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{self.day}/input",
            headers={"cookie": "session=" + AOC_COOKIE},
        )
        self.input = req.text.strip()
        with open(f"I_{self.day}.txt", "w") as f:
            f.write(self.input)

    def load_text(self):
        req = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{self.day}",
            headers={"cookie": "session=" + AOC_COOKIE},
        )
        self.text = req.text
        with open(f"Q_{self.day}.txt", "w") as f:
            f.write(self.question)

    @property
    def question(self) -> str:
        parts = self.text.split('<article class="day-desc">')
        q = parts[1].split("</article>")[0]
        if len(parts) > 2:
            q += parts[2].split("</article>")[0]
        return q

    @property
    def examples(self) -> list[str]:
        examples = example_re.findall(self.text)
        for i, example in enumerate(examples):
            # Replace HTML entities
            examples[i] = example.replace("&lt;", '<').replace("&gt;", '>')
            examples[i] = examples[i].replace("<em>", "").replace("</em>", "")
        return examples

    def submit(self, level: Literal[1, 2], answer: int) -> Response:
        data = {"level": str(level), "answer": str(answer)}

        response = requests.post(
            f"https://adventofcode.com/{YEAR}/day/{self.day}/answer",
            headers={"cookie": "session=" + AOC_COOKIE},
            data=data,
        )

        if "You gave an answer too recently" in response.text:
            return Response.WAIT
        elif "not the right answer" in response.text:
            if "too low" in response.text:
                return Response.TOO_LOW
            elif "too high" in response.text:
                return Response.TOO_HIGH
            else:
                return Response.WRONG
        elif "seem to be solving the right level." in response.text:
            return Response.SOLVED
        else:
            return Response.SUCCESS

    def run(self, solver: Callable[[str], int]) -> int:
        return solver(self.input)

    def test(self, solver: Callable[[str], int]) -> None:
        for i, example in enumerate(self.examples):
            print(f"Example {i + 1}:")
            print(f"Input:\n{example}")
            print(f"Output: {solver(example)}")
            print()
