# Center icons

Default is no sticker (`none`) so the QR stays easiest to scan.

Pass `--icon burger` (or another id). The script paints a small color sticker on a white circle after encoding `qr_string`.

Keep stickers small. If a bank app fails, regenerate with `--icon none`.

## Ids

Logo — `none`, `paynow` (both mean no extra sticker)

Drinking — `beer`, `cheers`, `wine`, `cocktail`, `tropical`, `champagne`, `whisky`, `sake`, `boba`, `coffee`, `tea`

Food — `pizza`, `burger`, `fries`, `taco`, `sushi`, `ramen`, `hotpot`, `chickenwing`, `steak`, `curry`, `icecream`, `donut`, `cake`, `chocolate`, `banana`

Travel — `plane`, `island`, `beach`, `luggage`, `taxi`, `train`, `ship`, `hotel`, `map`, `ticket`, `mountain`, `sunset`

Dance — `dancer`, `groove`, `ballet`, `disco`, `party`, `confetti`

Entertainment — `clapper`, `popcorn`, `mic`, `headphones`, `notes`, `game`, `joystick`, `slots`, `masks`, `magic`, `circus`, `darts`

Memes — `joy`, `moai`, `skull`, `clown`, `frog`, `duck`, `chicken`, `cat`, `dog`, `cool`, `nerd`, `alien`, `fire`, `poop`, `goat`, `melt`, `peek`

## Mapping speech

- burger / hamburger → `burger`
- beer / beers / cheers → `beer` or `cheers`
- pizza night → `pizza`
- plane / flight / travel → `plane`
- karaoke → `mic`
- movie / film → `clapper`
- party / octoberfest vibe → `party` or `beer`
