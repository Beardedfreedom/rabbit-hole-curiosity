# Sample Rabbit-Hole Investigation Walkthrough

This example demonstrates how an agent uses the **Rabbit-Hole Curiosity** skill to turn a seemingly ordinary prompt (*"Tell me about shipping containers"*) into a deep, multi-threaded, outside-the-box investigation.

---

## Step 1: Run the Rabbit-Hole Curiosity Engine

```bash
python3 ~/.agents/skills/rabbit-hole-curiosity/scripts/rabbit_hole_engine.py explore "Intermodal shipping container"
```

---

## Step 2: Apply the 5-Stratum Synthesis in the Response

### 1. The Entry Shaft (The White Rabbit Anomaly)
- **Surface view**: A shipping container is just a corrugated steel box ($8 \times 8.5 \times 40$ feet).
- **The Anomaly**: Before 1956, loading a cargo ship cost **\$5.86 per ton** and tied up ships in port for a week; after Malcom McLean's *Ideal X* sailed from Newark to Houston on April 26, 1956, loading cost dropped to **\$0.16 per ton**—a **97.3% collapse in friction** that reshaped global economic geography more than almost any trade treaty of the 20th century (Marc Levinson, *The Box*). Even stranger: the entire global system hinged not on the steel box itself, but on a tiny, patent-free mechanical corner casting—**Keith Tantlinger's twistlock**—which allowed cranes and ships to lock boxes together without human hands in the hold.

### 2. In the Threads (Multi-Hop Associative Trail)
- **`Hop 0`: Intermodal Shipping Container** $\rightarrow$ **`Hop 1`: Twistlock & ISO 668 Standardization** $\rightarrow$ **`Hop 2`: Packet Switching (ARPANET / TCP-IP)**.
- **The Subterranean Connection**: Notice the exact structural isomorphism between **Malcom McLean's physical container (1956)** and **Paul Baran / Donald Davies's digital "packet" (1964)**: both solved congestion by wrapping heterogeneous payloads inside a standardized header/envelope so the routing infrastructure never needs to inspect the contents inside!

### 3. Thinking Outside the Nine-Dot Box (Sam Loyd / Edward de Bono)
- **The Invisible Box**: In the 1950s, steamship companies kept trying to build faster ships and better winches (*digging the old hole deeper*).
- **Stepping Outside the Box**: McLean wasn't a shipping executive—he was a *trucking* entrepreneur who asked a lateral question: *"Why unload the truck trailer at the dock at all? Why not put the box itself onto the ship?"*

### 4. Koestler Bisociation Collision
- **`Intermodal Containers` $\times$ `Epigenetic Chromatin Packaging`**: Just as eukaryotic cells fold 2 meters of diverse DNA around standardized histone octamers so cellular machinery can transport and regulate any gene uniformly, global logistics wraps arbitrary physical matter around standardized ISO twistlock geometry.

### 5. The Open Warren (Next Rabbit-Hole Threads to Pull)
1. **The Military Logistics Thread**: How did the 1967 Cam Ranh Bay bottleneck in Vietnam force the U.S. military to adopt McLean's Sea-Land containers, inadvertently subsidizing the empty return trips from Japan that kickstarted East Asian export manufacturing?
2. **The Architecture of Ghost Ports**: Why did containerization destroy historic urban waterfronts (Manhattan, San Francisco, London Docklands) overnight while turning obscure mudflats (Newark, Felixstowe, Shenzhen) into mega-hubs?
3. **The Acoustic Whale Thread**: How has the low-frequency propeller cavitation noise of ultra-large container vessels altered the oceanic acoustic communication range of baleen whales since 1960?
