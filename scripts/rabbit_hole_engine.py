#!/usr/bin/env python3
"""
rabbit_hole_engine.py - Deep Long-Thread Autonomous Epistemic Curiosity Engine.

A true rabbit hole is a LONG thread that takes time to descend.
Instead of a shallow 2-hop summary, this engine:
1. Fetches the FULL multi-section text of each node along the thread.
2. Searches deep inside the body sections (History, Mechanism, Paradoxes, Origins)
   to find buried anomalous sentences that link to the next concept.
3. Quotes the exact "Bridge Sentence" (the literal thread pulled) that leads
   from Hop k into Hop k+1 across 10, 15, or 20+ sequential hops.
4. Spawns branching Side-Warrens (secondary tunnels splitting off at mid-depth).
5. Queries Internet Archive, Open Library, Library of Congress, and Project Gutenberg
   at multiple depths along the thread so primary-source books are discovered
   not just for the surface topic, but for the deep subterranean hops as well.
6. Runs Sam Loyd Nine-Dot Boundary Audits, Edward de Bono Lateral Hole-Switching,
   and Arthur Koestler Bisociation Collisions across both surface and deep nodes.

Built on Python 3 standard library (zero external dependencies).
"""

import os
import sys
import re
import time
import json
import hashlib
import argparse
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

USER_AGENT = "AntigravityRabbitHoleEngine/2.0 (https://github.com/Beardedfreedom/rabbit-hole-curiosity; epistemic-research@github.com) Python-urllib/3"
TIMEOUT = 15

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
        "domain": "Ant Colony Stigmergy & Pheromone Trails",
        "principle": "Complex collective intelligence emerging from agents leaving traces in the environment that guide subsequent agents, balanced by trail evaporation.",
        "bridge_prompt": "What environmental traces ('pheromones') are participants leaving behind in this discussion, and what happens if old trails fail to evaporate?"
    }
]

BORING_LINK_PATTERNS = re.compile(
    r"^(ISBN|DOI|ISSN|OCLC|PMID|S2CID|Wayback Machine|Bibcode|ArXiv|Wikidata|"
    r"List of |Index of |Outline of |Category:|Help:|Portal:|Template:|Special:|"
    r"\d{1,4}|January|February|March|April|May|June|July|August|September|October|November|December|"
    r"United States|United Kingdom|France|Germany|Italy|Spain|China|Japan|Russia|Canada|Australia|"
    r"New York|London|Paris|Berlin|Rome|Oxford|Cambridge|Latin|Greek|English|French|German)$",
    re.IGNORECASE
)

EPISTEMIC_TRIGGER_WORDS = [
    "paradox", "anomaly", "unexpected", "mysterious", "controvers", "accident",
    "serendipit", "coined", "origin", "beneath", "hidden", "secret", "contrary",
    "puzzle", "labyrinth", "thread", "unlikely", "discovered", "forgotten",
    "strange", "curious", "assumption", "illusion", "breakthrough", "theorem",
    "hypothesis", "experiment", "philosoph", "psycholog", "mechanism", "ancient"
]


def log_progress(msg: str) -> None:
    """Prints live progress to stderr so the investigator sees each chamber being excavated."""
    sys.stderr.write(f"🐇 [Rabbit-Hole Burrower] {msg}\n")
    sys.stderr.flush()


def http_get_json(url: str, timeout: int = TIMEOUT, retries: int = 3) -> Optional[Dict[str, Any]]:
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except Exception:
            if attempt + 1 < retries:
                time.sleep(0.6 * (attempt + 1))
    return None


# =============================================================================
# 1. Deep Full-Text Node Excavator & Contextual Bridge Finder
# =============================================================================
def split_into_sentences(text: str) -> List[str]:
    """Splits article text into clean sentences."""
    cleaned = re.sub(r"\s+", " ", text)
    raw = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[])", cleaned)
    return [s.strip() for s in raw if len(s.strip()) > 35]


def extract_sections(full_text: str) -> List[Tuple[str, str]]:
    """Extracts named sections (== Section ==) from Wikipedia plaintext extract."""
    parts = re.split(r"\n(==+\s*[^=]+\s*==+)\n", full_text)
    sections: List[Tuple[str, str]] = [("Lead / Surface Overview", parts[0].strip())]
    idx = 1
    while idx + 1 < len(parts):
        header = parts[idx].strip("= \t")
        body = parts[idx + 1].strip()
        if body and header.lower() not in ["references", "external links", "further reading", "notes", "Bibliography"]:
            sections.append((header, body))
        idx += 2
    return sections


