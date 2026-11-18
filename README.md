# The World in One Image — Wednesday, 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Tiannuryadins/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Tiannuryadins/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

An entry for the make.fun bounty **"Sum up 18 November's world news in one image"**
(`news-image-20261118`): $250 in prizes shared by the top 50 entries — $50 for
1st, $30 for 2nd, $15 for 3rd, $5 for 4th–10th, $3 for 11th–50th. Entries close
Friday 20 November 2026, 00:00 UTC (07:00 WIB). Entry is free.

## The idea

A newspaper front page for one day: the program writes a single poster that
lets anyone who missed Wednesday, 18 November 2026 catch up on it at a glance —
one lead story, a by-the-numbers strip, and nine more stories in a grid, each
with a category tag and a hand-drawn icon. The image carries the news itself
(the judge has no news feed), so every story is named, dated and sourced on
the poster.

Run it and you get `world_news_18_nov_2026.png` written to `/output/entry.png`:

```bash
python3 main.py                                    # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py        # local testing override
```

`main.py` is standard library only and reads the poster PNG that ships in this
repo — no Pillow at run time (the grader runs `python3 -P -s`, where Pillow
does not exist), no network, and the same bytes on every run, so the two
grader runs write identical files. If `/output` is not writable it falls back
to `./output/entry.png`. The program checks the gate itself on every run with
a small stdlib PNG parser: the file must be a whole PNG of at most 1 MiB and
1024×1024 px. This poster is 1024×1024 px and under 1 MiB.

## The day in ten stories

All ten were reported on 18 November 2026 and cross-checked against at least
two independent sources (full list in BUILD-TRANSCRIPT.md):

| # | Story |
| --- | --- |
| 1 | **APEC opens in Shenzhen** — Xi urges 21 economies to tear down trade barriers; Trump lands late Wednesday, Putin is already there, and the first-ever Trump–Xi–Putin trilateral meets Thursday. *(Reuters, CNBC, Xinhua)* |
| 2 | **Kuwait and Bahrain hit by drones; US strikes Qeshm** — third Bahrain attack in five days; US jets hit an IRGC missile site on Qeshm Island. *(Reuters, Al Jazeera, Devdiscourse)* |
| 3 | **Kerch Bridge span in the sea after a second strike** — Ukraine's record 1,441-drone raid; road arch fell, traffic halted, Kyiv's bridges hit. *(Reuters, EuropeSays, Devdiscourse)* |
| 4 | **QUAD unveils a new plan in Manila** — maritime surveillance, AI fund and cable links agreed by the four nations. *(MEA India, Reuters, The Hindu BusinessLine)* |
| 5 | **Canada and China extend trade deals** — Xi meets Carney before APEC as Ottawa diversifies away from US trade. *(Reuters, Canada Government, Jagran Josh)* |
| 6 | **Australia sanctions settler firms** — three people and four groups hit, following the UK's sanctions on eight firms. *(Reuters, The Guardian, TradersUnion)* |
| 7 | **MS Dhoni retires from the IPL** — 278 matches and 5 titles in 19 seasons; the 45-year-old stays on as CSK mentor. *(Reuters, The Hindu BusinessLine, CSK)* |
| 8 | **Cyclone Akvan bears down on Andhra Pradesh** — landfall due Friday noon; 145 km/h gusts, red alert. *(IMD, The Hindu, Indian Express)* |
| 9 | **US presses the UN over Taiwan flight curbs** — Washington urges ICAO to act; China hits back as Taipei seeks $14B in arms. *(Reuters, NDTV, Jagran Josh)* |
| 10 | **Trump backs Huang for the Nvidia top job** — the board says no return for the ex-CEO; quarterly sales still up 103%. *(Indian Express, Reuters, Washington Post)* |

Nothing here is invented. Two stories were deliberately left out because their
events belong to other days: the ULA Vulcan rocket failure (15 November) and
the Dow's 1,000-point plunge at Monday's close (17 November).

## Files in this repo

- `main.py` — the entry point: reads the poster and writes `/output/entry.png`
- `render_poster.py` — draws the poster with Pillow (build time only)
- `world_news_18_nov_2026.png` — the poster (1024×1024)
- `LICENSE` — MIT (OSI-approved)
- `BUILD-TRANSCRIPT.md` — research notes, test results, bundling notes

To change the poster, edit `render_poster.py` and re-run it:

```bash
pip install pillow        # only needed for rendering, not for the entry
python3 render_poster.py  # regenerates world_news_18_nov_2026.png
```

The renderer asserts that every headline and body fits its card, so a layout
overflow fails loudly at build time instead of shipping a broken poster.

## License

MIT — see `LICENSE`. Copyright (c) 2026 Januar.
