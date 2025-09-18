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
    """Initialize the properties CSV file with 85 properties"""
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
        
        # Write 85 properties with initial values
        for i in range(1, 86):
            writer.writerow([i, 'deck', ''])
    
    print(f"Initialized {filename} with 85 properties")

def init_businesses():
    """Initialize the business tiles CSV file"""
    filename = "chinatown_businesses.csv"
    ref_filename = "businesses-ref.csv"
    
    if os.path.exists(filename):
        response = input(f"{filename} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Initialization cancelled.")
            return
    
    if not os.path.exists(ref_filename):
        print(f"Error: {ref_filename} not found. This file is required for business initialization.")
        return
    
    # Read business data from reference file
    businesses = []
    with open(ref_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            size = int(row['Size'])
            count = size + 3  # Quantity is always size + 3
            businesses.append((name, size, count))
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Business', 'Status', 'Player'])
        
        # Write business tiles
        total_tiles = 0
        for business_name, size, count in businesses:
            for i in range(count):
                tile_name = f"{business_name}{size}"
                writer.writerow([tile_name, 'deck', ''])
                total_tiles += 1
    
    print(f"Initialized {filename} with {total_tiles} business tiles")

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
            # Ensure row has 3 columns (Property, Status, Player)
            if len(row) < 3:
                row.extend([''] * (3 - len(row)))
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

def deal_businesses(num_cards):
    """Deal business tiles to players randomly"""
    filename = "chinatown_businesses.csv"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run 'init' first.")
        return
    
    # Read current businesses
    businesses = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            businesses.append(row)
    
    
    # Find businesses that are still in deck
    deck_businesses = [biz for biz in businesses if biz[1] == 'deck']
    
    # Check if we have enough cards
    total_needed = num_cards * len(PLAYERS)
    if len(deck_businesses) < total_needed:
        print(f"Error: Not enough cards in deck. Need {total_needed}, have {len(deck_businesses)}")
        return
    
    # Randomly shuffle deck businesses
    random.shuffle(deck_businesses)
    
    # Deal cards to players
    card_index = 0
    for player in PLAYERS:
        for _ in range(num_cards):
            biz = deck_businesses[card_index]
            biz[1] = 'owned'  # Update status
            biz[2] = player       # Assign player
            card_index += 1
    
    # Write updated businesses back to file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(businesses)
    
    print(f"Dealt {num_cards} business tiles to each of {len(PLAYERS)} players")

def get_plots(player):
    """Get comma-separated list of properties owned by a player"""
    filename = "chinatown_properties.csv"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run 'init' first.")
        return
    
    # Validate player
    if player not in PLAYERS:
        print(f"Error: Invalid player '{player}'. Valid players: {', '.join(PLAYERS)}")
        return
    
    # Read current properties
    properties = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            properties.append(row)
    
    # Find properties owned by the player
    owned_properties = [prop[0] for prop in properties if prop[1] == 'owned' and prop[2] == player]
    
    if owned_properties:
        print(','.join(owned_properties))
    else:
        print("")

def main():
    if len(sys.argv) < 2:
        print("Usage: python ct.py <command>")
        print("Commands:")
        print("  init                         - Initialize properties and business tiles CSV files")
        print("  deal plots <num>             - Deal <num> plots to each player")
        print("  deal biz <num>               - Deal <num> business tiles to each player")
        print("  return-plots <player> <ids>  - Return specified plots to deck, keep rest")
        print("  get-plots <player>           - Get comma-separated list of owned properties")
        return
    
    command = sys.argv[1].lower()
    
    if command == "init":
        init_properties()
        init_businesses()
    elif command == "deal":
        if len(sys.argv) < 4:
            print("Usage: python ct.py deal plots <number>")
            print("       python ct.py deal biz <number>")
            return
        
        subcommand = sys.argv[2].lower()
        
        try:
            num_cards = int(sys.argv[3])
            if num_cards <= 0:
                print("Error: Number of cards must be positive")
                return
            
            if subcommand == "plots":
                deal_plots(num_cards)
            elif subcommand == "biz":
                deal_businesses(num_cards)
            else:
                print("Error: Invalid deal subcommand. Use 'plots' or 'biz'")
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
    elif command == "get-plots":
        if len(sys.argv) < 3:
            print("Usage: python ct.py get-plots <player>")
            print("Example: python ct.py get-plots red")
            return
        
        player = sys.argv[2].lower()
        get_plots(player)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: init, deal, return-plots, get-plots")

if __name__ == "__main__":
    main()