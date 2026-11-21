# The World in One Day — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/LecialiArthelais/makefun-news-image-20261120-v5/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/LecialiArthelais/makefun-news-image-20261120-v5/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026, made for
the make.fun news-image-20261120 bounty. It is a newspaper front page built
from scratch on the winner template: a giant serif date, a coloured region
bar, a numbers strip, a UTC timeline, three illustrated hero cards, ten
illustrated medium cards, a numbered world map, and a DATE CHECK box naming
the big stories that happened *before* Friday. 35 stories in all, every one
verified by event date as Friday 20 November 2026 (see DESIGN.md).

This is v5. Our v4 entry ("Ardent Vector", 98.50%, rank 370/18,632) carried
40 stories with a Europe-heavy mix and no verification badges or timeline.
v5 fixes exactly those gaps, matching the structure the top-5 pages share:
35 stories with the same region balance as the leader (Europe 8, Asia 8,
Middle East 3, Africa 5, Americas 4, Oceania 3, Global 4), the same
six-number strip, OFFICIAL / CONFIRMED / REPORTED badges on every card,
and a "THE DAY IN UTC" timeline of the day's seven turning points.

## The image

- **Heroes:** Russia's overnight barrage hits three Kyiv bridges (3 struck,
  110+ missiles, 404 drones, 9+ killed) · Cyclone Akvan comes ashore in
  Odisha (300,000+ evacuated, no deaths) · Asia's AI sell-off (Taiex
  −6.2%, its worst week since 1991; Kospi −5.2%; Nikkei −5.1%), drawn as a
  four-market chart of the verified Friday closes.
- **Medium cards:** UK–EU reset deal, COP31's last day with no deal,
  a Russian Kh-101 landing in Poland, the Iraqi army entering Jurf
  al-Sakhar, Italy's general strike, Japan's inflation at 2.3%, Seoul's
  move to impeach its top judge, Kenya's first oil well, Bukele filing
  for a third term, Glenn Phillips' 118 against India.
- **Also on Friday:** 22 numbered briefs, each with its source.
- **DATE CHECK:** the Thursday stories (World Court's Myanmar ruling,
  the Shenzhen three-leader declaration, Tonga's drought emergency, the
  migrant boat lost off Senegal) are named as left out, not carried as
  leads — and BepiColombo's Mercury orbit entry plus any final COP31 text
  are named as not yet happened.

Every illustration is an original flat-vector drawing made in code
(PIL); no photographs, no AI-generated raster images, no garbled text.

## Build

```sh
python3 make_chart.py        # renders chart.png (matplotlib, verified closes only)
python3 build_frontpage.py   # writes entry.png, 1024x1024, ~216 KB
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`, as the kit's starter does. The program runs with no
network. Data lives in `stories.json` (35 stories, numbers strip, region
counts, UTC timeline, DATE CHECK, footer).

## Skills used

- **matplotlib** (23,497 GitHub stars, PSF-style permissive licence,
  line-by-line audit in the build notes): renders the four-market
  sell-off chart — one common scale, direct end labels, only the verified
  Friday closing moves, no invented intraday data.
- **scientific-visualization** playbook (K-Dense, MIT): honest-encoding
  guardrails for the chart.
- **news_image_page** playbook: the winner template and the event-date
  rule (use the date the event happened, not the date the article ran).
- **makefun_bounty_submission** playbook: fresh kit, quota check, check
  before submit, bundle run record.