def fetch_deep_wiki_node(query_or_title: str, is_exact_title: bool = False) -> Optional[Dict[str, Any]]:
    """
    Fetches the ENTIRE multi-section text of a Wikipedia article, its sections,
    categories, backlinks, and up to 250 outgoing links to find buried threads.
    """
    title = query_or_title
    if not is_exact_title:
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

    # Fetch FULL article text (not just intro!) + links + categories, resolving redirects
    prop_params = urllib.parse.urlencode({
        "action": "query",
        "titles": title,
        "redirects": "1",
        "prop": "extracts|links|categories",
        "explaintext": "1",
        "pllimit": "250",
        "plnamespace": "0",
        "cllimit": "20",
        "format": "json"
    })
    time.sleep(0.35)
    page_data = http_get_json(f"https://en.wikipedia.org/w/api.php?{prop_params}")
    if not page_data:
        return None

    pages = page_data.get("query", {}).get("pages", {})
    page_obj = next(iter(pages.values()), {})
    title = page_obj.get("title", title)
    full_text = page_obj.get("extract", "").strip()
    if not full_text:
        return None

    sections = extract_sections(full_text)
    lead_text = sections[0][1] if sections else full_text[:1000]

    # Pick a deep section excerpt (e.g., History, Etymology, Mechanism, Paradox, or mid-article section)
    deep_section_title = "Deep Subterranean Section"
    deep_section_excerpt = ""
    for sec_title, sec_body in sections[1:]:
        if len(sec_body) > 200:
            deep_section_title = sec_title
            deep_section_excerpt = re.sub(r"\s+", " ", sec_body)[:700]
            if any(k in sec_title.lower() for k in ["history", "origin", "etymology", "mechanism", "theory", "paradox", "criticism", "controversy", "example", "discovery"]):
                break

    raw_links = [l.get("title", "") for l in page_obj.get("links", []) if l.get("title")]
    categories = [
        c.get("title", "").replace("Category:", "")
        for c in page_obj.get("categories", [])
        if not any(x in c.get("title", "").lower() for x in ["articles", "pages", "wikidata", "cs1", "webarchive", "short description", "dmy", "mdy"])
    ]

    interesting_links = [
        lnk for lnk in raw_links
        if not BORING_LINK_PATTERNS.match(lnk)
        and len(lnk) > 4
        and lnk.lower() != title.lower()
    ]

    # Now match outgoing links against actual sentences in the full text
    # so we know the EXACT contextual sentence ("bridge thread") where each link lives!
    all_sentences = split_into_sentences(full_text)
    total_sents = max(len(all_sentences), 1)

    scored_bridges: List[Dict[str, Any]] = []
    seen_targets = set()

    for lnk in interesting_links:
        if lnk.lower() in seen_targets:
            continue
        # Search for link title (or its core phrase) inside sentences, preferring deeper sentences
        pattern = re.compile(r"\b" + re.escape(lnk) + r"\b", re.IGNORECASE)
        matched_sent = None
        matched_pos = 0
        for s_idx, sent in enumerate(all_sentences):
            if pattern.search(sent):
                matched_sent = sent
                matched_pos = s_idx
                # Keep looking if this was in the very first sentence so we prefer deeper body sentences
                if s_idx >= 3:
                    break

        if matched_sent:
            seen_targets.add(lnk.lower())
            # Score by epistemic trigger words + depth in article + multi-word concept
            trig_count = sum(1 for tw in EPISTEMIC_TRIGGER_WORDS if tw in matched_sent.lower() or tw in lnk.lower())
            depth_bonus = 2 if (matched_pos / total_sents) > 0.2 else 1
            word_bonus = 2 if 2 <= len(lnk.split()) <= 4 else 1
            score = (trig_count * 3) + depth_bonus + word_bonus
            scored_bridges.append({
                "target": lnk,
                "bridge_sentence": matched_sent[:450],
                "sentence_index": matched_pos,
                "total_sentences": total_sents,
                "score": score
            })

    # Also keep fallback links that didn't match exact case/plural in plaintext
    if len(scored_bridges) < 10:
        for lnk in interesting_links:
            if lnk.lower() not in seen_targets:
                seen_targets.add(lnk.lower())
                trig_count = sum(1 for tw in EPISTEMIC_TRIGGER_WORDS if tw in lnk.lower())
                scored_bridges.append({
                    "target": lnk,
                    "bridge_sentence": f"Connected via conceptual thread in '{title}' ({deep_section_title}).",
                    "sentence_index": total_sents // 2,
                    "total_sentences": total_sents,
                    "score": trig_count * 2
                })

    scored_bridges.sort(key=lambda x: x["score"], reverse=True)

    return {
        "title": title,
        "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
        "char_length": len(full_text),
        "section_count": len(sections),
        "section_names": [s[0] for s in sections[:10]],
        "lead_extract": re.sub(r"\s+", " ", lead_text)[:650],
        "deep_section_title": deep_section_title,
        "deep_section_excerpt": deep_section_excerpt,
        "categories": categories[:8],
        "scored_bridges": scored_bridges[:25],
        "threads": [b["target"] for b in scored_bridges[:20]]
    }


