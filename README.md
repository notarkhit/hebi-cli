# hebi-cli

The main control script for the Hebi dotfiles.

<details><summary id="dependencies">External dependencies</summary>

- [`libnotfy`](https://gitlab.gnome.org/GNOME/libnotify) - sending notifications
- [`swappy`](https://github.com/jtheoof/swappy) - screenshot editor
- [`grim`](https://gitlab.freedesktop.org/emersion/grim) - taking screenshots
- [`dart-sass`](https://github.com/sass/dart-sass) - discord theming
- [`app2unit`](https://github.com/Vladimir-csp/app2unit) - launching apps
- [`wl-clipboard`](https://github.com/bugaevc/wl-clipboard) - copying to clipboard
- [`slurp`](https://github.com/emersion/slurp) - selecting an area
- [`gpu-screen-recorder`](https://git.dec05eba.com/gpu-screen-recorder/about) - screen recording
- `glib2` - closing notifications
- [`cliphist`](https://github.com/sentriz/cliphist) - clipboard history
- [`fuzzel`](https://codeberg.org/dnkl/fuzzel) - clipboard history/emoji picker

</details>

## Installation

The recommended way to install `hebi-cli` is via [`pipx`](https://pipx.pypa.io/). This ensures the CLI and its dependencies are isolated in their own virtual environment while still being globally available in your PATH.

### 1. Install dependencies
First, ensure you have all external [dependencies](#dependencies) installed, as well as `pipx`:

```sh
# Example for Arch Linux using yay:
yay -S libnotify swappy grim dart-sass app2unit wl-clipboard slurp gpu-screen-recorder glib2 cliphist fuzzel python-pipx
```

### 2. Install the CLI using pipx
You can install `hebi-cli` directly from GitHub using `pipx`:

```sh
pipx install git+https://github.com/notarkhit/hebi-cli.git
```

Once installed, the `hebi` command will be available in your terminal!

> [!TIP]
> To update the CLI in the future, simply run:
> `pipx upgrade hebi`

### Additional steps

#### Auto folder colour theming

For automatic Papirus folder icon colour syncing, you must have [`papirus-folders`](https://github.com/PapirusDevelopmentTeam/papirus-folders)
installed, and `papirus-folders` must to be able to run with `sudo` without a password prompt.

You can allow this by creating a sudoers file:

```sh
echo "$USER ALL=(ALL) NOPASSWD: $(which papirus-folders)" | sudo tee /etc/sudoers.d/papirus-folders
sudo chmod 440 /etc/sudoers.d/papirus-folders
```


## Usage

All subcommands/options can be explored via the help flag.

```
$ hebi -h
usage: hebi [-h] [-v] COMMAND ...

Main control script for the Hebi dotfiles

options:
  -h, --help     show this help message and exit
  -v, --version  print the current version

subcommands:
  valid subcommands

  COMMAND        the subcommand to run
    shell        start or message the shell
    toggle       toggle a special workspace
    scheme       manage the colour scheme
    screenshot   take a screenshot
    record       start a screen recording
    clipboard    open clipboard history
    emoji        emoji/glyph utilities
    wallpaper    manage the wallpaper
    resizer      window resizer daemon
```

### User templates

Custom user templates can be defined in `~/.config/hebi/templates/`.

#### Template syntax

`{{ <color>.<format> }}`

- `<color>` is a theme color role derived from the Material You color system (e.g. `primary`, `secondary`, `background`)
- `<format>` is the output format: `hex` or `rgb`

#### Examples

- `{{ primary.hex }}` outputs `3f4ba2`
- `{{ primary.rgb }}` outputs `rgb(193, 132, 207)`

Output files are written to `~/.local/state/hebi/theme/`. You can symlink them to your desired locations.

## Configuring

All configuration options are in `~/.config/hebi/cli.json`.

<details><summary>Example configuration</summary>

```json
{
    "record": {
        "extraArgs": []
    },
    "wallpaper": {
        "postHook": "echo $WALLPAPER_PATH $SCHEME_NAME $SCHEME_FLAVOUR $SCHEME_MODE $SCHEME_VARIANT $SCHEME_COLOURS"
    },
    "theme": {
        "enableTerm": true,
        "enableHypr": true,
        "enableDiscord": true,
        "enableSpicetify": true,
        "enablePandora": true,
        "enableFuzzel": true,
        "enableBtop": true,
        "enableNvtop": true,
        "enableHtop": true,
        "enableGtk": true,
        "enableQt": true,
        "enableWarp": true,
        "enableChromium": true,
        "enableZed": true,
        "enableCava": true,
        "iconTheme": "Papirus-Dark",
        "iconThemeLight": "Papirus-Light",
        "iconThemeDark": "Papirus-Dark",
        "postHook": "echo $SCHEME_NAME $SCHEME_FLAVOUR $SCHEME_MODE $SCHEME_VARIANT $SCHEME_COLOURS"
    },
    "toggles": {
        "communication": {
            "discord": {
                "enable": true,
                "match": [{ "class": "discord" }],
                "command": ["discord"],
                "move": true
            },
            "whatsapp": {
                "enable": true,
                "match": [{ "class": "whatsapp" }],
                "move": true
            }
        },
        "music": {
            "spotify": {
                "enable": true,
                "match": [{ "class": "Spotify" }, { "initialTitle": "Spotify" }, { "initialTitle": "Spotify Free" }],
                "command": ["spicetify", "watch", "-s"],
                "move": true
            },
            "feishin": {
                "enable": true,
                "match": [{ "class": "feishin" }],
                "move": true
            }
        },
        "sysmon": {
            "btop": {
                "enable": true,
                "match": [{ "class": "btop", "title": "btop", "workspace": { "name": "special:sysmon" } }],
                "command": ["foot", "-a", "btop", "-T", "btop", "fish", "-C", "exec btop"]
            }
        },
        "todo": {
            "todoist": {
                "enable": true,
                "match": [{ "class": "Todoist" }],
                "command": ["todoist"],
                "move": true
            }
        }
    }
}
```

</details>
