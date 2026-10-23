#!/usr/bin/env python3
"""
rabbit_hole_engine.py (v3.0) - Coherent Long-Thread & Strange-Loop Curiosity Engine.

Key Architectural Principles:
1. Local Hop-to-Hop Coherence (0->1, 1->2, 2->3, 3->4, 4->5, 5->6...):
   Every hop transition is selected from genuine narrative prose (stripping out
   'See also', 'Bibliography', and 'Selected works' list dumps) and scored for
   direct conceptual continuity with both the current chamber (Hop k) and the
   preceding chamber (Hop k-1).
2. Overarching Ariadne's Thread (Tethered to Hop 0):
   At Hop 0, the engine builds a Seed Profile consisting of Hop 0's core conceptual
   vocabulary, outgoing links, and up to 500 Wikipedia Backlinks (pages across the
   encyclopedia that link directly back to Hop 0). Every downstream hop is scored
   against this Seed Profile so the thread never drifts into unrelated trivia.
3. The Return Arc / Strange Loop (Following It All the Way Back to the Beginning):
   In the final third of the descent, Return-Arc Gravity guides the thread into
   chambers that belong to Hop 0's backlink neighborhood, culminating in a verbatim
   "Closing Bridge Sentence" (Hop Final -> Hop 0) that brings the entire long
   thread full circle back to the beginning.

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
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set

USER_AGENT = "AntigravityRabbitHoleEngine/3.0 (https://github.com/Beardedfreedom/rabbit-hole-curiosity; epistemic-research@github.com) Python-urllib/3"
TIMEOUT = 15

STOPWORDS: Set[str] = {
    "about", "above", "after", "again", "against", "all", "also", "although", "always",
    "among", "an", "and", "another", "any", "are", "around", "as", "at", "back", "be",
    "became", "because", "become", "becomes", "been", "before", "began", "being", "below",
    "between", "both", "but", "by", "call", "called", "came", "can", "cannot", "century",
    "city", "come", "could", "day", "days", "did", "different", "do", "does", "done",
    "down", "during", "each", "early", "either", "end", "english", "even", "every",
    "example", "examples", "first", "five", "following", "for", "form", "forms", "found",
    "four", "from", "further", "gave", "general", "get", "given", "give", "good", "great",
    "group", "had", "has", "have", "having", "he", "her", "here", "high", "him", "himself",
    "his", "history", "how", "however", "if", "important", "in", "include", "included",
    "includes", "including", "into", "is", "it", "its", "itself", "just", "keep", "kind",
    "known", "large", "later", "late", "lead", "led", "less", "life", "like", "line",
    "list", "little", "long", "made", "main", "major", "make", "makes", "making", "man",
    "many", "may", "mean", "means", "men", "might", "more", "most", "mostly", "much",
    "must", "my", "name", "named", "national", "near", "need", "never", "new", "next",
    "no", "non", "nor", "not", "now", "number", "of", "off", "often", "old", "on", "once",
    "one", "only", "or", "order", "other", "others", "our", "out", "over", "own", "page",
    "part", "particular", "parts", "past", "people", "per", "period", "person", "place",
    "placed", "point", "popular", "possible", "power", "present", "public", "published",
    "put", "rather", "related", "result", "results", "right", "same", "saw", "say", "says",
    "second", "see", "seem", "seemed", "seems", "seen", "several", "shall", "she", "should",
    "show", "showed", "shown", "shows", "side", "similar", "since", "six", "small", "so",
    "some", "something", "sometimes", "state", "states", "still", "study", "such", "system",
    "take", "taken", "takes", "taking", "term", "terms", "than", "that", "the", "their",
    "them", "themselves", "then", "there", "therefore", "these", "they", "thing", "things",
    "think", "third", "this", "those", "though", "three", "through", "thus", "time",
    "times", "to", "together", "told", "too", "took", "toward", "towards", "two", "type",
    "types", "under", "united", "university", "until", "up", "upon", "us", "use", "used",
    "uses", "using", "usually", "various", "very", "was", "way", "ways", "we", "well",
    "went", "were", "what", "when", "where", "whether", "which", "while", "who", "whole",
    "whom", "whose", "why", "will", "with", "within", "without", "word", "words", "work",
    "worked", "working", "works", "world", "would", "write", "written", "wrote", "year",
    "years", "yet", "you", "young", "your",
    "john", "william", "charles", "robert", "james", "thomas", "george", "henry", "edward",
    "richard", "david", "michael", "peter", "paul", "mary", "anne", "joseph", "francis",
    "louis", "alexander", "horace", "arthur", "stephen", "martin", "walter", "frank", "albert"
}

NON_PROSE_SECTIONS: Set[str] = {
    "see also", "notes", "references", "bibliography", "further reading",
    "external links", "selected works", "works", "publications", "sources",
    "citations", "footnotes", "awards", "honors", "honours", "filmography",
    "discography", "gallery", "patents", "notable people", "notable alumni"
}

BORING_LINK_PATTERNS = re.compile(
    r"^(ISBN|DOI|ISSN|OCLC|PMID|S2CID|Wayback Machine|Bibcode|ArXiv|Wikidata|"
    r"List of |Index of |Outline of |Category:|Help:|Portal:|Template:|Special:|"
    r"\d{1,4}|January|February|March|April|May|June|July|August|September|October|November|December|"
    r"United States|United Kingdom|France|Germany|Italy|Spain|China|Japan|Russia|Canada|Australia|"
    r"England|Scotland|Ireland|Europe|Asia|Africa|North America|South America|"
    r"New York|London|Paris|Berlin|Rome|Oxford|Cambridge|Leeds|Yorkshire|Chicago|Boston|California|"
    r"Latin|Greek|English|French|German|Spanish|Italian|Arabic|Sanskrit|Persian|Chinese|"
    r"University of .*|.* University|.* College|.* Institute|Doi \(identifier\)|ISBN \(identifier\)|"
    r"PMID \(identifier\)|ISSN \(identifier\)|S2CID \(identifier\)|OCLC \(identifier\))$",
    re.IGNORECASE
)

EPISTEMIC_TRIGGER_WORDS = [
    "paradox", "anomaly", "unexpected", "mysterious", "controvers", "accident",
    "serendipit", "coined", "origin", "beneath", "hidden", "secret", "contrary",
    "puzzle", "labyrinth", "thread", "unlikely", "discovered", "discovery",
    "strange", "curious", "curiosity", "assumption", "illusion", "breakthrough",
    "hypothesis", "experiment", "philosoph", "psycholog", "mechanism", "cognition",
    "cognitive", "heuristic", "abduct", "induct", "deduct", "intuition", "insight",
    "creativ", "innovation", "pattern", "network", "emergenc", "unintended"
]

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


def tokenize_keywords(text: str, min_len: int = 4) -> List[str]:
    """Extracts meaningful lowercase content tokens from text."""
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    return [w for w in words if len(w) >= min_len and w not in STOPWORDS]


def extract_top_keywords(text: str, top_k: int = 60) -> Dict[str, int]:
    """Returns top_k content words and their frequencies."""
    counts = Counter(tokenize_keywords(text))
    return dict(counts.most_common(top_k))


# =============================================================================
# 1. Deep Prose-Only Node Excavator & Backlink Mapper
# =============================================================================
def extract_prose_sections(full_text: str) -> List[Tuple[str, str]]:
    """
    Extracts named sections (== Section ==) from Wikipedia plaintext extract,
    strictly discarding non-prose list/reference sections ('See also', 'Bibliography', etc.).
    """
    parts = re.split(r"\n(==+\s*[^=]+\s*==+)\n", full_text)
    sections: List[Tuple[str, str]] = [("Lead / Surface Overview", parts[0].strip())]
    idx = 1
    while idx + 1 < len(parts):
        header = parts[idx].strip("= \t")
        body = parts[idx + 1].strip()
        header_low = header.lower()
        if any(bad in header_low for bad in NON_PROSE_SECTIONS):
            # If we hit References / See also / Notes at the end of the article, skip
            idx += 2
            continue
        if body and len(body) > 80:
            sections.append((header, body))
        idx += 2
    return sections


def split_into_prose_sentences(prose_sections: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    Splits only genuine prose sections into (section_name, sentence) pairs,
    rejecting citation dumps, headers, and list fragments.
    """
    results: List[Tuple[str, str]] = []
    for sec_name, sec_body in prose_sections:
        cleaned = re.sub(r"\s+", " ", sec_body)
        raw = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[])", cleaned)
        for s in raw:
            s_str = s.strip()
            if len(s_str) < 45 or len(s_str) > 550:
                continue
            if "==" in s_str or "ISBN " in s_str or "doi:" in s_str or "pp. " in s_str:
                continue
            results.append((sec_name, s_str))
    return results


