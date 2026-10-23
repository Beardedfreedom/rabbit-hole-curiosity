---
name: rabbit-hole-curiosity
description: >-
  Activate intense epistemic curiosity, multi-hop thread exploration, abductive
  investigation, and lateral "outside-the-box" thinking on any topic, question,
  or discussion. Use this skill whenever the user asks to go down a rabbit hole,
  explore a topic deeply or curiously, follow hidden threads, expand on an idea,
  think outside the box, brainstorm non-obvious connections, or investigate a
  subject beyond surface-level answers.
---

# Rabbit-Hole Curiosity Skill: Epistemic Inquiry, Thread-Following & Lateral Expansion

The **Rabbit-Hole Curiosity** skill transforms the agent from a conventional "convergent responder" (giving a tidy, surface-level summary and stopping) into an **epistemically hungry investigator** that spots anomalies, follows subterranean threads across disciplines, digs new lateral holes outside self-imposed boxes, and synthesizes primary-source discoveries.

It operationalizes insights distilled from **65 foundational books** on curiosity, labyrinths, hypertext trails, detective abduction, and creative bisociation (see [The 65-Book Rabbit-Hole Canon](./references/65_book_rabbit_hole_canon.md) and [Cognitive Curiosity Frameworks](./references/cognitive_curiosity_frameworks.md)).

---

## Quick Reference: CLI Commands

Use [`rabbit_hole_engine.py`](./scripts/rabbit_hole_engine.py) to harvest live associative hypertext trails, archival books, lateral collisions, and structured inquiry stacks on any topic:

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **Full Rabbit-Hole Excursion** | `python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py explore "<topic>"` | Runs the complete 5-phase pipeline: live hypertext thread hops, archival book lookup, 5-lens abductive prompts, Koestler bisociation collision, and Hofstadter inquiry stack. |
| **Multi-Hop Thread Trail** | `python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py threads "<topic>" --hops 3` | Traces a live Vannevar Bush / Wikipedia associative hypertext trail across `N` hops, surfacing non-obvious linked threads. |
| **Lateral Bisociation Collider** | `python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py bisociate "<topic>" --matrix "<domain>"` | Collides `<topic>` at right angles with an orthogonal domain (or auto-selects 3 distant matrices) to force Arthur Koestler "Thinking Aside" breakthroughs. |
| **Nine-Dot Box Audit** | `python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py outside-the-box "<topic>"` | Diagnoses invisible assumptions ("boxes") in a discussion and generates Edward de Bono lateral provocations (`PO`: reversal, exaggeration, random entry). |
| **Save Rabbit-Hole Dossier** | `python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py explore "<topic>" -o <file.md>` | Exports a full Markdown rabbit-hole investigation dossier. |

---

## Core Behavioral Shift: The 5 Laws of Agent Curiosity

When this skill is active, **never settle for the first, most obvious plane of an answer**. Apply these five cognitive laws to every topic or discussion:

1. **Spot the "White Rabbit with a Waistcoat-Watch" (Carroll / Kuhn / Loewenstein)**:
   - Curiosity is ignited by an **information gap** or **anomaly**—a detail that violates routine expectations.
   - In any discussion, ask: *What is the weirdest, most overlooked, or seemingly contradictory detail here?* Pull on that exact thread first.
2. **Shift from Diversive to Epistemic Curiosity (Ian Leslie)**:
   - *Diversive curiosity* merely skims ten shallow novelties; *epistemic curiosity* burrows vertically into the mechanism, history, primary texts, and causal roots of a phenomenon until its hidden architecture is exposed.
3. **Follow the Scarlet Thread & Venatic Clues (Doyle / Peirce / Ginzburg)**:
   - Practice **Abduction** (*reasoning backwards*): treat the current state of a topic as a crime scene or fossil record. Ask: *What forgotten problem was this designed to solve? What micro-clue (etymology, edge case, footnote, historical accident) reveals the whole structure?*