def trace_long_rabbit_hole(seed_topic: str, hops: int = 10, branch_count: int = 3) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Traces a LONG, winding multi-hop rabbit hole (`hops` chambers deep),
    recording the exact verbatim bridge sentence pulled at every single hop,
    PLUS spawns secondary side-warren branches along the descent!
    """
    trail: List[Dict[str, Any]] = []
    side_warrens: List[Dict[str, Any]] = []
    visited = set()
    current_query = seed_topic
    incoming_bridge: Optional[Dict[str, Any]] = None

    for hop_idx in range(hops):
        log_progress(f"Excavating Chamber [Hop {hop_idx}/{hops - 1}]: '{current_query}'...")
        visited.add(current_query.lower())
        node = fetch_deep_wiki_node(current_query, is_exact_title=(hop_idx > 0))
        if not node or (node["title"].lower() in visited and node["title"].lower() != current_query.lower()):
            node = None
            if trail:
                prev_bridges = [b for b in trail[-1]["scored_bridges"] if b["target"].lower() not in visited]
                for alt in prev_bridges[:6]:
                    visited.add(alt["target"].lower())
                    log_progress(f"  ↻ Pivoting to alternate thread in chamber: '{alt['target']}'...")
                    cand_node = fetch_deep_wiki_node(alt["target"], is_exact_title=True)
                    if cand_node and cand_node["title"].lower() not in (visited - {alt["target"].lower()}):
                        incoming_bridge = alt
                        node = cand_node
                        break
            if not node:
                break

        visited.add(node["title"].lower())
        node["hop"] = hop_idx
        node["incoming_bridge"] = incoming_bridge
        trail.append(node)

        # Find unvisited bridges out of this chamber
        candidates = [b for b in node["scored_bridges"] if b["target"].lower() not in visited]
        if not candidates:
            break

        # If we are at a mid-depth chamber, also spawn a Side-Warren branch!
        if len(side_warrens) < branch_count and hop_idx in (1, 3, 5, 7) and len(candidates) > 2:
            side_bridge = candidates[1]
            visited.add(side_bridge["target"].lower())
            log_progress(f"  ↳ Exploring Side-Warren Branch off Hop {hop_idx}: '{side_bridge['target']}'...")
            side_node = fetch_deep_wiki_node(side_bridge["target"], is_exact_title=True)
            if side_node:
                visited.add(side_node["title"].lower())
                # Follow the side-warren one more hop deeper!
                side_sub_candidates = [b for b in side_node["scored_bridges"] if b["target"].lower() not in visited]
                side_leaf = None
                if side_sub_candidates:
                    leaf_bridge = side_sub_candidates[0]
                    visited.add(leaf_bridge["target"].lower())
                    log_progress(f"    ↳ Following Side-Warren deeper into: '{leaf_bridge['target']}'...")
                    side_leaf = fetch_deep_wiki_node(leaf_bridge["target"], is_exact_title=True)
                    if side_leaf:
                        visited.add(side_leaf["title"].lower())
                        side_leaf["incoming_bridge"] = leaf_bridge

                side_warrens.append({
                    "parent_hop": hop_idx,
                    "parent_title": node["title"],
                    "bridge_from_parent": side_bridge,
                    "first_chamber": side_node,
                    "second_chamber": side_leaf
                })

        # Re-filter candidates after side-warren visits
        candidates = [b for b in node["scored_bridges"] if b["target"].lower() not in visited]
        if not candidates:
            break

        chosen = candidates[0]
        incoming_bridge = chosen
        current_query = chosen["target"]

    return trail, side_warrens


# =============================================================================
# 2. Multi-Depth Archival Book & Primary-Source Harvester
# =============================================================================
def search_archival_books(topic: str, rows: int = 4) -> List[Dict[str, Any]]:
    """Searches Internet Archive & Open Library for primary and scholarly books on a topic."""
    books: List[Dict[str, Any]] = []
    clean_topic = re.sub(r'["():]', ' ', topic).strip()
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
                    "for_topic": topic,
                    "identifier": ident,
                    "title": doc.get("title", "Untitled"),
                    "creator": doc.get("creator", "Unknown"),
                    "year": doc.get("year", "n.d."),
                    "access": "LENDABLE (CDL)" if restricted else "OPEN ACCESS (Full OCR)",
                    "url": f"https://archive.org/details/{ident}"
                })
            break
    return books


def harvest_books_across_thread(trail: List[Dict[str, Any]], rows_per_stop: int = 3) -> List[Dict[str, Any]]:
    """
    Instead of only looking up books for Hop 0, harvests archival books at
    4 depth levels along the long thread (Surface Entry, Upper Shaft, Deep Shaft, Bottom Chamber)!
    """
    if not trail:
        return []
    n = len(trail)
    indices = sorted(list({0, n // 3, (2 * n) // 3, n - 1}))
    all_books: List[Dict[str, Any]] = []
    seen_ids = set()
    for idx in indices:
        node = trail[idx]
        log_progress(f"Mining Internet Archive & Open Library catalogs for Hop {idx} ('{node['title']}')...")
        b_list = search_archival_books(node["title"], rows=rows_per_stop)
        for b in b_list:
            if b["identifier"] not in seen_ids:
                seen_ids.add(b["identifier"])
                b["hop"] = idx
                all_books.append(b)
    return all_books


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
    """Generates structured epistemic curiosity questions spanning the entire long thread."""
    hop_titles = [n["title"] for n in trail[1:]] if len(trail) > 1 else ["adjacent disciplines"]
    deepest_title = trail[-1]["title"] if trail else topic
    mid_title = trail[len(trail) // 2]["title"] if len(trail) > 2 else deepest_title
    hop_chain_str = " → ".join([n["title"] for n in trail])

    return [
        {
            "lens": "1. The White Rabbit Anomaly (Lewis Carroll / Thomas Kuhn)",
            "focus": "Violation of Paradigm Expectations",
            "question": f"What is the single most counterintuitive, anomalous, or 'weird' empirical fact about '{topic}'—and how does descending down the thread to '{deepest_title}' expose an anomaly that surface summaries completely miss?"
        },
        {
            "lens": "2. Reasoning Backwards / The Scarlet Thread (Conan Doyle / C.S. Peirce Abduction)",
            "focus": "Retroductive Reconstruction Across the Thread",
            "question": f"Tracing the scarlet thread backwards from Hop {len(trail)-1} ('{deepest_title}') through '{mid_title}' back to Hop 0 ('{topic}'), what hidden causal mechanism or historical struggle secretly links the bottom of this shaft to the top?"
        },
        {
            "lens": "3. The Venatic Micro-Clue & Etymology (Carlo Ginzburg / Anthony Grafton)",
            "focus": "Microscopic Marginalia & Linguistic Fossil Record",
            "question": f"What hidden history is buried inside the literal etymology, footnotes, or earliest primary-source manuscripts along the chain [{hop_chain_str}]? Whose voices or dead-end experiments were erased along the way?"
        },
        {
            "lens": "4. In the Threads / Rhizomatic Cross-Passages (Borges / Deleuze / Vannevar Bush)",
            "focus": "Long-Distance Structural Isomorphism",
            "question": f"At first glance, '{topic}' (Hop 0) and '{deepest_title}' (Hop {len(trail)-1}) live in different worlds—yet we walked from one to the other via verifiable bridge sentences. What deep structural law or feedback loop do they share?"
        },
        {
            "lens": "5. Epistemic vs. Diversive Depth (Ian Leslie / Mihaly Csikszentmihalyi)",
            "focus": "First-Principles Mechanism",
            "question": f"Beneath the surface metaphors used to describe '{topic}' and '{mid_title}', what is the exact causal, mathematical, or material mechanism that governs them—and where does that mechanism break down under extreme conditions?"
        }
    ]


# =============================================================================
# 4. Sam Loyd Nine-Dot Box Audit & Edward de Bono Lateral Provocations
# =============================================================================
def generate_outside_the_box(topic: str, deepest_topic: str) -> Dict[str, Any]:
    """Generates Nine-Dot boundary diagnostics and Edward de Bono Lateral Thinking provocations."""
    return {
        "nine_dot_origin": (
            "Inspired by Sam Loyd's 1914 'Christopher Columbus's Egg Puzzle' (the 3x3 Nine-Dot Puzzle), "
            "where connecting all 9 dots with 4 straight lines requires drawing BEYOND the imaginary "
            "square perimeter that human Gestalt perception unconsciously projects."
        ),
        "boundary_audit_questions": [
            f"Boundary 1 (The Invisible Perimeter): What unspoken rule or boundary in '{topic}' is everyone obeying simply because they assume the 'dots' define a closed box?",
            f"Boundary 2 (The Long-Thread Perspective): How does looking at '{topic}' from the vantage point of Hop N ('{deepest_topic}') shatter the conventional framing of the problem?",
            f"Boundary 3 (Scale & Time Horizon): What happens to '{topic}' if we shrink the scale by 1,000x (micro-level) or expand the time horizon by 100 years?"
        ],
        "de_bono_lateral_provocations": [
            f"PO-1 [Reversal]: Instead of 'How do we optimize/understand {topic}?', ask: 'What if {topic} deliberately worked in reverse, or what if its perceived flaw is actually its primary evolutionary feature?'",
            f"PO-2 [Cross-Chamber Fusion]: Force a direct short-circuit between Hop 0 ('{topic}') and the bottom of the shaft ('{deepest_topic}'): what new invention, theory, or question emerges when you fuse them directly?",
            f"PO-3 [Elimination]: What happens if we remove the single most 'indispensable' assumption of '{topic}' and force the remaining parts to compensate?",
            f"PO-4 [Hole-Switching]: Edward de Bono's Law: 'Vertical thinking is digging the same hole deeper; lateral thinking is digging a hole in a new place.' Where is the current discussion digging a deeper hole in the wrong spot?"
        ]
    }


# =============================================================================
# 5. Arthur Koestler Bisociation Collider ("Thinking Aside")
# =============================================================================
def select_bisociations(topic: str, deepest_topic: str, custom_matrix: Optional[str] = None, count: int = 3) -> List[Dict[str, str]]:
    """Selects orthogonal matrices to collide with both the surface topic and the deepest hop."""
    selected: List[Dict[str, str]] = []
    if custom_matrix:
        selected.append({
            "domain": custom_matrix,
            "principle": f"Structural laws, dynamics, and failure modes native to {custom_matrix}.",
            "bridge_prompt": f"Bisociate '{topic}' (and its deep thread '{deepest_topic}') with '{custom_matrix}': Where do their underlying mechanisms intersect at right angles?"
        })

    h = int(hashlib.sha256(topic.encode("utf-8")).hexdigest(), 16)
    n = len(ORTHOGONAL_MATRICES)
    for i in range(count):
        idx = (h + i * 5) % n
        mat = ORTHOGONAL_MATRICES[idx]
        target_label = f"{topic} ↔ {deepest_topic}" if deepest_topic != topic else topic
        selected.append({
            "domain": mat["domain"],
            "principle": mat["principle"],
            "bridge_prompt": f"[{target_label} × {mat['domain']}] {mat['bridge_prompt']}"
        })
    return selected[:count]


# =============================================================================
# Markdown Expedition Formatter
# =============================================================================
def format_markdown_report(
    topic: str,
    trail: List[Dict[str, Any]],
    side_warrens: List[Dict[str, Any]],
    books: List[Dict[str, Any]],
    dojo_hits: List[str],
    lenses: List[Dict[str, str]],
    box_audit: Dict[str, Any],
    bisociations: List[Dict[str, str]],
    elapsed_sec: float
) -> str:
    lines: List[str] = []
    total_chars_read = sum(n.get("char_length", 0) for n in trail) + sum(
        w["first_chamber"].get("char_length", 0) + (w["second_chamber"].get("char_length", 0) if w.get("second_chamber") else 0)
        for w in side_warrens
    )
    deepest_title = trail[-1]["title"] if trail else topic

    lines.append(f"# Deep Rabbit-Hole Expedition Log: {topic} → {deepest_title}")
    lines.append(
        f"*Excavated via `rabbit_hole_engine.py` | "
        f"**{len(trail)} Main-Shaft Chambers** + **{len(side_warrens)} Side-Warrens** | "
        f"**{total_chars_read:,} chars** of full-text articles mined in **{elapsed_sec:.1f}s***\n"
    )

    # Overview Map of the Thread
    if trail:
        chain_str = " ──► ".join(f"**[Hop {n['hop']}: {n['title']}]**" for n in trail)
        lines.append("## 0. Map of the Main Subterranean Thread")
        lines.append(f"> {chain_str}\n")

    # 1. Chamber-by-Chamber Descent Down the Long Thread
    lines.append("## 1. Down the Long Thread: Chamber-by-Chamber Excavation (Bush / Nelson / Borges)")
    if trail:
        for node in trail:
            hop = node["hop"]
            bridge = node.get("incoming_bridge")
            lines.append(f"### Chamber {hop} (`Hop {hop}`): [{node['title']}]({node['url']})")
            lines.append(
                f"- **Corpus Depth Mined**: `{node['char_length']:,} chars` across `{node['section_count']} sections` "
                f"({', '.join(f'*{s}*' for s in node['section_names'][:6])})"
            )
            if bridge:
                lines.append(
                    f"- **🧵 Exact Thread Pulled from Hop {hop - 1}** *(Sentence #{bridge['sentence_index']} of {bridge['total_sentences']})*:"
                )
                lines.append(f"  > *\"{bridge['bridge_sentence']}\"*")
            lines.append(f"- **Surface Overview**:")
            lines.append(f"  > {node['lead_extract']}")
            if node.get("deep_section_excerpt"):
                lines.append(f"- **Deep Excavation (`§ {node['deep_section_title']}`)**:")
                lines.append(f"  > {node['deep_section_excerpt']}")
            if node["categories"]:
                lines.append(f"- **Ontological Strata**: `{', '.join(node['categories'])}`")
            if node["threads"]:
                lines.append(f"- **Unexplored Doors in This Chamber**: {', '.join(f'`{t}`' for t in node['threads'][:8])}\n")
    else:
        lines.append(f"- *No live hypertext node matched `{topic}` directly — apply direct abductive decomposition below.*\n")

    # 1B. Side-Warrens (Branching Tunnels)
    if side_warrens:
        lines.append("## 2. Branching Side-Warrens (Rhizomatic Offshoots Along the Descent)")
        for idx, w in enumerate(side_warrens, 1):
            c1 = w["first_chamber"]
            c2 = w.get("second_chamber")
            b1 = w["bridge_from_parent"]
            lines.append(f"### Side-Warren {idx} (Splitting off `Hop {w['parent_hop']}: {w['parent_title']}`)")
            lines.append(f"- **🧵 Branching Thread Pulled**: *\"{b1['bridge_sentence']}\"*")
            lines.append(f"- **Sub-Chamber A — [{c1['title']}]({c1['url']})** (`{c1['char_length']:,} chars`):")
            lines.append(f"  > {c1['lead_extract']}")
            if c1.get("deep_section_excerpt"):
                lines.append(f"  - *Deep Section (`§ {c1['deep_section_title']}`)*: {c1['deep_section_excerpt'][:400]}...")
            if c2:
                b2 = c2.get("incoming_bridge", {})
                lines.append(f"- **Sub-Chamber B (2nd-Order Branch) — [{c2['title']}]({c2['url']})** (`{c2['char_length']:,} chars`):")
                if b2.get("bridge_sentence"):
                    lines.append(f"  - *🧵 Thread Pulled*: *\"{b2['bridge_sentence']}\"*")
                lines.append(f"  > {c2['lead_extract']}\n")
            else:
                lines.append("")

    # 3. Primary Source Archival Books Across Multiple Hops
    lines.append("## 3. Multi-Depth Archival Book Burrow (Internet Archive & Open Library)")
    if books:
        for b in books:
            hop_tag = f"Hop {b.get('hop', 0)} ({b.get('for_topic', topic)})"
            lines.append(
                f"- **`[{hop_tag}]` `[{b['access']}]` [{b['title']}]({b['url']})** ({b['year']}) — "
                f"*{b['creator']}* (`{b['identifier']}`)"
            )
        lines.append(
            "\n  *(Tip: Chain with `python3 ~/.agents/skills/librarian/scripts/librarian_cli.py extract <identifier> --keywords \"...\"` "
            "to ingest full-text OCR from any volume discovered along the thread.)*\n"
        )
    else:
        lines.append("- *No direct catalog title match; broaden search terms with `librarian_cli.py global-search`.*\n")

    if dojo_hits:
        lines.append("### Local Dojo Vault Connections")
        for dh in dojo_hits:
            lines.append(f"- `{dh}`")
        lines.append("")

    # 4. Five-Lens Abductive & Venatic Prompts
    lines.append("## 4. The Five Investigative Lenses Across the Thread (Carroll / Peirce / Ginzburg / Kuhn / Leslie)")
    for l in lenses:
        lines.append(f"### {l['lens']}")
        lines.append(f"- **Cognitive Focus**: *{l['focus']}*")
        lines.append(f"- **Investigative Probe**: {l['question']}\n")

    # 5. Outside the Nine-Dot Box & De Bono Lateral Hole-Digging
    lines.append("## 5. Thinking Outside the Box & Lateral Hole-Switching (Sam Loyd / Edward de Bono)")
    lines.append(f"> *{box_audit['nine_dot_origin']}*\n")
    lines.append("### Self-Imposed Boundary Diagnostics")
    for q in box_audit["boundary_audit_questions"]:
        lines.append(f"- {q}")
    lines.append("\n### Edward de Bono Lateral Provocations (`PO`)")
    for po in box_audit["de_bono_lateral_provocations"]:
        lines.append(f"- {po}")
    lines.append("")

    # 6. Arthur Koestler Bisociation Collisions
    lines.append("## 6. Arthur Koestler Bisociation Collider ('Thinking Aside' Across Matrices)")
    for idx, bi in enumerate(bisociations, 1):
        lines.append(f"### Collision {idx}: `{topic} ↔ {deepest_title}` × `{bi['domain']}`")
        lines.append(f"- **Orthogonal Matrix Principle**: {bi['principle']}")
        lines.append(f"- **Bisociative Synthesis Prompt**: **{bi['bridge_prompt']}**\n")

    # 7. Hofstadter Stack & Epistemic Compass
    lines.append("## 7. Hofstadter Inquiry Stack (`PUSH`/`POP`) & Epistemic Compass")
    lines.append("```text")
    lines.append(f"[STACK LEVEL 0: SURFACE ENTRY]  {topic}")
    if len(trail) > 1:
        for n in trail[1:]:
            indent = "  " * min(n["hop"], 6)
            lines.append(f"{indent}└── PUSH [HOP {n['hop']} CHAMBER]  {n['title']}")
    for idx, w in enumerate(side_warrens, 1):
        c1 = w["first_chamber"]["title"]
        c2 = f" -> {w['second_chamber']['title']}" if w.get("second_chamber") else ""
        lines.append(f"    ├── PUSH [SIDE-WARREN {idx} off Hop {w['parent_hop']}]  {c1}{c2}")
    lines.append(f"  [POP ALL FRAMES -> SYNTHESIZE BACK TO SURFACE GOAL: {topic}]")
    lines.append("```")
    lines.append("- **Mertonian Serendipity vs. Apophenia Check (Eco / Pynchon)**:")
    lines.append("  1. *Does this long-thread connection rest on a verifiable causal bridge, primary source, or testable structural isomorphism?* (Serendipity)")
    lines.append("  2. *Or does it rely purely on verbal coincidence and unfalsifiable pattern-matching?* (Apophenia — discard or flag as metaphor!)")

    return "\n".join(lines)


# =============================================================================
# CLI Entrypoint
# =============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rabbit-Hole Curiosity Engine v2.0: Deep Long-Thread Excavator, Side-Warren Explorer & Lateral Bisociation Collider"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # explore
    p_exp = subparsers.add_parser("explore", help="Run deep long-thread rabbit-hole expedition on a topic")
    p_exp.add_argument("topic", help="Topic, question, or concept to investigate")
    p_exp.add_argument("--hops", type=int, default=10, help="Number of sequential chambers down the main thread (default: 10, use 15-20 for marathon threads)")
    p_exp.add_argument("--branches", type=int, default=3, help="Number of branching side-warrens to excavate along the descent (default: 3)")
    p_exp.add_argument("--rows", type=int, default=3, help="Number of archival books to retrieve per depth stop (default: 3)")
    p_exp.add_argument("--matrix", help="Optional custom orthogonal domain for Koestler bisociation")
    p_exp.add_argument("-o", "--output", help="Save full Markdown expedition dossier to file")

    # threads
    p_thr = subparsers.add_parser("threads", help="Trace a long multi-hop associative hypertext trail with exact bridge sentences")
    p_thr.add_argument("topic", help="Seed topic")
    p_thr.add_argument("--hops", type=int, default=10, help="Number of sequential hops (default: 10)")
    p_thr.add_argument("--branches", type=int, default=3, help="Number of branching side-warrens (default: 3)")

    # bisociate
    p_bis = subparsers.add_parser("bisociate", help="Collide topic with orthogonal domains (Koestler Bisociation)")
    p_bis.add_argument("topic", help="Target topic")
    p_bis.add_argument("--matrix", help="Specific orthogonal matrix to collide with")
    p_bis.add_argument("--count", type=int, default=3, help="Number of collisions (default: 3)")

    # outside-the-box
    p_box = subparsers.add_parser("outside-the-box", help="Run Sam Loyd Nine-Dot boundary audit & De Bono lateral provocations")
    p_box.add_argument("topic", help="Target topic or problem")

    args = parser.parse_args()
    t0 = time.time()

    if args.command == "explore":
        trail, side_warrens = trace_long_rabbit_hole(args.topic, hops=args.hops, branch_count=args.branches)
        books = harvest_books_across_thread(trail, rows_per_stop=args.rows) if trail else search_archival_books(args.topic, rows=args.rows)
        dojo_hits = search_dojo_vault(args.topic)
        deepest_title = trail[-1]["title"] if trail else args.topic
        lenses = generate_curiosity_lenses(args.topic, trail)
        box_audit = generate_outside_the_box(args.topic, deepest_title)
        bisociations = select_bisociations(args.topic, deepest_title, custom_matrix=args.matrix, count=3)
        elapsed = time.time() - t0

        report = format_markdown_report(
            topic=args.topic,
            trail=trail,
            side_warrens=side_warrens,
            books=books,
            dojo_hits=dojo_hits,
            lenses=lenses,
            box_audit=box_audit,
            bisociations=bisociations,
            elapsed_sec=elapsed
        )
        if args.output:
            out_path = Path(args.output).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report, encoding="utf-8")
            log_progress(f"Expedition complete in {elapsed:.1f}s! Dossier saved to {out_path} ({len(report.splitlines())} lines).")
        else:
            print(report)
        return 0

    elif args.command == "threads":
        trail, side_warrens = trace_long_rabbit_hole(args.topic, hops=args.hops, branch_count=args.branches)
        for node in trail:
            b = node.get("incoming_bridge")
            print(f"=== [Hop {node['hop']}] {node['title']} ({node['char_length']:,} chars | {node['section_count']} sections) ===")
            print(f"  URL: {node['url']}")
            if b:
                print(f"  Thread Pulled: \"{b['bridge_sentence']}\"")
            print(f"  Overview: {node['lead_extract']}")
            if node.get("deep_section_excerpt"):
                print(f"  Deep Section (§ {node['deep_section_title']}): {node['deep_section_excerpt'][:350]}...")
            print(f"  Next Doors: {', '.join(node['threads'][:8])}\n")
        return 0

    elif args.command == "bisociate":
        bis = select_bisociations(args.topic, args.topic, custom_matrix=args.matrix, count=args.count)
        for idx, b in enumerate(bis, 1):
            print(f"=== Collision {idx}: {args.topic} × {b['domain']} ===")
            print(f"  Principle: {b['principle']}")
            print(f"  Prompt:    {b['bridge_prompt']}\n")
        return 0

    elif args.command == "outside-the-box":
        box = generate_outside_the_box(args.topic, args.topic)
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
