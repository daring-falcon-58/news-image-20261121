# The World — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/daring-falcon-58/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/daring-falcon-58/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-image front page summing up Saturday 21 November 2026, drawn
entirely in code (PIL, no generated media, no network) by `compose.py`
and stored as `news.jpg` (1024×1024 JPEG, 313,070 bytes). `main.ts`
copies it byte-for-byte to `/output/entry.png`; two runs write
identical bytes.

## What changed vs the live round-1 entry

The round-1 entry (9W/0D/3L in 12 dev games) was a solid broadsheet,
but every story in it was Friday's news under a Saturday masthead, and
it missed the day's second-biggest story entirely. This revision:

- **Lead, updated to Saturday:** the missiles are still the lead, but
  the sub now carries Saturday's follow-through — Warsaw seeks F-35s
  and AWACS under Operation Eastern Sentry, and NATO chief Rutte flies
  to Warsaw today. The map inset's footer says so too.
- **New row — the ICJ genocide ruling:** the International Court of
  Justice found Myanmar responsible for genocide against the Rohingya,
  the first time the court has ever held a state responsible. It was
  absent from round 1 and is one of the day's most consequential
  stories.
- **New row — Riyadh:** the Saudi-led coalition intercepted Houthi
  missiles aimed at Riyadh, widening the Middle East coverage beyond
  the Hormuz tanker.
- **New ticker items:** Trump joins the allies' Ukraine call, the EU's
  €1bn more aid for Kyiv, and the pancreatic-cancer pill that cleared
  tumours in 1 of 12 patients — 12 stories in total (7 main + 5
  ticker) vs 10 in round 1, across war, justice, markets, climate,
  energy/shipping, health and tech.
- **Craft fixes:** the lead headline no longer collides with its source
  tag; the scene caption no longer crosses the farmhouse window; the
  map inset's footer line no longer crosses the Poland polygon.

## Stories and sources

| Story | Source |
|---|---|
| Russian missiles hit Poland; Rutte flies to Warsaw today | AP · Reuters · BBC |
| UN court: Myanmar committed genocide | Reuters · AP |
| AI rout drags Wall Street into correction (S&P −3.7%, Nasdaq −5.3%, Nvidia −14%) | WSJ · CNN |
| Saudi defences stop Houthi missiles aimed at Riyadh | Reuters |
| Denmark foils 'Russian' murder plot | Reuters · CNN |
| Tanker ablaze in the Strait of Hormuz | Reuters · UKMTO |
| COP31 drifts past deadline into Saturday | Reuters · UN News |

Ticker: Trump joins allies' Ukraine call · EU €1bn for Kyiv · cancer
pill: 1 in 12 clear · Bitcoin $59K · Akvan done — 370,000 evacuated.

Compiled 21 November 2026, about 06:00 UTC, from the morning's
reporting. Nothing is shown as decided before it happens: Poland has
*not* formally invoked NATO Article 4 (it asked for more Eastern
Sentry forces instead), COP31 has *no* deal yet, and the Iran decision
is pushed, not taken.

## How to run

```sh
python3 compose.py          # regenerates news.jpg (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

## Licence

MIT — see `LICENSE`.
