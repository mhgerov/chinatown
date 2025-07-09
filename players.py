"""
Chinatown Board Game Player Configuration

This module contains the read-only list of player names/colors
used throughout the Chinatown board game tracker.
"""

# Read-only list of player names (colors) used in the game
PLAYERS = [
    "red",
    "blue", 
    "green",
    "yellow",
    "purple"
]

# For display purposes, get capitalized version of player names
def get_display_name(player):
    """Return capitalized version of player name for display"""
    return player.capitalize()

# Validate if a player name is valid
def is_valid_player(player):
    """Check if a player name is in the valid player list"""
    return player.lower() in PLAYERS