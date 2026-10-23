#!/usr/bin/env python3
"""
rabbit_hole_engine.py - Autonomous Epistemic Curiosity, Multi-Hop Thread Explorer,
Abductive Clue Generator, and Lateral Bisociation Engine.

Author: Antigravity Rabbit-Hole Curiosity Skill
Built on Python 3 standard library (zero external dependencies).
"""

import os
import sys
import re
import json
import hashlib
import argparse
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

USER_AGENT = "AntigravityRabbitHoleEngine/1.0 (Epistemic Curiosity & Archival Research)"
TIMEOUT = 12

# =============================================================================
# Curated Orthogonal Matrices for Arthur Koestler Bisociation ("Thinking Aside")
# =============================================================================
ORTHOGONAL_MATRICES: List[Dict[str, str]] = [
    {
        "domain": "Mycorrhizal Fungal Networks (Wood-Wide Web)",
        "principle": "Decentralized subterranean nutrient routing, chemical signaling across species, and hub-tree resource redistribution without a central brain.",
        "bridge_prompt": "How do hidden underground conduits distribute resources, warnings, or signals across seemingly separate surface actors in this topic?"
    },
    {
        "domain": "Thermodynamic Phase Transitions & Criticality",
        "principle": "Gradual accumulation of latent energy produces zero visible change until a critical threshold triggers a sudden, system-wide reorganization of state.",
        "bridge_prompt": "Where is latent pressure quietly accumulating in this topic before a sudden phase transition or paradigm shift?"
    },
    {
        "domain": "Baroque Counterpoint & Fugue Architecture (J.S. Bach)",
        "principle": "Multiple independent voices pursue the same theme at staggered intervals, inverted, retrograde, or augmented, creating harmony through structured tension.",
        "bridge_prompt": "If we treat the competing perspectives in this discussion as contrapuntal voices, what is the underlying 'subject' being inverted or mirrored?"
    },
    {
        "domain": "Adaptive Immune Memory & Clonal Selection",
        "principle": "Generating hyper-diverse random receptors in advance, amplifying only those that bind to an unexpected invader, and retaining long-term memory cells.",
        "bridge_prompt": "How does this system handle novel, never-before-seen shocks, and what serves as its long-term institutional or conceptual memory?"
    },
    {
        "domain": "Medieval Siege Craft & Star Fort Geometry (Trace Italienne)",
        "principle": "Cannon warfare rendered high vertical stone walls obsolete, forcing low, thick, angled earthen bastions with interlocking fields of fire and zero dead zones.",
        "bridge_prompt": "What 'tall vertical wall' in this field has been rendered obsolete by a new force, requiring a completely different geometry of defense or design?"
    },
    {
        "domain": "Venetian Double-Entry Bookkeeping (Luca Pacioli, 1494)",
        "principle": "Every credit requires a corresponding debit in a conserved ledger; invisible leaks and fictive capital immediately surface as structural imbalances.",
        "bridge_prompt": "What is the hidden conservation law here? When one side of this system gains, what unrecorded ledger entry is paying the cost?"
    },
    {
        "domain": "Abyssal Hydrothermal Vent Ecosystems (Chemosynthesis)",
        "principle": "Thriving complex life in pitch darkness at crushing pressure, powered entirely by volcanic chemical gradients rather than sunlight.",
        "bridge_prompt": "How can this idea or system thrive in an environment completely deprived of the 'sunlight' (conventional resources/assumptions) everyone thinks is mandatory?"
    },
    {
        "domain": "Palimpsest Manuscript Archaeology",
        "principle": "Parchment was scraped and overwritten centuries later, but multispectral imaging reveals the erased foundational text bleeding through underneath.",
        "bridge_prompt": "What older, erased 'under-text' is still secretly governing the visible rules and habits of this topic today?"
    },
    {
        "domain": "Predator-Prey Lotka-Volterra Oscillations",
        "principle": "Coupled non-linear feedback loops where the success of the predator causes its own scarcity, creating endogenous cycles without external shocks.",
        "bridge_prompt": "How does success in this domain endogenously breed its own reversal or bottleneck?"
    },
    {
        "domain": "Polynesian Wayfinding & Wave-Piloting Stick Charts",
        "principle": "Navigating thousands of miles of open ocean without compasses by reading subtle wave refractions bounced off unseen distant islands.",
        "bridge_prompt": "Instead of looking directly at the target, what faint 'wave refractions' (secondary ripple effects) reveal the presence of something unseen ahead?"
    },
    {
        "domain": "Epigenetic Chromatin Remodeling",
        "principle": "The underlying DNA sequence remains identical, yet folding/methylation switches radically alter which genes can be read and expressed.",
        "bridge_prompt": "Without changing the core components of this system, how does changing what is 'folded away' vs. 'exposed' transform its behavior?"
    },
    {
        "domain": "ant Colony Stigmergy & Pheromone Trails",
        "principle": "Complex collective intelligence emerging from agents leaving traces in the environment that guide subsequent agents, balanced by trail evaporation.",
        "bridge_prompt": "What environmental traces ('pheromones') are participants leaving behind in this discussion, and what happens if old trails fail to evaporate?"
    }
]