def fetch_backlinks(title: str, limit: int = 350) -> Set[str]:
    """Fetches up to `limit` Wikipedia pages that link directly BACK to `title`."""
    params = urllib.parse.urlencode({
        "action": "query",
        "list": "backlinks",
        "bltitle": title,
        "blnamespace": "0",
        "bllimit": str(min(limit, 500)),
        "format": "json"
    })
    data = http_get_json(f"https://en.wikipedia.org/w/api.php?{params}")
    if not data:
        return set()
    bls = data.get("query", {}).get("backlinks", [])
    return {
        b["title"] for b in bls
        if b.get("title") and not BORING_LINK_PATTERNS.match(b["title"])
    }


def fetch_raw_wiki_article(query_or_title: str, is_exact_title: bool = False) -> Optional[Dict[str, Any]]:
    """Downloads the raw Wikipedia full text, links, and categories for a node."""
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

    prop_params = urllib.parse.urlencode({
        "action": "query",
        "titles": title,
        "redirects": "1",
        "prop": "extracts|links|categories",
        "explaintext": "1",
        "pllimit": "350",
        "plnamespace": "0",
        "cllimit": "25",
        "format": "json"
    })
    time.sleep(0.3)
    page_data = http_get_json(f"https://en.wikipedia.org/w/api.php?{prop_params}")
    if not page_data:
        return None

    pages = page_data.get("query", {}).get("pages", {})
    page_obj = next(iter(pages.values()), {})
    title = page_obj.get("title", title)
    full_text = page_obj.get("extract", "").strip()
    if not full_text:
        return None

    prose_sections = extract_prose_sections(full_text)
    prose_text = "\n\n".join(sec_body for _, sec_body in prose_sections)
    lead_text = prose_sections[0][1] if prose_sections else full_text[:1000]

    # Pick a rich deep prose section
    deep_section_title = "Deep Subterranean Section"
    deep_section_excerpt = ""
    for sec_title, sec_body in prose_sections[1:]:
        if len(sec_body) > 200:
            deep_section_title = sec_title
            deep_section_excerpt = re.sub(r"\s+", " ", sec_body)[:700]
            if any(k in sec_title.lower() for k in [
                "history", "origin", "etymology", "mechanism", "theory", "paradox",
                "criticism", "controversy", "example", "discovery", "psychology", "philosophy"
            ]):
                break

    raw_links = [l.get("title", "") for l in page_obj.get("links", []) if l.get("title")]
    categories = [
        c.get("title", "").replace("Category:", "")
        for c in page_obj.get("categories", [])
        if not any(x in c.get("title", "").lower() for x in [
            "articles", "pages", "wikidata", "cs1", "webarchive", "short description", "dmy", "mdy", "stubs"
        ])
    ]

    interesting_links = [
        lnk for lnk in raw_links
        if not BORING_LINK_PATTERNS.match(lnk)
        and len(lnk) > 4
        and lnk.lower() != title.lower()
    ]

    prose_sentences = split_into_prose_sentences(prose_sections)
    node_keywords = extract_top_keywords(prose_text, top_k=60)

    return {
        "title": title,
        "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
        "char_length": len(full_text),
        "section_count": len(prose_sections),
        "section_names": [s[0] for s in prose_sections[:10]],
        "lead_extract": re.sub(r"\s+", " ", lead_text)[:650],
        "deep_section_title": deep_section_title,
        "deep_section_excerpt": deep_section_excerpt,
        "categories": categories[:8],
        "interesting_links": interesting_links,
        "prose_sentences": prose_sentences,
        "node_keywords": node_keywords
    }


