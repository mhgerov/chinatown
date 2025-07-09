# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a board game tracker for "Chinatown" - a static HTML/CSS/JavaScript application that displays the game board state, player statistics, and business information. The application runs entirely in the browser with no build process or dependencies.

## Architecture

- **Single-page application**: All code is contained in `index.html`
- **Vanilla JavaScript**: No frameworks or libraries used
- **Grid-based board layout**: Uses CSS Grid to render the game board with 6 building blocks
- **Static game state**: Game data is hardcoded in JavaScript objects within the HTML file

### Key Components

- **Board rendering**: Dynamic grid layout based on `layout` array defining plot positions
- **Player management**: Tracks balances, owned plots, and business inventories for 5 players (red, blue, green, yellow, purple)
- **Business system**: 12 different business types with emoji representations and deck tracking
- **Round tracking**: Shows current round and available resources per round

### Data Structures

- `businesses`: Maps business types to emoji + size representations
- `ownedPlots`: Tracks which plots each player owns
- `businessAssignments`: Maps plot numbers to placed businesses
- `playerBalances`: Current money for each player
- `businessInventory`: Businesses owned by each player
- `businessDeck`: Available business tiles remaining

## Development

Since this is a static HTML file with no build process:
- Open `index.html` directly in a browser to view/test
- No package.json, dependencies, or build commands exist
- All changes are made directly to the HTML file
- Use browser developer tools for debugging JavaScript

## File Structure

- `index.html` - Complete application (HTML, CSS, JavaScript)
- `README.md` - Basic project title

## Environment Notes

- In this environment, python is run with `python3`.

## Script Memories

- `ct.py` script purpose: Currently unknown. Specific functionality needs to be determined and documented.