def http_get_json(url: str, timeout: int = TIMEOUT) -> Optional[Dict[str, Any]]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


# =============================================================================
# 1. Wikipedia / Hypertext Associative Trail Engine (Bush / Nelson / Borges)
# =============================================================================
BORING_LINK_PATTERNS = re.compile(
    r"^(ISBN|DOI|ISSN|OCLC|PMID|S2CID|Wayback Machine|Bibcode|ArXiv|Wikidata|"
    r"List of |Index of |Outline of |Category:|Help:|Portal:|Template:|Special:|"
    r"\d{4}|January|February|March|April|May|June|July|August|September|October|November|December|"
    r"United States|United Kingdom|France|Germany|New York|London| Oxford|Cambridge)$",
    re.IGNORECASE
)


def fetch_wiki_node(query_or_title: str) -> Optional[Dict[str, Any]]:
    """Fetches a Wikipedia concept summary, categories, and outgoing hypertext links."""
    # Step 1: Search for best matching page title
    search_params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": query_or_title,
        "srlimit": "3",
        "format": "json"
    })
    search_data = http_get_json(f"https://en.wikipedia.org/w/api.php?{search_params}")
    if not search_data:
        return None
    hits = search_data.get("query", {}).get("search", [])
    if not hits:
        return None

    title = hits[0]["title"]

    # Step 2: Fetch extract, links, see-also sections, and categories
    prop_params = urllib.parse.urlencode({
        "action": "query",
        "titles": title,
        "prop": "extracts|links|categories",
        "exintro": "1",
        "explaintext": "1",
        "pllimit": "80",
        "plnamespace": "0",
        "cllimit": "15",
        "format": "json"
    })
    page_data = http_get_json(f"https://en.wikipedia.org/w/api.php?{prop_params}")
    if not page_data:
        return None

    pages = page_data.get("query", {}).get("pages", {})
    page_obj = next(iter(pages.values()), {})
    extract = page_obj.get("extract", "").strip()
    raw_links = [l.get("title", "") for l in page_obj.get("links", []) if l.get("title")]
    categories = [
        c.get("title", "").replace("Category:", "")
        for c in page_obj.get("categories", [])
        if "articles" not in c.get("title", "").lower()
        and "pages" not in c.get("title", "").lower()
        and "wikidata" not in c.get("title", "").lower()
        and "cs1" not in c.get("title", "").lower()
    ]

    # Filter links to keep high-curiosity conceptual threads
    interesting_links = [
        lnk for lnk in raw_links
        if not BORING_LINK_PATTERNS.match(lnk)
        and len(lnk) > 4
        and lnk.lower() != title.lower()
    ]

    # Sort links deterministically but favor multi-word conceptual phrases
    def link_curiosity_score(lnk: str) -> Tuple[int, int]:
        words = lnk.split()
        has_concept_kw = any(
            w in lnk.lower()
            for w in ["theory", "paradox", "effect", "hypothesis", "history", "philosophy",
                      "psychology", "system", "model", "law", "problem", "illusion",
                      "architecture", "network", "labyrinth", "method", "experiment", "syndrome"]
        )
        return (1 if has_concept_kw else 0, 1 if 2 <= len(words) <= 4 else 0)

    interesting_links.sort(key=link_curiosity_score, reverse=True)

    return {
        "title": title,
        "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
        "extract": re.sub(r"\s+", " ", extract)[:650],
        "categories": categories[:8],
        "threads": interesting_links[:15]
    }