def score_node_bridges(
    node: Dict[str, Any],
    seed_profile: Dict[str, Any],
    prev_node: Optional[Dict[str, Any]],
    hop_idx: int,
    total_hops: int,
    visited: Set[str],
    used_seed_terms: Optional[Counter] = None,
    visited_title_tokens: Optional[Counter] = None
) -> List[Dict[str, Any]]:
    """
    Scores every outgoing link in `node` that appears inside a genuine prose sentence:
    - Local Connection Score (Hop k-1 -> Hop k -> Candidate):
      Shared conceptual vocabulary with current node and previous node.
    - Overarching Ariadne's Thread Score (Hop 0 <-> Candidate):
      Shared conceptual vocabulary with `seed_profile['keywords']` (with diversity
      weighting so the thread explores new facets of Hop 0 rather than getting stuck
      on a single repeated word), plus membership in `seed_profile['backlinks']`.
    - Return-Arc Gravity (in the second half of the thread):
      Strongly rewards candidates in `seed_profile['backlinks']` (pages that link
      directly back to Hop 0!) so the thread arches back to the beginning!
    """
    seed_kw: Dict[str, int] = seed_profile["keywords"]
    seed_outlinks_low: Set[str] = seed_profile["outlinks_low"]
    seed_backlinks_low: Set[str] = seed_profile["backlinks_low"]
    seed_stem: str = seed_profile["stem"]
    used_counts = used_seed_terms or Counter()
    title_token_counts = visited_title_tokens or Counter()

    curr_kw: Dict[str, int] = node["node_keywords"]
    prev_kw: Dict[str, int] = prev_node["node_keywords"] if prev_node else curr_kw

    prose_sentences: List[Tuple[str, str]] = node["prose_sentences"]
    total_sents = max(len(prose_sentences), 1)

    scored_bridges: List[Dict[str, Any]] = []
    seen_targets: Set[str] = set()

    # How far along the descent are we? (0.0 at start -> 1.0 at final hop)
    progress_ratio = hop_idx / max(total_hops - 1, 1)

    for lnk in node["interesting_links"]:
        lnk_low = lnk.lower()
        if lnk_low in visited or lnk_low in seen_targets:
            continue

        clean_lnk = re.sub(r"\s*\([^)]*\)\s*", "", lnk).strip()
        if len(clean_lnk) < 4:
            continue
        pattern = re.compile(r"\b" + re.escape(clean_lnk) + r"\b", re.IGNORECASE)
        best_match: Optional[Tuple[int, str, str, float, List[str], List[str]]] = None
        exhausted_terms = {t for t, c in used_counts.items() if c >= 2}

        for s_idx, (sec_name, sent) in enumerate(prose_sentences):
            if pattern.search(sent):
                sent_tokens = set(tokenize_keywords(sent + " " + clean_lnk))
                # Shared tokens with Seed (Hop 0), excluding saturated terms
                shared_seed = [t for t in sent_tokens if (t in seed_kw or seed_stem in t) and t not in exhausted_terms]
                # Shared tokens with Current & Previous Hop (Local Continuity), excluding saturated terms
                shared_local = [t for t in sent_tokens if (t in curr_kw or t in prev_kw) and t not in exhausted_terms]

                # Reward fresh seed terms much more than already-used seed terms so the thread arches across facets
                seed_diversity_score = sum(5.5 / (1.0 + 2.5 * used_counts[t]) for t in shared_seed)
                trig_count = sum(1 for tw in EPISTEMIC_TRIGGER_WORDS if tw in sent.lower() or tw in lnk_low)
                cand_score = seed_diversity_score + (len(shared_local) * 2.0) + (trig_count * 3.0)

                if best_match is None or cand_score > best_match[3]:
                    best_match = (s_idx, sec_name, sent, cand_score, shared_seed[:6], shared_local[:6])

        if best_match:
            s_idx, sec_name, sent, base_score, shared_seed, shared_local = best_match
            seen_targets.add(lnk_low)

            is_in_backlinks = lnk_low in seed_backlinks_low
            is_in_outlinks = lnk_low in seed_outlinks_low

            # Overarching Ariadne's Thread bonus
            ariadne_bonus = 0.0
            if is_in_backlinks:
                # Backlinks are pages that literally link back to Hop 0!
                ariadne_bonus += 22.0 + (85.0 * (progress_ratio ** 1.2))
            if is_in_outlinks and hop_idx <= 3:
                ariadne_bonus += 8.0

            # Penalize candidates whose title repeats words already used in earlier chamber titles or exhausted terms
            cand_title_tokens = set(tokenize_keywords(clean_lnk))
            repeated_title_penalty = sum(18.0 * title_token_counts[t] for t in cand_title_tokens if title_token_counts[t] > 0)
            exhausted_title_penalty = sum(22.0 for t in cand_title_tokens if t in exhausted_terms)
            base_score -= (repeated_title_penalty + exhausted_title_penalty)

            # Penalize candidates that have ZERO connection to Hop 0's conceptual universe
            if not shared_seed and not is_in_backlinks and not is_in_outlinks:
                base_score -= 18.0

            # Penalize single-word proper names that look like tangential people/places unless backlinked
            words = clean_lnk.split()
            if len(words) == 1 and clean_lnk[0].isupper() and not is_in_backlinks and not any(tw in lnk_low for tw in EPISTEMIC_TRIGGER_WORDS):
                base_score -= 6.0

            total_score = int(round(base_score + ariadne_bonus))
            scored_bridges.append({
                "target": lnk,
                "section_name": sec_name,
                "bridge_sentence": sent,
                "sentence_index": s_idx + 1,
                "total_sentences": total_sents,
                "shared_seed_terms": shared_seed,
                "shared_local_terms": shared_local,
                "links_back_to_origin": is_in_backlinks,
                "score": total_score
            })

    scored_bridges.sort(key=lambda x: x["score"], reverse=True)
    return scored_bridges[:60]


