#!/usr/bin/env python3
"""
Chinatown Board Game Property and Business Tile Tracker
"""

import csv
import sys
import os
import random
from players import PLAYERS

def init_properties():
    """Initialize the properties CSV file with 90 properties"""
    filename = "chinatown_properties.csv"
    
    if os.path.exists(filename):
        response = input(f"{filename} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Initialization cancelled.")
            return
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Property', 'Status', 'Player'])
        
        # Write 90 properties with initial values
        for i in range(1, 91):
            writer.writerow([i, 'deck', ''])
    
    print(f"Initialized {filename} with 90 properties")

def init_businesses():
    """Initialize the business tiles CSV file"""
    filename = "chinatown_businesses.csv"
    
    if os.path.exists(filename):
        response = input(f"{filename} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Initialization cancelled.")
            return
    
    # Business types and their quantities based on the image
    businesses = [
        ("photo", 3, 6),      # 6 Photo tiles of size 3
        ("teahouse", 4, 6),   # 6 Tea House tiles of size 4
        ("seafood", 5, 6),    # 6 Sea Food tiles of size 5
        ("jewelery", 3, 5),   # 5 Jewelry tiles of size 3
        ("tropical", 4, 5),   # 5 Tropical tiles of size 4
        ("florist", 5, 5),    # 5 Florist tiles of size 5
        ("takeout", 3, 4),    # 4 Take Out tiles of size 3
        ("laundry", 4, 4),    # 4 Laundry tiles of size 4
        ("dimsum", 5, 4),     # 4 Dim Sum tiles of size 5
        ("antiques", 3, 3),   # 3 Antiques tiles of size 3
        ("restaurant", 6, 3), # 3 Restaurant tiles of size 6
    ]
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Business', 'Status', 'Player'])
        
        # Write business tiles
        for business_name, size, count in businesses:
            for i in range(count):
                tile_name = f"{business_name}{size}"
                writer.writerow([tile_name, 'deck', ''])
    
    print(f"Initialized {filename} with business tiles")

def deal_plots(num_cards):
    """Deal plots to players randomly"""
    filename = "chinatown_properties.csv"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run 'init' first.")
        return
    
    # Read current properties
    properties = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            properties.append(row)
    
    # Check if any plots are under review
    reviewing_properties = [prop for prop in properties if prop[1] == 'reviewing']
    if reviewing_properties:
        print("Error: Cannot deal plots while some are under review. Use 'return-plots' first.")
        return
    
    # Find properties that are still in deck
    deck_properties = [prop for prop in properties if prop[1] == 'deck']
    
    # Check if we have enough cards
    total_needed = num_cards * len(PLAYERS)
    if len(deck_properties) < total_needed:
        print(f"Error: Not enough cards in deck. Need {total_needed}, have {len(deck_properties)}")
        return
    
    # Randomly shuffle deck properties
    random.shuffle(deck_properties)
    
    # Deal cards to players
    card_index = 0
    for player in PLAYERS:
        for _ in range(num_cards):
            prop = deck_properties[card_index]
            prop[1] = 'reviewing'  # Update status
            prop[2] = player       # Assign player
            card_index += 1
    
    # Write updated properties back to file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(properties)
    
    print(f"Dealt {num_cards} plots to each of {len(PLAYERS)} players")

def return_plots(player, plot_ids_str):
    """Return specified plots to deck and mark remaining as owned"""
    filename = "chinatown_properties.csv"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run 'init' first.")
        return
    
    # Validate player
    if player not in PLAYERS:
        print(f"Error: Invalid player '{player}'. Valid players: {', '.join(PLAYERS)}")
        return
    
    # Parse plot IDs
    try:
        plot_ids = [int(plot_id.strip()) for plot_id in plot_ids_str.split(',')]
    except ValueError:
        print("Error: Plot IDs must be comma-separated integers")
        return
    
    # Read current properties
    properties = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            properties.append(row)
    
    # Find player's reviewing plots
    player_reviewing = [prop for prop in properties if prop[1] == 'reviewing' and prop[2] == player]
    
    if not player_reviewing:
        print(f"Error: No plots under review for player '{player}'")
        return
    
    # Validate that all specified plot IDs belong to the player and are under review
    player_plot_ids = [int(prop[0]) for prop in player_reviewing]
    invalid_ids = [pid for pid in plot_ids if pid not in player_plot_ids]
    if invalid_ids:
        print(f"Error: Plot IDs {invalid_ids} are not under review by player '{player}'")
        return
    
    # Update plot statuses
    returned_count = 0
    owned_count = 0
    
    for prop in properties:
        if prop[1] == 'reviewing' and prop[2] == player:
            plot_id = int(prop[0])
            if plot_id in plot_ids:
                # Return to deck
                prop[1] = 'deck'
                prop[2] = ''
                returned_count += 1
            else:
                # Mark as owned
                prop[1] = 'owned'
                owned_count += 1
    
    # Write updated properties back to file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(properties)
    
    print(f"Player '{player}': returned {returned_count} plots to deck, kept {owned_count} plots")

def main():
    if len(sys.argv) < 2:
        print("Usage: python ct.py <command>")
        print("Commands:")
        print("  init                         - Initialize properties and business tiles CSV files")
        print("  deal plots <num>             - Deal <num> plots to each player")
        print("  return-plots <player> <ids>  - Return specified plots to deck, keep rest")
        return
    
    command = sys.argv[1].lower()
    
    if command == "init":
        init_properties()
        init_businesses()
    elif command == "deal":
        if len(sys.argv) < 4 or sys.argv[2].lower() != "plots":
            print("Usage: python ct.py deal plots <number>")
            return
        
        try:
            num_cards = int(sys.argv[3])
            if num_cards <= 0:
                print("Error: Number of cards must be positive")
                return
            deal_plots(num_cards)
        except ValueError:
            print("Error: Number of cards must be a valid integer")
    elif command == "return-plots":
        if len(sys.argv) < 4:
            print("Usage: python ct.py return-plots <player> <plot_ids>")
            print("Example: python ct.py return-plots blue 33,35")
            return
        
        player = sys.argv[2].lower()
        plot_ids_str = sys.argv[3]
        return_plots(player, plot_ids_str)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: init, deal, return-plots")

if __name__ == "__main__":
    main()