def trace_associative_trail(seed_topic: str, hops: int = 3) -> List[Dict[str, Any]]:
    """
    Traces a multi-hop Vannevar Bush Memex associative trail through hypertext links.
    """
    trail: List[Dict[str, Any]] = []
    visited = set()
    current_query = seed_topic

    for hop_idx in range(hops):
        node = fetch_wiki_node(current_query)
        if not node or node["title"].lower() in visited:
            break
        visited.add(node["title"].lower())
        node["hop"] = hop_idx
        trail.append(node)

        # Choose next hop that hasn't been visited yet
        next_candidates = [t for t in node["threads"] if t.lower() not in visited]
        if not next_candidates:
            break
        # Pick candidate at offset hop_idx % len to diversify
        current_query = next_candidates[min(hop_idx, len(next_candidates) - 1)]

    return trail


# =============================================================================
# 2. Digital Library & Dojo Vault Archival Burrow (IA + Open Library + Dojo)
# =============================================================================
def search_archival_books(topic: str, rows: int = 5) -> List[Dict[str, Any]]:
    """Searches Internet Archive & Open Library for primary and scholarly books on the topic."""
    books: List[Dict[str, Any]] = []
    clean_topic = topic.replace('"', '').strip()
    queries = [
        f'mediatype:(texts) AND (title:("{clean_topic}") OR subject:("{clean_topic}"))',
        f'mediatype:(texts) AND ({clean_topic})'
    ]
    for q_str in queries:
        params = {
            "q": q_str,
            "fl[]": ["identifier", "title", "creator", "year", "access-restricted-item", "downloads"],
            "sort[]": "downloads desc",
            "rows": str(rows),
            "output": "json"
        }
        qs = urllib.parse.urlencode(params, doseq=True)
        data = http_get_json(f"https://archive.org/advancedsearch.php?{qs}")
        if data and data.get("response", {}).get("docs"):
            for doc in data["response"]["docs"]:
                restricted = str(doc.get("access-restricted-item", "false")).lower() == "true"
                ident = doc.get("identifier", "")
                books.append({
                    "identifier": ident,
                    "title": doc.get("title", "Untitled"),
                    "creator": doc.get("creator", "Unknown"),
                    "year": doc.get("year", "n.d."),
                    "access": "LENDABLE (CDL)" if restricted else "OPEN ACCESS (Full OCR)",
                    "url": f"https://archive.org/details/{ident}"
                })
            break
    return books


def search_dojo_vault(topic: str) -> List[str]:
    """Queries local Dojo knowledge corpus if `dojo` CLI is available."""
    try:
        res = subprocess.run(
            ["dojo", "search", topic],
            capture_output=True,
            text=True,
            timeout=4
        )
        if res.returncode == 0 and res.stdout.strip():
            lines = [ln.strip() for ln in res.stdout.strip().splitlines() if ln.strip()]
            return lines[:6]
    except Exception:
        pass
    return []


