# talks

Talks by Zhiqian Chen (RIT Computer Science), one folder per talk, named by the date it was given (YYYY-MM-DD-name), so the folders sort by date. Each folder is a self contained reveal.js deck.

Online: https://aquastar.github.io/talks/

| Folder | Talk | Where |
|---|---|---|
| 2026-11-19-graph-inside/ | Is There a Graph Inside Generative Models? Evidence from Language and Music | RIT CS department talk, Nov 19 2026 |
| 2026-11-03-ai-literacy/ | AI Literacy for CS Faculty | RIT CS faculty meeting, Nov 3 2026 |
| networks/ | From Networks to Neural Networks | RIT CS PhD colloquium, Oct 2026 |

History: The networks and ai-literacy folders were moved in from aquastar/neural-networks-to-networks and aquastar/ai-literacy-faculty with their full git history (git subtree). Those repos are kept as they were. The graph-inside folder came from aquastar/graph-inside-generative-models the same way.

Building: `python3 2026-11-19-graph-inside/src/build.py` (it reads the October deck from the networks folder next door), `python3 <date>-networks/src/restyle.py`. ai-literacy/ is plain HTML.

Next: a shared/ folder for the style module, fonts, people photos, book covers and paper figures, and a slide library that every talk can pick from by name.

Figures reproduced from cited papers remain the property of their authors and publishers.
