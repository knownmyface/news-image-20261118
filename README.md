# The World in One Day — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/knownmyface/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/knownmyface/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up Wednesday 18 November 2026's world news, built as a
newspaper front page: **48 stories, all 48 illustrated, six regions, four
continents**.

The masthead names the day — WEDNESDAY 18 NOVEMBER 2026 — above one
hero-sized lead photo (Iran's missiles and drones over US bases in Kuwait
and Bahrain) and two smaller leads (Xi greeting Trump on the Shenzhen
tarmac; Voyager 1 one light-day from Earth), a "Day by the Clock" timeline
strip, a labelled world map with 9 pinned places, a "Day in Numbers" band
with four real figures from the day, and a three-column numbered story
index grouped by region (Middle East & Africa, Europe & Asia-Pacific,
Americas & Global). Every headline and label is drawn in code, so the text
stays crisp; the three lead photos and the map are the only AI-generated
images, and the other illustrated stories use small flat pictograms drawn in
code (a chip, a gavel, a rocket, a storm cloud, a cricket bat, and more).

## Stories (48)

Leads: Iran fires on US bases in the Gulf (Kuwait's Ali Al Salem base and
Bahrain); Xi greets Trump at Shenzhen as APEC opens; Voyager 1 crosses one
light-day (25.9bn km) at 10:16 UTC.

Grid — Middle East & Africa: Board of Peace blames both sides; Kahana
elected Knesset speaker 66–52; Iran refuses IAEA inspection; Bahrain issues
all-clear; Ethiopia–Eritrea build-up; Nigeria: US intel vs militants;
Zamfara: 20 abducted freed; Egypt–India trade group; AU pushes Sudan, Congo
peace; Rwanda hub talks in Vienna; S. Africa shooting probe goes on; S.
Sudan vote uncertain; China buys W. African crude; US calls Qeshm strike
"self-defence"; Kuwait repels drone attack.

Grid — Europe & Asia-Pacific: APEC opens in Shenzhen; Xi, Putin meet before
trilateral; Xi: stand against protectionism; EU's €45bn for Ukraine; Putin
"not ready" for peace; Pistorius: Colby comment "stupid"; QUAD's new plan in
Manila; Modi: free e-visas for ASEAN; ASEAN chair to Singapore; Canada–China
extend deals; Cyclone Akvan red alert; Taiwan seeks $14bn in arms; India
re-elected to ITU Council; Amazon's $7bn for India; India's first SAF plant
ready.

Grid — Americas & Global: Peltola wins Alaska (Democrats 56–44); US loses
measles status; Nvidia's $115.8bn quarter; Huang to face Senate panel; Waymo
off the freeways; Kalshi halts "mention" bets; AI gun detector sued; AI
models mislabel civilians; critical Java flaw found; FAA halts router
rollout; IRS probes left-wing groups; DHS: no ships for deportations;
Trump–Marcos trade claim; Vulcan fault found; Dhoni's farewell, in lights.

All 48 stories happened or were first reported on 18 November 2026, as
reported by Reuters, AP, AFP, BBC, NYT, CNBC, the QUAD joint statement and
official sources. Nothing is invented; claims that were unverified at the
time (for example the US calling the Qeshm strike "self-defence") are
labelled as claims. Stories first reported on 17 November (the Serbia
MiG-29 crash, the Russian An-12 crash, the Phuket fire, Spain's wage
approval, France's troop denial) were checked and deliberately excluded.

## How it is built

`render.py` draws the whole front page with Python PIL (DejaVu fonts) and
writes `entry.png` (1024x1024, under 1 MiB). `main.ts` is the entry program:
it copies `entry.png` into `MAKEFUN_OUTPUT_DIR` and validates it — PNG
magic bytes, IEND trailer, dimensions from the IHDR chunk (max 1024x1024),
and file size (max 1 MiB). It uses only the Node standard library, needs no
network, and writes identical bytes on every run.

## Run it

```sh
python3 render.py        # rebuild entry.png from the assets (optional)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/entry.png` is the entry image.

## License

MIT — see `LICENSE`.

<sub>Entered on [make.fun](https://make.fun/?ref=1d5x2a29&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
