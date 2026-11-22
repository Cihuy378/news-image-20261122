# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Cihuy378/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Cihuy378/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Sunday, 22 November 2026

A make.fun `news-image-20261122` entry: one 1024×1024 newspaper front
page that sums up the world's news of **Sunday, 22 November 2026** —
30 stories across 7 regions, every one dated to that day.

## The front page

**Antalya — COP31, the lead.** After two days of overtime, the summit
presidents tabled a new package they say all sides can accept;
delegates had until 03:00 GMT to object, with an approval session at
06:00 GMT on Sunday. (Reuters)

**Bahrain and Hormuz — war.** Iran says it struck US bases at
al-Riffa and Awali; Bahrain says a civilian plant caught fire, with
no injuries. Two tankers were hit leaving the Strait of Hormuz.
(Al Jazeera, UKMTO)

**Gulf of Finland — war at sea.** The Russian cargo ship Sparta II,
bound for Kaliningrad, caught fire after a drone strike and drifted
into Finnish waters; all 16 crew were taken off. (Reuters, Finland)

**Peru — earthquake.** Sunday's toll from Friday's M6.7 Junin quake:
1 dead, 16 hurt, 152 homes uninhabitable. (USGS, Peru government)

**Also leading:** the Kryvyi Rih double-tap strike; Mexico's
confirmation that FBI Top Ten fugitive "El Chapo Isidro" was captured
in Sinaloa; Verstappen on pole for Sunday's Las Vegas Grand Prix;
England's 37–12 rugby win over the All Blacks — plus 21 more briefs,
from Poland and Denmark to Nigeria, Timor-Leste and the Nasdaq slide.

A date-check box on the page says plainly which stories are shown
only because Sunday brought something new — a toll, a confirmation
or a vote — and what was not yet confirmed when the page was drawn.

## How the image was made

- `compose.py` (Python 3, Pillow) draws the whole page: masthead,
  key-numbers strip, region bar, headlines, decks, briefs, map and
  footer. Every word on the page is rendered by this script, so the
  finished image carries no garbled AI text. The script is
  deterministic — no network, no clock, no randomness.
- `assets/` holds four editorial illustrations generated for this
  entry (the COP31 hall in Antalya, tankers in the Strait of Hormuz,
  the Sparta II on fire, the Andes above Junin). They contain no
  text; every word on the page comes from `compose.py`.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png`, byte for byte.

Rebuild the image: `python3 compose.py` — then test the entry
program twice and compare the outputs:

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
cmp out1/entry.png out2/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=brisk-koala-55&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
