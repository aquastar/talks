# talks

Talks by Zhiqian Chen (RIT Computer Science). One folder per topic, and inside it one folder per version, named by the date it was given and a short venue name.

Online: https://aquastar.github.io/talks/

| Topic (stable link) | Version | Where |
|---|---|---|
| music-to-brain/ | 2026-12-01-bibm-dallas/ | Keynote, AI4BioSig Workshop at IEEE BIBM 2026, Dallas, Dec 2026 (upcoming, day TBD) |
| graph-inside/ | 2026-11-19-cs-colloquium/ | RIT CS Department Colloquium, Nov 19 2026 |
| graph-inside/ | 2026-10-02-gccis-phd/ | RIT GCCIS PhD Colloquium Series, Oct 2 2026 |
| ai-literacy/ | 2026-11-03-faculty-meeting/ | RIT CS faculty meeting, Nov 3 2026 |

A topic link such as https://aquastar.github.io/talks/graph-inside/ always opens the latest version.

Rules for anyone, human or agent, who works here: MEMORY.md.

Building: `python3 graph-inside/2026-11-19-cs-colloquium/src/build.py` (it reads the Oct 2 version next door), `python3 graph-inside/2026-10-02-gccis-phd/src/restyle.py`. The ai-literacy version is plain HTML. `python3 -I music-to-brain/2026-12-01-bibm-dallas/src/build.py`, full layout check `music-to-brain/2026-12-01-bibm-dallas/src/measure.sh OUTDIR`.

History: the Oct 2 and Nov 3 versions came from aquastar/neural-networks-to-networks and aquastar/ai-literacy-faculty with full git history (git subtree), and those repos are kept as they were. The Nov 19 version came from aquastar/graph-inside-generative-models the same way, and that repo was deleted afterwards. music-to-brain came from aquastar/music-to-brain the same way (2026-11-16), to be deleted after this move.

Figures reproduced from cited papers remain the property of their authors and publishers.