# =============================================================================
# 3. Five-Lens Abductive & Venatic Curiosity Question Generator
# =============================================================================
def generate_curiosity_lenses(topic: str, trail: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generates structured epistemic curiosity questions across the 5 Rabbit-Hole strata."""
    hop_titles = [n["title"] for n in trail[1:]] if len(trail) > 1 else ["adjacent disciplines"]
    hop_str = ", ".join(hop_titles)

    return [
        {
            "lens": "1. The White Rabbit Anomaly (Lewis Carroll / Thomas Kuhn)",
            "focus": "Violation of Paradigm Expectations",
            "question": f"What is the single most counterintuitive, anomalous, or 'weird' empirical fact about '{topic}' that standard textbook summaries gloss over or treat as an awkward footnote?"
        },
        {
            "lens": "2. Reasoning Backwards / The Scarlet Thread (Conan Doyle / C.S. Peirce Abduction)",
            "focus": "Retroductive Reconstruction",
            "question": f"If we treat '{topic}' as the final result at a crime scene and reason backwards, what forgotten crisis, historical constraint, or fierce controversy forced it into its current shape?"
        },
        {
            "lens": "3. The Venatic Micro-Clue & Etymology (Carlo Ginzburg / Anthony Grafton)",
            "focus": "Microscopic Marginalia & Linguistic Fossil Record",
            "question": f"What hidden history is buried inside the literal etymology, original terminology, or earliest primary-source manuscripts of '{topic}'? Whose voices or dead-end experiments were erased along the way?"
        },
        {
            "lens": "4. In the Threads / Rhizomatic Cross-Passages (Borges / Deleuze / Vannevar Bush)",
            "focus": "Multi-Hop Associative Trails",
            "question": f"Following the hypertext thread from '{topic}' into [{hop_str}], what unexpected structural isomorphism or feedback loop connects these seemingly separate worlds?"
        },
        {
            "lens": "5. Epistemic vs. Diversive Depth (Ian Leslie / Mihaly Csikszentmihalyi)",
            "focus": "First-Principles Mechanism",
            "question": f"Beneath the surface metaphors used to describe '{topic}', what is the exact causal, mathematical, or material mechanism that makes it work—and where does that mechanism break down under extreme conditions?"
        }
    ]


# =============================================================================
# 4. Sam Loyd Nine-Dot Box Audit & Edward de Bono Lateral Provocations
# =============================================================================
def generate_outside_the_box(topic: str) -> Dict[str, Any]:
    """Generates Nine-Dot boundary diagnostics and Edward de Bono Lateral Thinking provocations."""
    return {
        "nine_dot_origin": (
            "Inspired by Sam Loyd's 1914 'Christopher Columbus's Egg Puzzle' (the 3x3 Nine-Dot Puzzle), "
            "where connecting all 9 dots with 4 straight lines requires drawing BEYOND the imaginary "
            "square perimeter that human Gestalt perception unconsciously projects."
        ),
        "boundary_audit_questions": [
            f"Boundary 1 (The Invisible Perimeter): What unspoken rule or boundary in '{topic}' is everyone obeying simply because they assume the 'dots' define a closed box?",
            f"Boundary 2 (Scale & Time Horizon): What happens to '{topic}' if we shrink the scale by 1,000x (micro-level) or expand the time horizon by 100 years?",
            f"Boundary 3 (The Observer Frame): Who is currently defining what counts as 'success' or 'normal' in '{topic}', and how does the problem look from the perspective of an outsider or waste byproduct?"
        ],
        "de_bono_lateral_provocations": [
            f"PO-1 [Reversal]: Instead of 'How do we optimize/understand {topic}?', ask: 'What if {topic} deliberately worked in reverse, or what if the perceived flaw is actually its primary feature?'",
            f"PO-2 [Elimination]: What happens if we remove the single most 'indispensable' component of '{topic}' and force the remaining parts to compensate?",
            f"PO-3 [Exaggeration]: What if '{topic}' were scaled to 100% of the entire system, or reduced to zero tomorrow?",
            f"PO-4 [Hole-Switching]: Edward de Bono's Law: 'Vertical thinking is digging the same hole deeper; lateral thinking is digging a hole in a new place.' Where is the current discussion digging a deeper hole in the wrong spot?"
        ]
    }


# =============================================================================
# 5. Arthur Koestler Bisociation Collider ("Thinking Aside")
# =============================================================================
def select_bisociations(topic: str, custom_matrix: Optional[str] = None, count: int = 3) -> List[Dict[str, str]]:
    """Selects orthogonal matrices to collide with `<topic>` at right angles."""
    selected: List[Dict[str, str]] = []
    if custom_matrix:
        selected.append({
            "domain": custom_matrix,
            "principle": f"Structural laws, dynamics, and failure modes native to {custom_matrix}.",
            "bridge_prompt": f"Bisociate '{topic}' (Matrix 1) with '{custom_matrix}' (Matrix 2): Where do their underlying mechanisms intersect at right angles?"
        })

    # Deterministically hash topic to pick diverse matrices
    h = int(hashlib.sha256(topic.encode("utf-8")).hexdigest(), 16)
    n = len(ORTHOGONAL_MATRICES)
    for i in range(count):
        idx = (h + i * 5) % n
        mat = ORTHOGONAL_MATRICES[idx]
        selected.append({
            "domain": mat["domain"],
            "principle": mat["principle"],
            "bridge_prompt": f"[{topic} × {mat['domain']}] {mat['bridge_prompt']}"
        })
    return selected[:count]


# =============================================================================
# Report Formatter
# =============================================================================
def format_markdown_report(
    topic: str,
    trail: List[Dict[str, Any]],
    books: List[Dict[str, Any]],
    dojo_hits: List[str],
    lenses: List[Dict[str, str]],
    box_audit: Dict[str, Any],
    bisociations: List[Dict[str, str]]
) -> str:
    lines: List[str] = []
    lines.append(f"# Rabbit-Hole Curiosity Dossier: {topic}")
    lines.append("*Generated by the Antigravity Rabbit-Hole Curiosity Engine (`rabbit_hole_engine.py`)*\n")

    # 1. Associative Hypertext Trail
    lines.append("## 1. In the Threads: Live Multi-Hop Associative Trail (Bush / Nelson / Borges)")
    if trail:
        seed = trail[0]
        lines.append(f"- **Entry Shaft (`Hop 0`) — [{seed['title']}]({seed['url']})**:")
        lines.append(f"  > {seed['extract']}")
        if seed["categories"]:
            lines.append(f"  - *Ontological Categories*: `{', '.join(seed['categories'])}`")
        if seed["threads"]:
            lines.append(f"  - *Branching Subterranean Threads*: {', '.join(f'`{t}`' for t in seed['threads'][:10])}\n")

        for node in trail[1:]:
            lines.append(f"- **Associative Leap (`Hop {node['hop']}`) — [{node['title']}]({node['url']})**:")
            lines.append(f"  > {node['extract']}")
            if node["threads"]:
                lines.append(f"  - *Next-Level Threads*: {', '.join(f'`{t}`' for t in node['threads'][:6])}\n")
    else:
        lines.append(f"- *No live Wikipedia hypertext node matched `{topic}` directly — treat `{topic}` as an uncharted frontier and apply direct abductive decomposition below.*\n")

    # 2. Primary Source Archival Books
    lines.append("## 2. Primary-Source Archival Burrow (Internet Archive & Open Library)")
    if books:
        for b in books:
            lines.append(f"- **`[{b['access']}]` [{b['title']}]({b['url']})** ({b['year']}) — *{b['creator']}* (`{b['identifier']}`)")
        lines.append("\n  *(Tip: Run `python3 ~/.agents/skills/librarian/scripts/librarian_cli.py extract <identifier> --keywords \"...\"` to ingest full-text OCR from any open or lendable volume above.)*\n")
    else:
        lines.append("- *No direct catalog title match; broaden search terms with `librarian_cli.py global-search`.*\n")

    if dojo_hits:
        lines.append("### Local Dojo Vault Connections")
        for dh in dojo_hits:
            lines.append(f"- `{dh}`")
        lines.append("")

    # 3. Five-Lens Abductive & Venatic Prompts
    lines.append("## 3. The Five Investigative Lenses (Carroll / Peirce / Ginzburg / Kuhn / Leslie)")
    for l in lenses:
        lines.append(f"### {l['lens']}")
        lines.append(f"- **Cognitive Focus**: *{l['focus']}*")
        lines.append(f"- **Investigative Probe**: {l['question']}\n")

    # 4. Outside the Nine-Dot Box & De Bono Lateral Hole-Digging
    lines.append("## 4. Thinking Outside the Box & Lateral Hole-Switching (Sam Loyd / Edward de Bono)")
    lines.append(f"> *{box_audit['nine_dot_origin']}*\n")
    lines.append("### Self-Imposed Boundary Diagnostics")
    for q in box_audit["boundary_audit_questions"]:
        lines.append(f"- {q}")
    lines.append("\n### Edward de Bono Lateral Provocations (`PO`)")
    for po in box_audit["de_bono_lateral_provocations"]:
        lines.append(f"- {po}")
    lines.append("")

    # 5. Arthur Koestler Bisociation Collisions
    lines.append("## 5. Arthur Koestler Bisociation Collider ('Thinking Aside' Across Matrices)")
    for idx, bi in enumerate(bisociations, 1):
        lines.append(f"### Collision {idx}: `{topic}` × `{bi['domain']}`")
        lines.append(f"- **Orthogonal Matrix Principle**: {bi['principle']}")
        lines.append(f"- **Bisociative Synthesis Prompt**: **{bi['bridge_prompt']}**\n")

    # 6. Hofstadter Stack & Epistemic Compass
    lines.append("## 6. Hofstadter Inquiry Stack (`PUSH`/`POP`) & Epistemic Compass")
    lines.append("```text")
    lines.append(f"[STACK LEVEL 0: SURFACE GOAL]  {topic}")
    if len(trail) > 1:
        for n in trail[1:]:
            lines.append(f"  └── PUSH [HOP {n['hop']} THREAD]   {n['title']}  (Remember to POP back to Level 0!)")
    for idx, bi in enumerate(bisociations, 1):
        lines.append(f"  └── PUSH [BISOCIATION {idx}]  {topic} × {bi['domain']}")
    lines.append("```")
    lines.append("- **Mertonian Serendipity vs. Apophenia Check (Eco / Pynchon)**:")
    lines.append("  1. *Does this connection rest on a verifiable causal mechanism, primary source, or testable structural isomorphism?* (Serendipity)")
    lines.append("  2. *Or does it rely purely on verbal coincidence and unfalsifiable pattern-matching?* (Apophenia — discard or flag as metaphor!)")

    return "\n".join(lines)


# =============================================================================
# CLI Entrypoint
# =============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rabbit-Hole Curiosity Engine: Multi-Hop Thread Explorer, Abductive Clue Generator & Lateral Bisociation Collider"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # explore
    p_exp = subparsers.add_parser("explore", help="Run full 6-stratum rabbit-hole exploration on a topic")
    p_exp.add_argument("topic", help="Topic, question, or concept to investigate")
    p_exp.add_argument("--hops", type=int, default=3, help="Number of associative hypertext hops (default: 3)")
    p_exp.add_argument("--rows", type=int, default=5, help="Number of archival books to retrieve (default: 5)")
    p_exp.add_argument("--matrix", help="Optional custom orthogonal domain for Koestler bisociation")
    p_exp.add_argument("-o", "--output", help="Save full Markdown dossier to file")

    # threads
    p_thr = subparsers.add_parser("threads", help="Trace a live multi-hop associative hypertext trail")
    p_thr.add_argument("topic", help="Seed topic")
    p_thr.add_argument("--hops", type=int, default=3, help="Number of hops (default: 3)")

    # bisociate
    p_bis = subparsers.add_parser("bisociate", help="Collide topic with orthogonal domains (Koestler Bisociation)")
    p_bis.add_argument("topic", help="Target topic")
    p_bis.add_argument("--matrix", help="Specific orthogonal matrix to collide with")
    p_bis.add_argument("--count", type=int, default=3, help="Number of collisions (default: 3)")

    # outside-the-box
    p_box = subparsers.add_parser("outside-the-box", help="Run Sam Loyd Nine-Dot boundary audit & De Bono lateral provocations")
    p_box.add_argument("topic", help="Target topic or problem")

    args = parser.parse_args()

    if args.command == "explore":
        trail = trace_associative_trail(args.topic, hops=args.hops)
        books = search_archival_books(args.topic, rows=args.rows)
        dojo_hits = search_dojo_vault(args.topic)
        lenses = generate_curiosity_lenses(args.topic, trail)
        box_audit = generate_outside_the_box(args.topic)
        bisociations = select_bisociations(args.topic, custom_matrix=args.matrix, count=3)

        report = format_markdown_report(
            topic=args.topic,
            trail=trail,
            books=books,
            dojo_hits=dojo_hits,
            lenses=lenses,
            box_audit=box_audit,
            bisociations=bisociations
        )
        if args.output:
            out_path = Path(args.output).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report, encoding="utf-8")
            print(f"[Rabbit-Hole Engine] Dossier saved to {out_path} ({len(report.splitlines())} lines).")
        else:
            print(report)
        return 0

    elif args.command == "threads":
        trail = trace_associative_trail(args.topic, hops=args.hops)
        for node in trail:
            print(f"[Hop {node['hop']}] {node['title']} ({node['url']})")
            print(f"  Summary: {node['extract']}")
            print(f"  Threads: {', '.join(node['threads'][:8])}\n")
        return 0

    elif args.command == "bisociate":
        bis = select_bisociations(args.topic, custom_matrix=args.matrix, count=args.count)
        for idx, b in enumerate(bis, 1):
            print(f"=== Collision {idx}: {args.topic} × {b['domain']} ===")
            print(f"  Principle: {b['principle']}")
            print(f"  Prompt:    {b['bridge_prompt']}\n")
        return 0

    elif args.command == "outside-the-box":
        box = generate_outside_the_box(args.topic)
        print(f"=== Sam Loyd 1914 Nine-Dot Boundary Audit: {args.topic} ===")
        for q in box["boundary_audit_questions"]:
            print(f"  • {q}")
        print("\n=== Edward de Bono Lateral Provocations (PO) ===")
        for po in box["de_bono_lateral_provocations"]:
            print(f"  • {po}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
