# talks

Talks by Zhiqian Chen (RIT Computer Science), one folder per talk. Each folder is a self contained reveal.js deck.

Online: https://aquastar.github.io/talks/

| Folder | Talk | Where |
|---|---|---|
| graph-inside/ | Is There a Graph Inside Generative Models? Evidence from Language and Music | RIT CS department talk, Nov 19 2026 |
| ai-literacy/ | AI Literacy for CS Faculty | RIT CS faculty meeting, Fall 2026 |
| networks/ | From Networks to Neural Networks | RIT CS PhD seminar, Oct 2026 |

History: networks/ and ai-literacy/ were moved in from aquastar/neural-networks-to-networks and aquastar/ai-literacy-faculty with their full git history (git subtree). Those repos are kept as they were. graph-inside/ came from aquastar/graph-inside-generative-models the same way.

Building: `python3 graph-inside/src/build.py` (it reads the October deck from networks/ next door), `python3 networks/src/restyle.py`. ai-literacy/ is plain HTML.

Next: a shared/ folder for the style module, fonts, people photos, book covers and paper figures, and a slide library that every talk can pick from by name.

Figures reproduced from cited papers remain the property of their authors and publishers.
