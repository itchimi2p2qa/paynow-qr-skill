# PayNow QR skill

<img width="292" height="292" alt="image" src="https://github.com/user-attachments/assets/fc7c5743-57aa-4a16-8d79-17075b245841" />

Local Singapore PayNow QR generator for Grok, Claude, and other agents. No API key.

This repository *is* the skill. `SKILL.md` is at the repo root.

Repo: https://github.com/itchimi2p2qa/paynow-qr-skill

## Point an AI at this repo

Paste one of these to Grok, Claude Code, Codex, or Cursor:

```
Install the PayNow QR skill from https://github.com/itchimi2p2qa/paynow-qr-skill
```

```
npx skills add itchimi2p2qa/paynow-qr-skill
```

```
git clone https://github.com/itchimi2p2qa/paynow-qr-skill.git ~/.claude/skills/paynow-qr
```

Then, once, set the installer's own mobile:

```
python3 scripts/setup_payee.py --mobile +65XXXXXXXX
pip install segno pillow
```

Claude.ai website skills are account settings. A chat cannot write them. There you still do:
Settings → Capabilities → Skills → Upload skill →
https://github.com/itchimi2p2qa/paynow-qr-skill/archive/refs/heads/main.zip

A folder named `paynow-qr-skill-main` is fine if `SKILL.md` is inside it.

## What it does

- Builds the EMVCo / SGQR payload on the machine
- CRC-16/CCITT-FALSE (`123456789` → `29B1`)
- Mobile, UEN, open amount, bill reference, favorites
- Optional center sticker from `assets/icons/`
- Confirms encoded details before showing the image

PayNow transfers are effectively irreversible. The receiving bank shows the registered account name on scan.

## Center stickers

73 bundled Twemoji icons. Say the name in chat (`put a burger on it`) or pass `--icon burger`.

Default is no sticker (`none` or `paynow`) so the QR stays easiest to scan. If a bank app struggles with a sticker, regenerate without one.

### Drinking

<img src="assets/icons/beer.png" width="40" alt="beer"> `beer`
<img src="assets/icons/cheers.png" width="40" alt="cheers"> `cheers`
<img src="assets/icons/wine.png" width="40" alt="wine"> `wine`
<img src="assets/icons/cocktail.png" width="40" alt="cocktail"> `cocktail`
<img src="assets/icons/tropical.png" width="40" alt="tropical"> `tropical`
<img src="assets/icons/champagne.png" width="40" alt="champagne"> `champagne`
<img src="assets/icons/whisky.png" width="40" alt="whisky"> `whisky`
<img src="assets/icons/sake.png" width="40" alt="sake"> `sake`
<img src="assets/icons/boba.png" width="40" alt="boba"> `boba`
<img src="assets/icons/coffee.png" width="40" alt="coffee"> `coffee`
<img src="assets/icons/tea.png" width="40" alt="tea"> `tea`

### Food

<img src="assets/icons/pizza.png" width="40" alt="pizza"> `pizza`
<img src="assets/icons/burger.png" width="40" alt="burger"> `burger`
<img src="assets/icons/fries.png" width="40" alt="fries"> `fries`
<img src="assets/icons/taco.png" width="40" alt="taco"> `taco`
<img src="assets/icons/sushi.png" width="40" alt="sushi"> `sushi`
<img src="assets/icons/ramen.png" width="40" alt="ramen"> `ramen`
<img src="assets/icons/hotpot.png" width="40" alt="hotpot"> `hotpot`
<img src="assets/icons/chickenwing.png" width="40" alt="chickenwing"> `chickenwing`
<img src="assets/icons/steak.png" width="40" alt="steak"> `steak`
<img src="assets/icons/curry.png" width="40" alt="curry"> `curry`
<img src="assets/icons/icecream.png" width="40" alt="icecream"> `icecream`
<img src="assets/icons/donut.png" width="40" alt="donut"> `donut`
<img src="assets/icons/cake.png" width="40" alt="cake"> `cake`
<img src="assets/icons/chocolate.png" width="40" alt="chocolate"> `chocolate`
<img src="assets/icons/banana.png" width="40" alt="banana"> `banana`

