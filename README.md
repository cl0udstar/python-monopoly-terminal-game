# Monopoly – Terminal Simulation (Python)

A terminal-based **Monopoly** simulation built in Python to demonstrate **complex state management, turn-based game logic, and object-oriented design**.  
Focus areas include: player turns, dice, property ownership, rents, Chance/Community Chest, jail logic, and bankruptcy handling.
---
## Features
- Turn engine with dice rolls, doubles, and jail rules
- Property system: purchase, rent, mortgages (data-driven via `property_data.py`)
- Cash flow and bankruptcy resolution
- Chance & Community Chest card mechanics (via `combinations.py` if applicable)
- Clean terminal output (color helpers in `colours.py`)
- Deterministic modes (seeded RNG) for testing & reproducibility
---
## Project Structure
```bash
monopoly/
├── monopoly_game.py     # Entry point / main loop
├── combinations.py      # Cards / rules helpers (Chance/Community Chest)
├── property_data.py     # Board & property metadata (rent tables, groups)
├── colours.py           # Terminal color helpers
```
---
## Requirements
- Python 3.8+
- No external dependencies required.


---
## Run
```bash
python monopoly_game.py
```
---

# How It Works (High Level)
- State: Players, positions, balances, owned properties and deck states are tracked each turn.
- Rules: Movement from dice; passing GO; rent calculation by color set & houses/hotels (partially implemented); jail; chance/community cards (not yet implemented).
- Design: Separated data (property_data.py) from logic (monopoly_game.py) to keep rules maintainable.

## Roadmap
- Save/Load game state (JSON)
- Stats & replay logs for simulations
- Bot strategies / Monte-Carlo runs
- Houses/Hotels building flow & auctions

---
# Disclaimer

This project is a learning exercise in simulations and OOP, not affiliated with Hasbro.
All Monopoly trademarks belong to their respective owners.
