# CT CLI Tool Documentation

The `ct.py` script is a command-line interface for managing Chinatown board game properties and business tiles. It tracks card distribution, player ownership, and deck management through CSV files.

## Overview

The tool manages two main game components:
- **Properties**: 85 numbered property plots (1-85)
- **Business Tiles**: Various business types with different quantities based on size

## Players

The game supports 5 players with color-coded identities:
- red
- blue
- green
- yellow
- purple

## Commands

### Initialize Game Data

```bash
python3 ct.py init
```

Creates two CSV files:
- `chinatown_properties.csv` - 85 properties numbered 1-85
- `chinatown_businesses.csv` - Business tiles based on `businesses-ref.csv`

The tool will prompt before overwriting existing files.

### Deal Properties

```bash
python3 ct.py deal plots <number>
```

Deals the specified number of property plots to each player. Properties are:
- Randomly shuffled before dealing
- Marked as "reviewing" status
- Assigned to players for decision-making

**Example:**
```bash
python3 ct.py deal plots 3
```
Deals 3 property plots to each of the 5 players (15 total).

### Deal Business Tiles

```bash
python3 ct.py deal biz <number>
```

Deals the specified number of business tiles to each player. Business tiles are:
- Randomly shuffled before dealing
- Marked as "reviewing" status
- Assigned to players for decision-making

**Example:**
```bash
python3 ct.py deal biz 2
```
Deals 2 business tiles to each of the 5 players (10 total).

### Return Properties

```bash
python3 ct.py return-plots <player> <plot_ids>
```

Allows a player to return specific property plots to the deck and keep the rest. Plot IDs should be comma-separated.

**Parameters:**
- `<player>`: Player color (red, blue, green, yellow, purple)
- `<plot_ids>`: Comma-separated list of property numbers to return

**Example:**
```bash
python3 ct.py return-plots blue 33,35
```
Player "blue" returns properties 33 and 35 to the deck, keeps all other reviewing properties.

### Return Business Tiles

```bash
python3 ct.py return-biz <player> <business_names>
```

Allows a player to return specific business tiles to the deck and keep the rest. Business names should be comma-separated.

**Parameters:**
- `<player>`: Player color (red, blue, green, yellow, purple)
- `<business_names>`: Comma-separated list of business tile names to return

**Example:**
```bash
python3 ct.py return-biz blue photo3,teahouse4
```
Player "blue" returns "photo3" and "teahouse4" business tiles to the deck, keeps all other reviewing tiles.

## Business Types

The following business types are available (name + size):

| Business | Size | Quantity | Tile Names |
|----------|------|----------|------------|
| photo | 3 | 6 | photo3 (×6) |
| teaHouse | 3 | 6 | teaHouse3 (×6) |
| seaFood | 3 | 6 | seaFood3 (×6) |
| jewellery | 4 | 7 | jewellery4 (×7) |
| tropicalFish | 4 | 7 | tropicalFish4 (×7) |
| florist | 4 | 7 | florist4 (×7) |
| takeOut | 5 | 8 | takeOut5 (×8) |
| laundry | 5 | 8 | laundry5 (×8) |
| dimSum | 5 | 8 | dimSum5 (×8) |
| antiques | 6 | 9 | antiques6 (×9) |
| factory | 6 | 9 | factory6 (×9) |
| restaurant | 6 | 9 | restaurant6 (×9) |

*Note: Business tile quantity = size + 3*

## Card States

Cards (both properties and business tiles) can be in one of three states:

- **deck**: Available for dealing
- **reviewing**: Dealt to a player, awaiting decision
- **owned**: Player has decided to keep the card

## Error Handling

The tool includes comprehensive error checking:

- Validates player names against the 5-player list
- Prevents dealing when cards are under review
- Ensures sufficient cards are available before dealing
- Validates that returned cards belong to the specified player
- Requires CSV files to exist before most operations

## Workflow

1. **Initialize**: Run `init` to create CSV files
2. **Deal**: Use `deal plots` or `deal biz` to distribute cards
3. **Review**: Players examine their dealt cards
4. **Return**: Use `return-plots` or `return-biz` to finalize decisions
5. **Repeat**: Continue dealing and returning as needed throughout the game

## Files Created

- `chinatown_properties.csv`: Property tracking (Property, Status, Player)
- `chinatown_businesses.csv`: Business tile tracking (Business, Status, Player)
- `businesses-ref.csv`: Business reference data (required for initialization)