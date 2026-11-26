# Outline v2: The Music That Plays the Brain (40 min, 29 main slides)

2026-11-26. Built from the RIT CS colloquium Part 2 and opening (graph-inside/2026-11-19-cs-colloquium), the current keynote, and research/music-brain-trends.md in the KB. Seconds in brackets. Total about 2210 s, 37 min, leaves 3 min for the demo running long.

Throughline: AI can now set the music to a dose, and the brain can grade it.

Three findings (forecast on slide 4, returned on slide 29):
1. Sound reliably moves brain signals, but music used as a fixed stimulus rarely moves clinical outcomes.
2. A small graph of note transitions already names a style and predicts the listening brain.
3. Generators can be turned knob by knob, so the missing step is write, then let the brain verify.

Recurring map: Read, Model, Write (small header strip on every body slide, full map on 10, 23).

## Opening (about 4 min)
1. Cover. Title, animated Für Elise dots. [20]
2. Pink Floyd, played back from electrodes on the brains of 29 patients (Bellier 2023, audio). The "read" hook. [75]
3. Many people with advanced dementia can still sing the hymns of their youth. Question: could we choose the song and watch the brain answer? [60]
4. Forecast: three findings, one figure each. [75]

## Part 1. Why now: what is and what is not working (about 8 min)
5. Hearing loss is a quiet epidemic, tied to dementia and depression (colloq 20, WHO, Lin, Lancet Commission 2024, ACHIEVE). [90]
6. Sound acts on the brain in ways we can measure (colloq 21: Nozaradan 2011, Salimpoor 2011, 40 Hz in mice). [60]
7. Music already acts as medicine, and nobody knows which part does the work (colloq 22 cards). [75]
8. NEW. The biggest, best controlled trials came back null: HOPE 40 Hz (CTAD 2026, verify), MIDDEL 1,021 residents, ICU music vs a silent track, LongSTEP. Expected result first, then the real one. [90]
9. NEW. What works is specific and closed loop: InTandem tempo follows gait (RCT, FDA, Medicare code E3200), adaptive RAS in Parkinson's (npj PD 2025), Lenire. [75]
10. Landmark and map. The missing piece is a knob: in every trial the music was fixed. Read, Model, Write. [60]

## Part 2. Read (about 2 min)
11. NEW. The brain can be read back into music: EEG and fMRI to audio (Postolache ICASSP 2025, MAAS NeurIPS 2026 with its shuffle control). Honest line: the generator sets the ceiling. [90]

## Part 3. Model (about 13 min)
12. In music, emotion lives in expectation (Meyer 1956, trimmed from colloq 5). [60]
13. A music generator is a language model with a pitch helix inside (colloq 6, Yagi 2026). [90]
14. Learned chord maps follow music theory's geometry (colloq 7, Tonnetz vs ISMIR 2026 map). [90]
15. A tiny graph is enough to represent a piece of music: Für Elise demo, listen then walk (colloq 25). Memorable moment 1. [60]
16. Fold 88 keys into 12, and a melody becomes 144 numbers (colloq 26). [90]
17. The simplest graph already names the tradition, 70.2% vs 17% chance. In progress. (colloq 27) [75]
18. A note transition graph predicts the listening brain (Di Liberto 2020, colloq 29). [90]
19. Past about eight notes, a better music model fits the brain worse (Kern 2022). [60]
20. Live: what MusicGen expects, next to what listeners' brains do (eeg-demo view=talk, colloq 30). Memorable moment 2, core result. Never tick the random model control live. [150]
21. Breath slide, the honest catch: on average yes, note by note not yet better than an untrained model. [60]
22. The brain is read as a graph too (colloq 31, for the biosignal audience). [75]

## Part 4. Write (about 8 min)
23. Landmark and map. Write is the missing step: vision and language already wrote stimuli and verified them in new people (Bashivan 2019, Tuckute 2024), music has none. [75]
24. Steering leaves a style easily but rarely enters one (colloq 28, co-authored work under review). [75]
25. Turn one dial: the same notes go from shuffled to almost a tune, then Beethoven (audio). [75]
26. Turn one dial inside MusicGen: same seed, only the tempo words change (audio). [60]
27. Vision. Close the loop: the brain's response picks the next phrase, and baseline EEG predicts who responds (sound mockup, CLAS responders, Chan 2025). [90]
28. Three experiments you could run next month with these stimuli (the ask). [75]

## Close (about 1.5 min)
29. Next time she sings, we choose the song, and her brain shows us what she responds to. Three contributions, the ask, QR to this deck, "or zhiqian.ai, then Talks". [90]

## Backup (under the down arrow)
Dopamine twice, song population in cortex, imagined march, Brain2Music, layer alignment, prescription card, frequency tagging, binaural beats and focus music (Woods 2024), neural data laws (CO, CA, MT, CT), TRIBE v2, all rigor slides.

## Needs him
- Keep Pink Floyd as cold open, or open with the colloquium cover graphs?
- Slide 8 HOPE numbers come only from news snippets: OK to show only "missed primary endpoint" until the paper is out?
- Slide 24 steering audio (same piece, style removed vs intact) if he has it.
