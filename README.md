# Rabbit-Hole Curiosity Skill

An agent skill and zero-dependency Python 3 engine that turns any AI coding or research agent into an epistemically curious investigator—tracing multi-hop hypertext threads, uncovering primary-source books, running Sam Loyd Nine-Dot boundary audits, and colliding ideas across orthogonal domains (Arthur Koestler Bisociation & Edward de Bono Lateral Thinking).

No API keys, logins, or `pip` packages required.

## 1-Step Install

```bash
sh install.sh
```

This installs the skill to `~/.agents/skills/rabbit-hole-curiosity/`.

## Usage

### In Your Agent Chat
Type `/rabbit-hole-curiosity` or ask your agent to *"go down a rabbit hole"*, *"get curious about"*, or *"think outside the box"* on any topic.

### From the Terminal
```bash
# Full 6-stratum rabbit-hole exploration
python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py explore "Intermodal shipping containers"

# Trace a 3-hop associative hypertext trail
python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py threads "Serendipity" --hops 3

# Collide a topic with orthogonal domains (Koestler Bisociation)
python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py bisociate "Urban traffic"

# Diagnose unspoken assumptions & generate De Bono lateral provocations
python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py outside-the-box "Battery storage"
```
