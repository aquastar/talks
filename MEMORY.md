# Memory: how talks are organized and made

Read this before doing anything in this repo. When Zhiqian gives a new rule about talks, add it here in one line with the date, and remove rules he replaces. Keep it short.

## Layout (decided 2026-11-16)
- One folder per topic, one folder per version inside it: `topic/YYYY-MM-DD-venue/`. Example: `graph-inside/2026-11-19-cs-colloquium/`.
- Topic names are short and name the research line, not one talk title: `graph-inside`, `ai-literacy`.
- Version names are the date the talk is given plus a short venue: `gccis-phd`, `cs-colloquium`, `faculty-meeting`. Folders then sort by date.
- `topic/index.html` redirects to the latest version. Update it whenever a version is added. That gives one stable link per topic, `aquastar.github.io/talks/topic/`.
- The root `index.html` and `README.md` list every topic with its versions, newest first. Update both with every new version.
- A talk that spans topics goes under the topic it is mostly about.
- `shared/` holds what more than one topic uses (style module, fonts, people photos, book covers, small demos). Move a file there the second time it is needed, not before.
- Planned after Nov 19 2026: a slide library per topic (`topic/slides/`, one function per slide, picked by name) so versions share slides instead of copying them, and `topic/figs/` for paper figures.

## Versions
- A version that has been given is frozen. Do not edit it after its date, except to fix a broken link or a missing file, and say so in the commit message. Improvements go into the next version.
- A new version starts from the previous one (copy the folder, or later, pick from the slide library). Rename the copy to its own date and venue first.

## Moving an existing talk repo in
- Use `git subtree add --prefix=topic/version <repo url> main` so the history comes along.
- Talks already given: keep the original repo untouched (his decision for neural-networks-to-networks and ai-literacy-faculty).
- Talks not yet given, and outdated outlines or drafts: move them in, update them, check every page online, and then delete the original repo. Deleting is done by a local agent after he confirms, never from a cloud session.
- After a move, search for hardcoded old paths and URLs, rebuild, and open the live pages to check that nothing returns 404.

## Publishing and links
- GitHub Pages deploys from `main`, root folder. Live site: https://aquastar.github.io/talks/
- Share the version link for an event and the topic link for a homepage or signature.
- His homepage (repo aquastar/zhiqian-ai, src/pages/teach.astro, also research.astro and index.astro) links talks only through this repo: the topic link as "Slides (latest)", each event to its version link. Add the new event there whenever a version is added. Old links already given out at events stay as they were (2026-11-16).
- A link that has been shared must keep working. If a folder is renamed after its link went out, leave a small redirect page at the old path.

## What a cloud session cannot do
- It cannot create or delete GitHub repos or change Pages settings. Give him a prompt for an agent on his own computer, then push once the repo exists.
- The cloud shell cannot reach cdnjs, so screenshots load reveal.js from a local npm copy.

## Making slides
- The full rules are in his knowledge base: aquastar/zhiqian-knowledge-base, `claude/skills/presentation-craft/` (SKILL.md, visual-style.md, reference.md). Those win over this list.
- Never use em dashes, en dashes or semicolons, in slides, notes or messages. Ranges use "to". American spelling.
- Talk with him in short Chinese. Slides in English.
- Real images next to our drawings: paper figures, book covers, photos of the people quoted. Find and download them yourself when the host is reachable, put the credit in the speaker notes, and ask him only when a site blocks scripted access. Never invent a quote.
- Numbers come only from the published version of a paper, read from the PDF. Unfinished work is labeled In progress and never counted as a result.
- Time: about 2 minutes per slide with content. A one hour slot means about 50 minutes of talking and about 30 main slides. The rest goes to backup slides under the down arrow, with one line or one number left on the main slide.
- Before pushing, screenshot every changed slide and look at it: no overlap, no clipped text, no empty boxes, no 404 in the browser console.

## Log
- 2026-11-16: repo created with graph-inside (Oct 2, Nov 19) and ai-literacy (Nov 3).