def find_closing_loop_bridge(final_node: Dict[str, Any], seed_node: Dict[str, Any], seed_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finds the exact sentence or conceptual bridge in the Final Chamber (`Hop N-1`)
    that loops all the way back to `Hop 0` (the Beginning)!
    """
    seed_title = seed_node["title"]
    seed_stem = seed_profile["stem"]
    seed_kw = seed_profile["keywords"]

    # 1. Look for a sentence in `final_node` that explicitly mentions `seed_title` or `seed_stem`
    for s_idx, (sec_name, sent) in enumerate(final_node["prose_sentences"]):
        if seed_stem in sent.lower() or seed_title.lower() in sent.lower():
            return {
                "type": "Direct Verbatim Strange-Loop Bridge",
                "section": sec_name,
                "sentence_index": s_idx + 1,
                "total_sentences": len(final_node["prose_sentences"]),
                "sentence": sent,
                "shared_concepts": [t for t in tokenize_keywords(sent) if t in seed_kw][:8]
            }

    # 2. Otherwise, find the sentence in `final_node` with the highest density of `Hop 0` seed keywords
    best_sent = ""
    best_sec = "Lead / Surface Overview"
    best_idx = 1
    best_shared: List[str] = []
    for s_idx, (sec_name, sent) in enumerate(final_node["prose_sentences"]):
        tokens = set(tokenize_keywords(sent))
        shared = [t for t in tokens if t in seed_kw]
        if len(shared) > len(best_shared):
            best_shared = shared
            best_sent = sent
            best_sec = sec_name
            best_idx = s_idx + 1

    # Also check if `seed_node` itself mentions `final_node["title"]`
    reverse_mention = None
    for s_idx, (sec_name, sent) in enumerate(seed_node["prose_sentences"]):
        if final_node["title"].lower() in sent.lower():
            reverse_mention = f"(And in Hop 0 '{seed_title}', § {sec_name}: \"{sent}\")"
            break

    full_closing_sent = best_sent
    if reverse_mention:
        full_closing_sent = f"{best_sent} {reverse_mention}"

    return {
        "type": "Thematic Strange-Loop Convergence",
        "section": best_sec,
        "sentence_index": best_idx,
        "total_sentences": max(len(final_node["prose_sentences"]), 1),
        "sentence": full_closing_sent or final_node["lead_extract"][:350],
        "shared_concepts": best_shared[:8]
    }


def trace_coherent_rabbit_hole(
    seed_topic: str,
    hops: int = 10,
    branch_count: int = 3
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    """
    Traces a coherent, Ariadne-tethered `hops`-deep rabbit hole where:
    - Hop 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 are each connected by
      genuine narrative prose sentences and local + overarching thematic overlap.
    - The final hops bend along a Return Arc into Hop 0's backlink neighborhood,
      closing the Strange Loop all the way back to Hop 0!
    """
    trail: List[Dict[str, Any]] = []
    side_warrens: List[Dict[str, Any]] = []
    visited: Set[str] = set()

    log_progress(f"Excavating Entry Chamber [Hop 0/{hops - 1}]: '{seed_topic}'...")
    seed_node = fetch_raw_wiki_article(seed_topic, is_exact_title=False)
    if not seed_node:
        return [], [], {}, {}

    seed_title = seed_node["title"]
    visited.add(seed_title.lower())
    log_progress(f"Mapping Ariadne's Thread & Return-Arc Backlinks for '{seed_title}'...")
    backlinks = fetch_backlinks(seed_title, limit=400)
    log_progress(f"  ↳ Mapped {len(backlinks)} backlink chambers that point back to '{seed_title}'.")

    # Build the Overarching Seed Profile (`Ariadne's Thread`)
    seed_words = re.findall(r"[a-zA-Z]{4,}", seed_title.lower())
    seed_stem = seed_words[0][:6] if seed_words else seed_title.lower()[:6]
    seed_profile: Dict[str, Any] = {
        "title": seed_title,
        "stem": seed_stem,
        "keywords": seed_node["node_keywords"],
        "outlinks_low": {l.lower() for l in seed_node["interesting_links"]},
        "backlinks_low": {b.lower() for b in backlinks},
        "backlinks_titles": list(backlinks)
    }

    used_seed_terms: Counter = Counter()
    visited_title_tokens: Counter = Counter()
    for t in tokenize_keywords(seed_title):
        visited_title_tokens[t] += 1

    # Score bridges out of Hop 0
    seed_node["hop"] = 0
    seed_node["incoming_bridge"] = None
    seed_node["scored_bridges"] = score_node_bridges(
        node=seed_node,
        seed_profile=seed_profile,
        prev_node=None,
        hop_idx=0,
        total_hops=hops,
        visited=visited,
        used_seed_terms=used_seed_terms,
        visited_title_tokens=visited_title_tokens
    )
    seed_node["threads"] = [b["target"] for b in seed_node["scored_bridges"][:15]]
    trail.append(seed_node)

    # Walk Hops 1 .. hops - 1
    for hop_idx in range(1, hops):
        prev_node = trail[-1]
        candidates = [b for b in prev_node["scored_bridges"] if b["target"].lower() not in visited]
        if not candidates:
            break

        # On the very last hop (`hop_idx == hops - 1`), strongly prefer a candidate that links directly back to Hop 0!
        if hop_idx == hops - 1:
            backlink_cands = [b for b in candidates if b.get("links_back_to_origin")]
            # Also find high-affinity backlinks to Hop 0 whose concepts/words appear in Hop N-2's prose
            prev_kw = prev_node["node_keywords"]
            scored_bl: List[Tuple[float, str]] = []
            for bl_title in seed_profile["backlinks_titles"]:
                bl_low = bl_title.lower()
                if bl_low in visited or BORING_LINK_PATTERNS.match(bl_title):
                    continue
                if len(bl_title.split()) > 5 or any(w in bl_low for w in (
                    "program", "university", "department", "faculty", "school", "institute",
                    "college", "episode", "album", "song", "film", "collection)", "novel)",
                    "book)", "series)", "game)", "band)", "magazine)", "journal)"
                )):
                    continue
                bl_tokens = tokenize_keywords(bl_title)
                if not bl_tokens:
                    continue
                overlap_prev = sum(8.0 for t in bl_tokens if t in prev_kw) / (len(bl_tokens) ** 0.5)
                overlap_seed = sum(4.0 / (1.0 + used_seed_terms[t]) for t in bl_tokens if t in seed_profile["keywords"])
                title_pen = sum(8.0 * visited_title_tokens[t] for t in bl_tokens)
                # Bonus if any token of bl_title appears directly in prev_node's prose
                in_prev_prose = any(any(t in s_txt.lower() for _, s_txt in prev_node["prose_sentences"]) for t in bl_tokens)
                prose_bonus = 10.0 if in_prev_prose else 0.0
                if overlap_prev > 0 or in_prev_prose:
                    scored_bl.append((overlap_prev + overlap_seed + prose_bonus - title_pen, bl_title))
            scored_bl.sort(key=lambda x: x[0], reverse=True)
            synth_cands: List[Dict[str, Any]] = []
            for _, bl_title in scored_bl[:6]:
                bl_tokens = set(tokenize_keywords(bl_title))
                best_s_idx = 0
                best_sec = "Lead / Surface Overview"
                best_sent = prev_node["prose_sentences"][0][1] if prev_node["prose_sentences"] else prev_node["lead_extract"]
                best_shared_loc: List[str] = []
                best_score_loc = -1.0
                for s_i, (sec_n, s_txt) in enumerate(prev_node["prose_sentences"]):
                    s_toks = set(tokenize_keywords(s_txt))
                    direct_bl_hits = [t for t in s_toks if t in bl_tokens]
                    loc = [t for t in s_toks if t in bl_tokens or t in prev_kw]
                    s_score = len(direct_bl_hits) * 5.0 + len(loc)
                    if s_score > best_score_loc:
                        best_score_loc = s_score
                        best_shared_loc = direct_bl_hits + [t for t in loc if t not in direct_bl_hits]
                        best_s_idx = s_i
                        best_sec = sec_n
                        best_sent = s_txt
                synth_cands.append({
                    "target": bl_title,
                    "section_name": best_sec,
                    "bridge_sentence": best_sent,
                    "sentence_index": best_s_idx + 1,
                    "total_sentences": max(len(prev_node["prose_sentences"]), 1),
                    "shared_seed_terms": [t for t in best_shared_loc if t in seed_profile["keywords"]][:5] or [seed_stem],
                    "shared_local_terms": best_shared_loc[:6],
                    "links_back_to_origin": True,
                    "score": 85
                })
            candidates = backlink_cands + synth_cands + [b for b in candidates if not b.get("links_back_to_origin")]

        chosen_node = None
        chosen_bridge = None
        fallback_pair: Optional[Tuple[Dict[str, Any], Dict[str, Any]]] = None

        for cand_idx, cand in enumerate(candidates[:6]):
            target_title = cand["target"]
            visited.add(target_title.lower())
            log_progress(
                f"Excavating Chamber [Hop {hop_idx}/{hops - 1}]: '{target_title}' "
                f"(via § {cand['section_name']} | Tether: {', '.join(cand['shared_seed_terms'][:3]) or 'backlink'})..."
            )
            raw_node = fetch_raw_wiki_article(target_title, is_exact_title=True)
            if raw_node and raw_node["title"].lower() not in (visited - {target_title.lower()}):
                visited.add(raw_node["title"].lower())
                raw_node["hop"] = hop_idx
                raw_node["incoming_bridge"] = cand
                raw_node["scored_bridges"] = score_node_bridges(
                    node=raw_node,
                    seed_profile=seed_profile,
                    prev_node=prev_node,
                    hop_idx=hop_idx,
                    total_hops=hops,
                    visited=visited,
                    used_seed_terms=used_seed_terms,
                    visited_title_tokens=visited_title_tokens
                )
                raw_node["threads"] = [b["target"] for b in raw_node["scored_bridges"][:15]]
                # Make sure this node isn't a dead-end stub if we still have hops to go
                if hop_idx < hops - 1 and len(raw_node["scored_bridges"]) == 0:
                    log_progress(f"  ↻ Chamber '{target_title}' is a leaf stub; pivoting to next coherent thread...")
                    continue

                # Prefer rich, deep chambers (>4,500 chars and >=8 outgoing prose bridges) over short stubs
                if hop_idx < hops - 1 and (raw_node["char_length"] < 4500 or len(raw_node["scored_bridges"]) < 8) and cand_idx < 4:
                    if fallback_pair is None:
                        fallback_pair = (raw_node, cand)
                    log_progress(f"  ↻ Chamber '{target_title}' is shallow ({raw_node['char_length']:,} chars); checking next deeper chamber...")
                    continue

                # On penultimate hop (hops - 2), prefer a chamber that directly links to a Hop 0 backlink!
                if hop_idx == hops - 2:
                    has_backlink_exit = any(b.get("links_back_to_origin") for b in raw_node["scored_bridges"])
                    if not has_backlink_exit and cand_idx < 3:
                        if fallback_pair is None:
                            fallback_pair = (raw_node, cand)
                        log_progress(f"  ↻ Checking if an alternate Hop {hop_idx} chamber has a direct bridge into Hop 0's backlink horizon...")
                        continue

                # On final hop (hops - 1), strongly prefer a chamber whose narrative prose explicitly mentions Hop 0!
                if hop_idx == hops - 1:
                    mentions_seed_in_prose = any(
                        seed_stem in s_txt.lower() or seed_title.lower() in s_txt.lower()
                        for _, s_txt in raw_node["prose_sentences"]
                    )
                    if not mentions_seed_in_prose and cand_idx < 5:
                        if fallback_pair is None:
                            fallback_pair = (raw_node, cand)
                        log_progress(f"  ↻ Seeking a Hop {hop_idx} chamber with a verbatim narrative bridge back to '{seed_title}'...")
                        continue

                chosen_node = raw_node
                chosen_bridge = cand
                break

        if not chosen_node and fallback_pair:
            chosen_node, chosen_bridge = fallback_pair

        if not chosen_node:
            break

        # Update diversity counters so the thread arches across new facets of Hop 0
        if chosen_bridge:
            for t in set(chosen_bridge.get("shared_seed_terms", []) + chosen_bridge.get("shared_local_terms", [])):
                used_seed_terms[t] += 1
        for t in tokenize_keywords(chosen_node["title"]):
            visited_title_tokens[t] += 1
            used_seed_terms[t] += 1

        trail.append(chosen_node)

        # Spawn a coherent Side-Warren branch at mid-depths (Hops 1, 3, 5)
        rem_candidates = [b for b in prev_node["scored_bridges"] if b["target"].lower() not in visited]
        if len(side_warrens) < branch_count and hop_idx in (2, 4, 6) and rem_candidates:
            side_bridge = rem_candidates[0]
            visited.add(side_bridge["target"].lower())
            log_progress(f"  ↳ Exploring Coherent Side-Warren off Hop {hop_idx - 1}: '{side_bridge['target']}'...")
            side_node = fetch_raw_wiki_article(side_bridge["target"], is_exact_title=True)
            if side_node:
                visited.add(side_node["title"].lower())
                side_node["scored_bridges"] = score_node_bridges(
                    node=side_node,
                    seed_profile=seed_profile,
                    prev_node=prev_node,
                    hop_idx=hop_idx,
                    total_hops=hops,
                    visited=visited
                )
                side_leaf = None
                if side_node["scored_bridges"]:
                    leaf_bridge = side_node["scored_bridges"][0]
                    visited.add(leaf_bridge["target"].lower())
                    log_progress(f"    ↳ Following Side-Warren deeper into: '{leaf_bridge['target']}'...")
                    side_leaf = fetch_raw_wiki_article(leaf_bridge["target"], is_exact_title=True)
                    if side_leaf:
                        visited.add(side_leaf["title"].lower())
                        side_leaf["incoming_bridge"] = leaf_bridge

                side_warrens.append({
                    "parent_hop": hop_idx - 1,
                    "parent_title": prev_node["title"],
                    "bridge_from_parent": side_bridge,
                    "first_chamber": side_node,
                    "second_chamber": side_leaf
                })

    # Construct the Closing Bridge (`Hop Final -> Hop 0`) to follow the thread all the way back to the beginning!
    closing_loop = {}
    if len(trail) > 1:
        log_progress(f"Closing the Strange Loop: Tracing Return Thread from Hop {len(trail)-1} ('{trail[-1]['title']}') back to Hop 0 ('{seed_title}')...")
        closing_loop = find_closing_loop_bridge(trail[-1], seed_node, seed_profile)

    return trail, side_warrens, seed_profile, closing_loop


# =============================================================================
# 2. Multi-Depth Archival Book & Primary-Source Harvester
# =============================================================================
def search_archival_books(topic: str, rows: int = 3) -> List[Dict[str, Any]]:
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
    """Harvests archival books at 4 depth levels along the long thread."""
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
    """Generates structured epistemic curiosity questions spanning the entire circular thread."""
    deepest_title = trail[-1]["title"] if trail else topic
    mid_title = trail[len(trail) // 2]["title"] if len(trail) > 2 else deepest_title
    hop_chain_str = " → ".join([n["title"] for n in trail]) + f" ↺ {topic}"

    return [
        {
            "lens": "1. The White Rabbit Anomaly (Lewis Carroll / Thomas Kuhn)",
            "focus": "Violation of Paradigm Expectations",
            "question": f"What is the single most counterintuitive, anomalous, or 'weird' empirical fact about '{topic}'—and how does descending down the thread through '{mid_title}' to '{deepest_title}' expose a deeper mechanism that surface summaries miss?"
        },
        {
            "lens": "2. Reasoning Backwards / The Scarlet Thread (Conan Doyle / C.S. Peirce Abduction)",
            "focus": "Retroductive Reconstruction Across the Loop",
            "question": f"Following the scarlet thread from '{topic}' (Hop 0) down to '{deepest_title}' (Hop {len(trail)-1}) and back again, what hidden causal law or historical struggle binds every chamber in this loop together?"
        },
        {
            "lens": "3. The Venatic Micro-Clue & Etymology (Carlo Ginzburg / Anthony Grafton)",
            "focus": "Microscopic Marginalia & Linguistic Fossil Record",
            "question": f"What hidden history is buried inside the literal etymology, footnotes, or earliest primary-source manuscripts along the circular trail [{hop_chain_str}]?"
        },
        {
            "lens": "4. In the Threads / The Strange Loop (Hofstadter / Borges / Vannevar Bush)",
            "focus": "Self-Referential Return to Origin",
            "question": f"How does arriving at '{deepest_title}' (Hop {len(trail)-1}) and following its return bridge back to '{topic}' (Hop 0) invert or transform our initial understanding of '{topic}'?"
        },
        {
            "lens": "5. Epistemic vs. Diversive Depth (Ian Leslie / Mihaly Csikszentmihalyi)",
            "focus": "First-Principles Mechanism",
            "question": f"Beneath the surface metaphors used to describe '{topic}', '{mid_title}', and '{deepest_title}', what is the exact causal, mathematical, or cognitive mechanism that governs them—and where does it break down?"
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
            f"Boundary 2 (The Strange-Loop Vantage Point): Now that we have walked from '{topic}' down to '{deepest_topic}' and back, what assumption about '{topic}' looks completely artificial?",
            f"Boundary 3 (Scale & Time Horizon): What happens to '{topic}' if we shrink the scale by 1,000x (micro-level) or expand the time horizon by 100 years?"
        ],
        "de_bono_lateral_provocations": [
            f"PO-1 [Reversal]: Instead of 'How do we optimize/understand {topic}?', ask: 'What if {topic} deliberately worked in reverse, or what if its perceived flaw is actually its primary feature?'",
            f"PO-2 [Loop Short-Circuit]: Fuse Hop 0 ('{topic}') and Hop {deepest_topic} directly into a single compound concept: what new method or invention does that create?",
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
            "bridge_prompt": f"Bisociate '{topic} ↺ {deepest_topic}' with '{custom_matrix}': Where do their underlying mechanisms intersect at right angles?"
        })

    h = int(hashlib.sha256(topic.encode("utf-8")).hexdigest(), 16)
    n = len(ORTHOGONAL_MATRICES)
    for i in range(count):
        idx = (h + i * 5) % n
        mat = ORTHOGONAL_MATRICES[idx]
        target_label = f"{topic} ↺ {deepest_topic}" if deepest_topic != topic else topic
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
    seed_profile: Dict[str, Any],
    closing_loop: Dict[str, Any],
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
    seed_title = trail[0]["title"] if trail else topic
    deepest_title = trail[-1]["title"] if trail else topic

    lines.append(f"# Coherent Rabbit-Hole Strange-Loop Dossier: {seed_title} ──► {deepest_title} ──► ↺ {seed_title}")
    lines.append(
        f"*Excavated via `rabbit_hole_engine.py v3.0` | "
        f"**{len(trail)} Connected Main-Shaft Chambers** + **{len(side_warrens)} Side-Warrens** | "
        f"**{total_chars_read:,} chars** of prose mined in **{elapsed_sec:.1f}s***\n"
    )

    # 0. Overarching Circular Map of the Thread
    if trail:
        chain_str = " ──► ".join(f"**[Hop {n['hop']}: {n['title']}]**" for n in trail)
        chain_str += f" ──► 🔄 **[Return to Hop 0: {seed_title}]**"
        lines.append("## 0. Overarching Strange-Loop Map (Descent & Return to Beginning)")
        lines.append(f"> {chain_str}\n")

        # Summary Table of Hop-to-Hop + Overarching Connections
        lines.append("| Hop Step | Chamber Transition | Local Connection (`k-1 → k`) | Overarching Ariadne Tether (`Hop 0 ↔ k`) | Links Back to Hop 0? |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for n in trail[1:]:
            b = n.get("incoming_bridge") or {}
            prev_t = trail[n["hop"] - 1]["title"]
            loc_terms = ", ".join(f"`{t}`" for t in b.get("shared_local_terms", [])[:4]) or "prose bridge"
            seed_terms = ", ".join(f"`{t}`" for t in b.get("shared_seed_terms", [])[:4]) or f"`{seed_profile.get('stem', '')}*`"
            back_flag = "✅ Yes (Direct Backlink)" if b.get("links_back_to_origin") else "🧭 Tethered"
            lines.append(f"| **`Hop {n['hop']-1} → {n['hop']}`** | **{prev_t}** $\\rightarrow$ **{n['title']}** | {loc_terms} | {seed_terms} | {back_flag} |")
        if len(trail) > 1:
            loop_terms = ", ".join(f"`{t}`" for t in closing_loop.get("shared_concepts", [])[:5]) or f"`{seed_title.lower()}`"
            lines.append(f"| **`Hop {len(trail)-1} ↺ Hop 0`** | **{deepest_title}** $\\rightarrow$ **{seed_title}** | *Closing the Strange Loop* | {loop_terms} | 🔄 **Full Circle to Origin** |")
        lines.append("")

    # 1. Chamber-by-Chamber Coherent Descent
    lines.append("## 1. Down the Coherent Thread: Chamber-by-Chamber Excavation")
    if trail:
        for node in trail:
            hop = node["hop"]
            bridge = node.get("incoming_bridge")
            lines.append(f"### Chamber {hop} (`Hop {hop}`): [{node['title']}]({node['url']})")
            lines.append(
                f"- **Prose Depth Mined**: `{node['char_length']:,} chars` across `{node['section_count']} prose sections` "
                f"({', '.join(f'*{s}*' for s in node['section_names'][:6])})"
            )
            if bridge:
                prev_title = trail[hop - 1]["title"]
                loc_str = ", ".join(f"`{t}`" for t in bridge.get("shared_local_terms", [])[:5])
                seed_str = ", ".join(f"`{t}`" for t in bridge.get("shared_seed_terms", [])[:5])
                lines.append(
                    f"- **🔗 Connected Hop-to-Hop Thread (`Hop {hop - 1}: {prev_title}` $\\rightarrow$ `Hop {hop}: {node['title']}`)** "
                    f"*(from § {bridge.get('section_name', 'Prose')}, Sentence #{bridge['sentence_index']} of {bridge['total_sentences']})*:"
                )
                lines.append(f"  > *\"{bridge['bridge_sentence']}\"*")
                lines.append(
                    f"- **🧭 Overarching Ariadne's Tether to `Hop 0 ({seed_title})`**: "
                    f"Shared seed concepts: {seed_str or 'domain backlink'} | "
                    f"Shared local concepts with Hop {hop-1}: {loc_str or 'direct narrative link'} "
                    f"{'| **[Direct Backlink to Hop 0]**' if bridge.get('links_back_to_origin') else ''}"
                )
            lines.append(f"- **Surface Overview**:")
            lines.append(f"  > {node['lead_extract']}")
            if node.get("deep_section_excerpt"):
                lines.append(f"- **Deep Excavation (`§ {node['deep_section_title']}`)**:")
                lines.append(f"  > {node['deep_section_excerpt']}")
            if node["categories"]:
                lines.append(f"- **Ontological Strata**: `{', '.join(node['categories'])}`")
            if node["threads"]:
                lines.append(f"- **Next Connected Doors in This Chamber**: {', '.join(f'`{t}`' for t in node['threads'][:8])}\n")

    # 2. Following the Thread All the Way Back to the Beginning (The Strange Loop)
    if len(trail) > 1 and closing_loop:
        lines.append(f"## 2. 🔄 Following the Thread All the Way Back to the Beginning (`Hop {len(trail)-1}: {deepest_title}` $\\rightarrow$ `Hop 0: {seed_title}`)")
        lines.append(
            f"- **Return-Arc Mechanism**: `{closing_loop.get('type')}` "
            f"(in `{deepest_title}`, `§ {closing_loop.get('section')}`, Sentence #{closing_loop.get('sentence_index')} of {closing_loop.get('total_sentences')})"
        )
        lines.append(f"- **🧵 Verbatim Closing Bridge Sentence (`{deepest_title}` $\\rightarrow$ `{seed_title}`)**:")
        lines.append(f"  > *\"{closing_loop.get('sentence')}\"*")
        if closing_loop.get("shared_concepts"):
            lines.append(f"- **Shared Overarching Vocabulary Completing the Loop**: {', '.join(f'`{c}`' for c in closing_loop['shared_concepts'])}")
        lines.append(
            f"- **The Full-Circle Synthesis**: Starting at **{seed_title}** (`Hop 0`), each hop followed an unbroken prose thread through "
            + " $\\rightarrow$ ".join(f"*{n['title']}* (`Hop {n['hop']}`)" for n in trail[1:])
            + f", which directly reconnects back to **{seed_title}** (`Hop 0`)—revealing how the deep structure at the bottom of the shaft illuminates the surface where we began.\n"
        )

    # 3. Side-Warrens (Branching Tunnels)
    if side_warrens:
        lines.append("## 3. Coherent Branching Side-Warrens (Tethered Offshoots)")
        for idx, w in enumerate(side_warrens, 1):
            c1 = w["first_chamber"]
            c2 = w.get("second_chamber")
            b1 = w["bridge_from_parent"]
            lines.append(f"### Side-Warren {idx} (Splitting off `Hop {w['parent_hop']}: {w['parent_title']}`)")
            lines.append(f"- **🧵 Branching Prose Thread (`§ {b1.get('section_name', 'Prose')}`)**: *\"{b1['bridge_sentence']}\"*")
            lines.append(f"- **Sub-Chamber A — [{c1['title']}]({c1['url']})** (`{c1['char_length']:,} chars`):")
            lines.append(f"  > {c1['lead_extract']}")
            if c2:
                b2 = c2.get("incoming_bridge", {})
                lines.append(f"- **Sub-Chamber B (2nd-Order Branch) — [{c2['title']}]({c2['url']})** (`{c2['char_length']:,} chars`):")
                if b2.get("bridge_sentence"):
                    lines.append(f"  - *🧵 Thread Pulled*: *\"{b2['bridge_sentence']}\"*")
                lines.append(f"  > {c2['lead_extract']}\n")
            else:
                lines.append("")

    # 4. Primary Source Archival Books Across Multiple Hops
    lines.append("## 4. Multi-Depth Archival Book Burrow (Internet Archive & Open Library)")
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

    # 5. Five-Lens Abductive & Venatic Prompts
    lines.append("## 5. The Five Investigative Lenses Across the Loop (Carroll / Peirce / Ginzburg / Kuhn / Leslie)")
    for l in lenses:
        lines.append(f"### {l['lens']}")
        lines.append(f"- **Cognitive Focus**: *{l['focus']}*")
        lines.append(f"- **Investigative Probe**: {l['question']}\n")

    # 6. Outside the Nine-Dot Box & De Bono Lateral Hole-Digging
    lines.append("## 6. Thinking Outside the Box & Lateral Hole-Switching (Sam Loyd / Edward de Bono)")
    lines.append(f"> *{box_audit['nine_dot_origin']}*\n")
    lines.append("### Self-Imposed Boundary Diagnostics")
    for q in box_audit["boundary_audit_questions"]:
        lines.append(f"- {q}")
    lines.append("\n### Edward de Bono Lateral Provocations (`PO`)")
    for po in box_audit["de_bono_lateral_provocations"]:
        lines.append(f"- {po}")
    lines.append("")

    # 7. Arthur Koestler Bisociation Collisions
    lines.append("## 7. Arthur Koestler Bisociation Collider ('Thinking Aside' Across Matrices)")
    for idx, bi in enumerate(bisociations, 1):
        lines.append(f"### Collision {idx}: `{seed_title} ↺ {deepest_title}` × `{bi['domain']}`")
        lines.append(f"- **Orthogonal Matrix Principle**: {bi['principle']}")
        lines.append(f"- **Bisociative Synthesis Prompt**: **{bi['bridge_prompt']}**\n")

    # 8. Hofstadter Strange-Loop Stack & Epistemic Compass
    lines.append("## 8. Hofstadter Strange-Loop Stack (`PUSH` / `POP` / `RETURN TO ORIGIN`)")
    lines.append("```text")
    lines.append(f"┌──► [HOP 0: ORIGIN & RETURN]  {seed_title}")
    if len(trail) > 1:
        for n in trail[1:]:
            indent = "│ " + ("  " * min(n["hop"], 6))
            back_tag = " [★ Direct Backlink to Hop 0]" if (n.get("incoming_bridge") or {}).get("links_back_to_origin") else ""
            lines.append(f"{indent}└── PUSH [HOP {n['hop']}]  {n['title']}{back_tag}")
    lines.append(f"└────── 🔄 RETURN BRIDGE FROM HOP {len(trail)-1} ('{deepest_title}') BACK TO HOP 0 ('{seed_title}')")
    lines.append("```")

    return "\n".join(lines)


# =============================================================================
# CLI Entrypoint
# =============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rabbit-Hole Curiosity Engine v3.0: Coherent Hop-to-Hop Thread Excavator & Strange-Loop Return Engine"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # explore
    p_exp = subparsers.add_parser("explore", help="Run coherent long-thread rabbit-hole expedition with return loop to origin")
    p_exp.add_argument("topic", help="Topic, question, or concept to investigate")
    p_exp.add_argument("--hops", type=int, default=10, help="Number of connected chambers down the main thread (default: 10)")
    p_exp.add_argument("--branches", type=int, default=3, help="Number of coherent branching side-warrens (default: 3)")
    p_exp.add_argument("--rows", type=int, default=3, help="Number of archival books to retrieve per depth stop (default: 3)")
    p_exp.add_argument("--matrix", help="Optional custom orthogonal domain for Koestler bisociation")
    p_exp.add_argument("-o", "--output", help="Save full Markdown expedition dossier to file")

    # threads
    p_thr = subparsers.add_parser("threads", help="Trace a coherent multi-hop associative trail that loops back to Hop 0")
    p_thr.add_argument("topic", help="Seed topic")
    p_thr.add_argument("--hops", type=int, default=10, help="Number of sequential hops (default: 10)")
    p_thr.add_argument("--branches", type=int, default=2, help="Number of branching side-warrens (default: 2)")

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
        trail, side_warrens, seed_profile, closing_loop = trace_coherent_rabbit_hole(
            args.topic, hops=args.hops, branch_count=args.branches
        )
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
            seed_profile=seed_profile,
            closing_loop=closing_loop,
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
            log_progress(f"Coherent Strange-Loop Expedition complete in {elapsed:.1f}s! Saved to {out_path} ({len(report.splitlines())} lines).")
        else:
            print(report)
        return 0

    elif args.command == "threads":
        trail, side_warrens, seed_profile, closing_loop = trace_coherent_rabbit_hole(
            args.topic, hops=args.hops, branch_count=args.branches
        )
        for node in trail:
            b = node.get("incoming_bridge")
            print(f"=== [Hop {node['hop']}] {node['title']} ({node['char_length']:,} chars) ===")
            if b:
                print(f"  Connected Thread (from § {b['section_name']}): \"{b['bridge_sentence']}\"")
                print(f"  Ariadne Tether to Hop 0: {b['shared_seed_terms']} | Local Continuity: {b['shared_local_terms']}")
            print(f"  Overview: {node['lead_extract'][:300]}...\n")
        if closing_loop:
            print(f"=== 🔄 RETURN LOOP TO HOP 0 ({trail[0]['title']}) ===")
            print(f"  Closing Bridge Sentence: \"{closing_loop.get('sentence')}\"")
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