### Travel

<img src="assets/icons/plane.png" width="40" alt="plane"> `plane`
<img src="assets/icons/island.png" width="40" alt="island"> `island`
<img src="assets/icons/beach.png" width="40" alt="beach"> `beach`
<img src="assets/icons/luggage.png" width="40" alt="luggage"> `luggage`
<img src="assets/icons/taxi.png" width="40" alt="taxi"> `taxi`
<img src="assets/icons/train.png" width="40" alt="train"> `train`
<img src="assets/icons/ship.png" width="40" alt="ship"> `ship`
<img src="assets/icons/hotel.png" width="40" alt="hotel"> `hotel`
<img src="assets/icons/map.png" width="40" alt="map"> `map`
<img src="assets/icons/ticket.png" width="40" alt="ticket"> `ticket`
<img src="assets/icons/mountain.png" width="40" alt="mountain"> `mountain`
<img src="assets/icons/sunset.png" width="40" alt="sunset"> `sunset`

### Dance

<img src="assets/icons/dancer.png" width="40" alt="dancer"> `dancer`
<img src="assets/icons/groove.png" width="40" alt="groove"> `groove`
<img src="assets/icons/ballet.png" width="40" alt="ballet"> `ballet`
<img src="assets/icons/disco.png" width="40" alt="disco"> `disco`
<img src="assets/icons/party.png" width="40" alt="party"> `party`
<img src="assets/icons/confetti.png" width="40" alt="confetti"> `confetti`

### Entertainment

<img src="assets/icons/clapper.png" width="40" alt="clapper"> `clapper`
<img src="assets/icons/popcorn.png" width="40" alt="popcorn"> `popcorn`
<img src="assets/icons/mic.png" width="40" alt="mic"> `mic`
<img src="assets/icons/headphones.png" width="40" alt="headphones"> `headphones`
<img src="assets/icons/notes.png" width="40" alt="notes"> `notes`
<img src="assets/icons/game.png" width="40" alt="game"> `game`
<img src="assets/icons/joystick.png" width="40" alt="joystick"> `joystick`
<img src="assets/icons/slots.png" width="40" alt="slots"> `slots`
<img src="assets/icons/masks.png" width="40" alt="masks"> `masks`
<img src="assets/icons/magic.png" width="40" alt="magic"> `magic`
<img src="assets/icons/circus.png" width="40" alt="circus"> `circus`
<img src="assets/icons/darts.png" width="40" alt="darts"> `darts`

### Memes

<img src="assets/icons/joy.png" width="40" alt="joy"> `joy`
<img src="assets/icons/moai.png" width="40" alt="moai"> `moai`
<img src="assets/icons/skull.png" width="40" alt="skull"> `skull`
<img src="assets/icons/clown.png" width="40" alt="clown"> `clown`
<img src="assets/icons/frog.png" width="40" alt="frog"> `frog`
<img src="assets/icons/duck.png" width="40" alt="duck"> `duck`
<img src="assets/icons/chicken.png" width="40" alt="chicken"> `chicken`
<img src="assets/icons/cat.png" width="40" alt="cat"> `cat`
<img src="assets/icons/dog.png" width="40" alt="dog"> `dog`
<img src="assets/icons/cool.png" width="40" alt="cool"> `cool`
<img src="assets/icons/nerd.png" width="40" alt="nerd"> `nerd`
<img src="assets/icons/alien.png" width="40" alt="alien"> `alien`
<img src="assets/icons/fire.png" width="40" alt="fire"> `fire`
<img src="assets/icons/poop.png" width="40" alt="poop"> `poop`
<img src="assets/icons/goat.png" width="40" alt="goat"> `goat`
<img src="assets/icons/melt.png" width="40" alt="melt"> `melt`
<img src="assets/icons/peek.png" width="40" alt="peek"> `peek`

Twemoji stickers are CC-BY 4.0 Twitter, Inc.

## License

MIT