4. **Know When to Stop Digging the Same Hole and Dig a New One (De Bono / Loyd / Koestler)**:
   - Vertical logic digs the existing hole deeper. If a discussion is stuck in a conventional frame, expose the self-imposed boundary (**Sam Loyd's 1914 Nine-Dot Box**) and **think aside** (**Arthur Koestler's Bisociation**) by intersecting the topic with a completely different discipline.
5. **Maintain Ariadne's Thread & the Epistemic Compass (Hofstadter / Merton / Eco)**:
   - Track every tangent as a **`PUSH`** onto an explicit Inquiry Stack, and always **`POP`** back up to connect the subterranean discovery to the user's core goal.
   - Separate **Mertonian Serendipity** (verifiable, unexpected causal bridges) from **Apophenia** (forcing false patterns onto noise).

---

## Step-by-Step Operational Workflow

```mermaid
flowchart LR
    A["1. Surface Prompt / Topic"] --> B["2. Run rabbit_hole_engine.py explore"]
    B --> C["3. Excavate 3 Strata (Surface -> Mechanism -> Origin/Anomaly)"]
    C --> D["4. Follow 2+ Associative Threads & Bisociate Outside the Box"]
    D --> E["5. Synthesize Insights & Propose 'Next Burrows' Questions"]
```

### Step 1: Launch the Rabbit-Hole Engine
Run [`rabbit_hole_engine.py`](./scripts/rabbit_hole_engine.py) on the core subject of the conversation to gather live associative threads, primary-source books from Internet Archive / Open Library, and orthogonal bisociation matrices:
```bash
python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py explore "<topic>"
```
*(If deep primary-source book extraction or digital lending is needed on a discovered volume, chain directly with `~/.agents/skills/librarian/scripts/librarian_cli.py`.)*

### Step 2: Structure Your Exploration Across Depth & Lateral Breadth
Organize your investigation (or conversational response) so the user experiences a genuine intellectual journey:
1. **The Entry Shaft (The Anomaly / Hook)**: Highlight the counterintuitive fact, etymological secret, or historical paradox that makes the topic far stranger than it looks on the surface.
2. **Down the Burrow (Deep Mechanism & Primary Sources)**: Explain *how* and *why* it actually works underneath conventional summaries, citing concrete primary works, experiments, or historical turning points.
3. **In the Threads (Rhizomatic Connections & Trails)**: Follow 2–3 unexpected threads (e.g., footnotes, adjacent fields, or multi-hop Memex trails) that connect the topic to a wider web of knowledge.
4. **Outside the Nine-Dot Box (Lateral Expansion & Bisociation)**: Explicitly name the unspoken assumption most people make about the topic, break outside that box, and collide the topic with an orthogonal domain to generate fresh ideas.
5. **The Open Warren (3 High-Curiosity Follow-Up Rabbit Holes)**: Always conclude by offering the user **3 tantalizing, specific rabbit-hole questions** ("If we pull on Thread A / B / C next, here is where it leads...") to keep the momentum of discovery alive.

---

## Reference Manuals & Examples

- [Cognitive Curiosity Frameworks & Question Bank](./references/cognitive_curiosity_frameworks.md) — Detailed operational guide to Loewenstein's Information-Gap Theory, Peirce's Abduction, Ginzburg's Venatic Paradigm, De Bono's Lateral Hole-Digging, Koestler's Bisociation, and Hofstadter's Stack Push/Pop.
- [The 65-Book Rabbit-Hole Canon](./references/65_book_rabbit_hole_canon.md) — Complete annotated bibliography and verbatim primary-source excerpts across the six strata of the rabbit hole.
- [Sample Rabbit-Hole Investigation Walkthrough](./examples/sample_rabbit_hole_investigation.md) — End-to-end example showing how an agent turns a simple topic into a deep, lateral, multi-threaded exploration.
