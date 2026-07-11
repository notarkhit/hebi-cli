import json
import subprocess
from argparse import Namespace
from urllib.request import urlopen

from hebi.utils.paths import cli_data_dir


class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        data_file = "nerdfonts.txt" if getattr(self.args, "nerdfont", False) else "emojis.txt"
        if self.args.picker:
            mode = '"::"' if getattr(self.args, "nerdfont", False) else '":"'
            subprocess.run(["hebi", "shell", "launcher", "openMode", mode])
        elif self.args.fetch:
            self.fetch_emojis()
        else:
            print((cli_data_dir / data_file).read_text(), end="")

    def fetch_emojis(self) -> None:
        data = []

        # Fetch emojis
        with urlopen(
            "https://raw.githubusercontent.com/milesj/emojibase/refs/heads/master/packages/data/en/data.raw.json"
        ) as f:
            emojis = json.load(f)
        emojis.sort(key=lambda x: x.get("order", 999999))

        for emoji in emojis:
            line = [emoji["unicode"]]

            if "emoticon" in emoji:
                if isinstance(emoji["emoticon"], str):
                    line.append(emoji["emoticon"])
                else:
                    line.extend(emoji["emoticon"])

            line.append(emoji["label"])

            if "tags" in emoji:
                line.extend(emoji["tags"])

            data.append(" ".join(line))

        nerdfont_data = []
        # Fetch nerd font glyphs
        with urlopen("https://raw.githubusercontent.com/ryanoasis/nerd-fonts/refs/heads/master/glyphnames.json") as f:
            glyphs = json.load(f)

        buckets = {}
        for name, glyph in glyphs.items():
            if name == "METADATA":
                continue

            unicode = glyph["char"]
            if unicode not in buckets:
                buckets[unicode] = []
            buckets[unicode].append(f"nf-{name}")

        for glyph, names in buckets.items():
            nerdfont_data.append(f"{glyph}  {' '.join(names)}")

        # Write to file
        (cli_data_dir / "emojis.txt").write_text("\n".join(data))
        (cli_data_dir / "nerdfonts.txt").write_text("\n".join(nerdfont_data))
