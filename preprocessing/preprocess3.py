import pandas as pd
import os
import numpy as np
from time import time
import re

#role mapping: {'Carry': 0, 'Escape': 1, 'Nuker': 2, 'Initiator': 3, 'Durable': 4, 'Disabler': 5, 'Support': 6, 'Pusher': 7}
# Fold the line below this one
hero_mapping = {
    "antimage": {
        "id": 1,
        "roles": [
            0,
            1,
            2
        ]
    },
    "axe": {
        "id": 2,
        "roles": [
            3,
            4,
            5,
            0
        ]
    },
    "bane": {
        "id": 3,
        "roles": [
            6,
            5,
            2,
            4
        ]
    },
    "bloodseeker": {
        "id": 4,
        "roles": [
            0,
            5,
            2,
            3
        ]
    },
    "crystalmaiden": {
        "id": 5,
        "roles": [
            6,
            5,
            2
        ]
    },
    "drowranger": {
        "id": 6,
        "roles": [
            0,
            5,
            7
        ]
    },
    "earthshaker": {
        "id": 7,
        "roles": [
            6,
            3,
            5,
            2
        ]
    },
    "juggernaut": {
        "id": 8,
        "roles": [
            0,
            7,
            1
        ]
    },
    "mirana": {
        "id": 9,
        "roles": [
            0,
            6,
            1,
            2,
            5
        ]
    },
    "morphling": {
        "id": 10,
        "roles": [
            0,
            1,
            4,
            2,
            5
        ]
    },
    "nevermore": {
        "id": 11,
        "roles": [
            0,
            2
        ]
    },
    "phantomlancer": {
        "id": 12,
        "roles": [
            0,
            1,
            7,
            2
        ]
    },
    "puck": {
        "id": 13,
        "roles": [
            3,
            5,
            1,
            2
        ]
    },
    "pudge": {
        "id": 14,
        "roles": [
            5,
            3,
            4,
            2
        ]
    },
    "razor": {
        "id": 15,
        "roles": [
            0,
            4,
            2,
            7
        ]
    },
    "sandking": {
        "id": 16,
        "roles": [
            3,
            5,
            6,
            2,
            1
        ]
    },
    "stormspirit": {
        "id": 17,
        "roles": [
            0,
            1,
            2,
            3,
            5
        ]
    },
    "sven": {
        "id": 18,
        "roles": [
            0,
            5,
            3,
            4,
            2
        ]
    },
    "tiny": {
        "id": 19,
        "roles": [
            0,
            2,
            7,
            3,
            4,
            5
        ]
    },
    "vengefulspirit": {
        "id": 20,
        "roles": [
            6,
            3,
            5,
            2,
            1
        ]
    },
    "windrunner": {
        "id": 21,
        "roles": [
            0,
            6,
            5,
            1,
            2
        ]
    },
    "zuus": {
        "id": 22,
        "roles": [
            2,
            0
        ]
    },
    "kunkka": {
        "id": 23,
        "roles": [
            0,
            6,
            5,
            3,
            4,
            2
        ]
    },
    "lina": {
        "id": 25,
        "roles": [
            6,
            0,
            2,
            5
        ]
    },
    "lion": {
        "id": 26,
        "roles": [
            6,
            5,
            2,
            3
        ]
    },
    "shadowshaman": {
        "id": 27,
        "roles": [
            6,
            7,
            5,
            2,
            3
        ]
    },
    "slardar": {
        "id": 28,
        "roles": [
            0,
            4,
            3,
            5,
            1
        ]
    },
    "tidehunter": {
        "id": 29,
        "roles": [
            3,
            4,
            5,
            2,
            0
        ]
    },
    "witchdoctor": {
        "id": 30,
        "roles": [
            6,
            2,
            5
        ]
    },
    "lich": {
        "id": 31,
        "roles": [
            6,
            2
        ]
    },
    "riki": {
        "id": 32,
        "roles": [
            0,
            1,
            5
        ]
    },
    "enigma": {
        "id": 33,
        "roles": [
            5,
            3,
            7
        ]
    },
    "tinker": {
        "id": 34,
        "roles": [
            0,
            2,
            7
        ]
    },
    "sniper": {
        "id": 35,
        "roles": [
            0,
            2
        ]
    },
    "necrolyte": {
        "id": 36,
        "roles": [
            0,
            2,
            4,
            5
        ]
    },
    "warlock": {
        "id": 37,
        "roles": [
            6,
            3,
            5
        ]
    },
    "beastmaster": {
        "id": 38,
        "roles": [
            3,
            5,
            4,
            2
        ]
    },
    "queenofpain": {
        "id": 39,
        "roles": [
            0,
            2,
            1
        ]
    },
    "venomancer": {
        "id": 40,
        "roles": [
            6,
            2,
            3,
            7,
            5
        ]
    },
    "facelessvoid": {
        "id": 41,
        "roles": [
            0,
            3,
            5,
            1,
            4
        ]
    },
    "skeletonking": {
        "id": 42,
        "roles": [
            0,
            6,
            4,
            5,
            3
        ]
    },
    "deathprophet": {
        "id": 43,
        "roles": [
            0,
            7,
            2,
            5
        ]
    },
    "phantomassassin": {
        "id": 44,
        "roles": [
            0,
            1
        ]
    },
    "pugna": {
        "id": 45,
        "roles": [
            2,
            7
        ]
    },
    "templarassassin": {
        "id": 46,
        "roles": [
            0,
            1
        ]
    },
    "viper": {
        "id": 47,
        "roles": [
            0,
            4,
            3,
            5
        ]
    },
    "luna": {
        "id": 48,
        "roles": [
            0,
            2,
            7
        ]
    },
    "dragonknight": {
        "id": 49,
        "roles": [
            0,
            7,
            4,
            5,
            3,
            2
        ]
    },
    "dazzle": {
        "id": 50,
        "roles": [
            6,
            2,
            5
        ]
    },
    "rattletrap": {
        "id": 51,
        "roles": [
            3,
            5,
            4,
            2
        ]
    },
    "leshrac": {
        "id": 52,
        "roles": [
            0,
            6,
            2,
            7,
            5
        ]
    },
    "furion": {
        "id": 53,
        "roles": [
            0,
            7,
            1,
            2
        ]
    },
    "lifestealer": {
        "id": 54,
        "roles": [
            0,
            4,
            1,
            5
        ]
    },
    "darkseer": {
        "id": 55,
        "roles": [
            3,
            1,
            5
        ]
    },
    "clinkz": {
        "id": 56,
        "roles": [
            0,
            1,
            7
        ]
    },
    "omniknight": {
        "id": 57,
        "roles": [
            6,
            4,
            2
        ]
    },
    "enchantress": {
        "id": 58,
        "roles": [
            6,
            7,
            4,
            5
        ]
    },
    "huskar": {
        "id": 59,
        "roles": [
            0,
            4,
            3
        ]
    },
    "nightstalker": {
        "id": 60,
        "roles": [
            0,
            3,
            4,
            5,
            2
        ]
    },
    "broodmother": {
        "id": 61,
        "roles": [
            0,
            7,
            1,
            2
        ]
    },
    "bountyhunter": {
        "id": 62,
        "roles": [
            1,
            2
        ]
    },
    "weaver": {
        "id": 63,
        "roles": [
            0,
            1
        ]
    },
    "jakiro": {
        "id": 64,
        "roles": [
            6,
            2,
            7,
            5
        ]
    },
    "batrider": {
        "id": 65,
        "roles": [
            3,
            5,
            1
        ]
    },
    "chen": {
        "id": 66,
        "roles": [
            6,
            7
        ]
    },
    "spectre": {
        "id": 67,
        "roles": [
            0,
            4,
            1
        ]
    },
    "ancientapparition": {
        "id": 68,
        "roles": [
            6,
            5,
            2
        ]
    },
    "doombringer": {
        "id": 69,
        "roles": [
            0,
            5,
            3,
            4,
            2
        ]
    },
    "ursa": {
        "id": 70,
        "roles": [
            0,
            4,
            5
        ]
    },
    "spiritbreaker": {
        "id": 71,
        "roles": [
            0,
            3,
            5,
            4,
            1
        ]
    },
    "gyrocopter": {
        "id": 72,
        "roles": [
            0,
            2,
            5
        ]
    },
    "alchemist": {
        "id": 73,
        "roles": [
            0,
            6,
            4,
            5,
            3,
            2
        ]
    },
    "invoker": {
        "id": 74,
        "roles": [
            0,
            2,
            5,
            1,
            7
        ]
    },
    "silencer": {
        "id": 75,
        "roles": [
            0,
            6,
            5,
            3,
            2
        ]
    },
    "obsidiandestroyer": {
        "id": 76,
        "roles": [
            0,
            2,
            5
        ]
    },
    "lycan": {
        "id": 77,
        "roles": [
            0,
            7,
            4,
            1
        ]
    },
    "brewmaster": {
        "id": 78,
        "roles": [
            0,
            3,
            4,
            5,
            2
        ]
    },
    "shadowdemon": {
        "id": 79,
        "roles": [
            6,
            5,
            3,
            2
        ]
    },
    "lonedruid": {
        "id": 80,
        "roles": [
            0,
            7,
            4
        ]
    },
    "chaosknight": {
        "id": 81,
        "roles": [
            0,
            5,
            4,
            7,
            3
        ]
    },
    "meepo": {
        "id": 82,
        "roles": [
            0,
            1,
            2,
            5,
            3,
            7
        ]
    },
    "treant": {
        "id": 83,
        "roles": [
            6,
            3,
            4,
            5,
            1
        ]
    },
    "ogremagi": {
        "id": 84,
        "roles": [
            6,
            2,
            5,
            4,
            3
        ]
    },
    "undying": {
        "id": 85,
        "roles": [
            6,
            4,
            5,
            2
        ]
    },
    "rubick": {
        "id": 86,
        "roles": [
            6,
            5,
            2
        ]
    },
    "disruptor": {
        "id": 87,
        "roles": [
            6,
            5,
            2,
            3
        ]
    },
    "nyxassassin": {
        "id": 88,
        "roles": [
            5,
            2,
            3,
            1
        ]
    },
    "nagasiren": {
        "id": 89,
        "roles": [
            0,
            6,
            7,
            5,
            3,
            1
        ]
    },
    "keeperofthelight": {
        "id": 90,
        "roles": [
            6,
            2,
            5
        ]
    },
    "wisp": {
        "id": 91,
        "roles": [
            6,
            1,
            2
        ]
    },
    "visage": {
        "id": 92,
        "roles": [
            6,
            2,
            4,
            5,
            7
        ]
    },
    "slark": {
        "id": 93,
        "roles": [
            0,
            1,
            5,
            2
        ]
    },
    "medusa": {
        "id": 94,
        "roles": [
            0,
            5,
            4
        ]
    },
    "trollwarlord": {
        "id": 95,
        "roles": [
            0,
            7,
            5,
            4
        ]
    },
    "centaur": {
        "id": 96,
        "roles": [
            4,
            3,
            5,
            2,
            1
        ]
    },
    "magnataur": {
        "id": 97,
        "roles": [
            3,
            5,
            2,
            1
        ]
    },
    "shredder": {
        "id": 98,
        "roles": [
            2,
            4,
            1
        ]
    },
    "bristleback": {
        "id": 99,
        "roles": [
            0,
            4,
            3,
            2
        ]
    },
    "tusk": {
        "id": 100,
        "roles": [
            3,
            5,
            2
        ]
    },
    "skywrathmage": {
        "id": 101,
        "roles": [
            6,
            2,
            5
        ]
    },
    "abaddon": {
        "id": 102,
        "roles": [
            6,
            0,
            4
        ]
    },
    "eldertitan": {
        "id": 103,
        "roles": [
            3,
            5,
            2,
            4
        ]
    },
    "legioncommander": {
        "id": 104,
        "roles": [
            0,
            5,
            3,
            4,
            2
        ]
    },
    "techies": {
        "id": 105,
        "roles": [
            2,
            5
        ]
    },
    "emberspirit": {
        "id": 106,
        "roles": [
            0,
            1,
            2,
            5,
            3
        ]
    },
    "earthspirit": {
        "id": 107,
        "roles": [
            2,
            1,
            5,
            3,
            4
        ]
    },
    "abyssalunderlord": {
        "id": 108,
        "roles": [
            6,
            2,
            5,
            4,
            1
        ]
    },
    "terrorblade": {
        "id": 109,
        "roles": [
            0,
            7,
            2
        ]
    },
    "phoenix": {
        "id": 110,
        "roles": [
            6,
            2,
            3,
            1,
            5
        ]
    },
    "oracle": {
        "id": 111,
        "roles": [
            6,
            2,
            5,
            1
        ]
    },
    "winterwyvern": {
        "id": 112,
        "roles": [
            6,
            5,
            2
        ]
    },
    "arcwarden": {
        "id": 113,
        "roles": [
            0,
            1,
            2
        ]
    },
    "monkeyking": {
        "id": 114,
        "roles": [
            0,
            1,
            5,
            3
        ]
    },
    "darkwillow": {
        "id": 119,
        "roles": [
            6,
            2,
            5,
            1
        ]
    },
    "pangolier": {
        "id": 120,
        "roles": [
            0,
            2,
            5,
            4,
            1,
            3
        ]
    },
    "grimstroke": {
        "id": 121,
        "roles": [
            6,
            2,
            5,
            1
        ]
    },
    "hoodwink": {
        "id": 123,
        "roles": [
            6,
            2,
            1,
            5
        ]
    },
    "voidspirit": {
        "id": 126,
        "roles": [
            0,
            1,
            2,
            5
        ]
    },
    "snapfire": {
        "id": 128,
        "roles": [
            6,
            2,
            5,
            1
        ]
    },
    "mars": {
        "id": 129,
        "roles": [
            0,
            3,
            5,
            4
        ]
    },
    "ringmaster": {
        "id": 131,
        "roles": [
            6,
            2,
            1,
            5
        ]
    },
    "dawnbreaker": {
        "id": 135,
        "roles": [
            0,
            4
        ]
    },
    "marci": {
        "id": 136,
        "roles": [
            6,
            0,
            3,
            5,
            1
        ]
    },
    "primalbeast": {
        "id": 137,
        "roles": [
            3,
            4,
            5
        ]
    },
    "muerta": {
        "id": 138,
        "roles": [
            0,
            2,
            5
        ]
    },
    "kez": {
        "id": 145,
        "roles": [
            0,
            1,
            5
        ]
    }
}

def create_modified_csv(directory, output_subfolder='modified_data'):
  """
  Iterates over CSV files in a directory, creates a DataFrame,
  calculates 'x_player_CBodyComponent.m_position' fields,
  adds 'x_player_isAlive' field, scales 'm_iHealth' to a
  0-1 range, drops original component fields, and saves the
  DataFrame to new CSV files with a "_modified" suffix.

  Args:
    directory: The path to the directory containing the CSV files.
    output_subfolder: The name of the subfolder to store the modified files.
  """
  columns_to_keep = ["hero",
    'm_iHealth', 'm_iMaxHealth', 'm_flMana', 'm_flMaxMana',
    'm_nTotalDamageTaken', 'm_iAttackRange', 'm_iDamageMin', 'm_iDamageMax', 'm_iDamageBonus',
    'm_hItems.0000', 'm_hItems.0001', 'm_hItems.0002', 'm_hItems.0003', 'm_hItems.0004', 'm_hItems.0005',
    'm_hItems.0006', 'm_hItems.0007', 'm_hItems.0008', 'm_hItems.0009', 'm_hItems.0010', 'm_hItems.0011',
    'm_hItems.0012', 'm_hItems.0013', 'm_hItems.0014','m_hItems.0015', 'm_hItems.0016', 'm_hItems.0017',
    'm_hItems.0018', 'm_iCurrentLevel', 'm_bIsMoving', 'm_MoveType',
    'm_iTaggedAsVisibleByTeam', 'm_iTeamNum', 'm_bVisibleinPVS',
    'CBodyComponent.m_cellX', 'CBodyComponent.m_cellY', 'CBodyComponent.m_cellZ',
    'CBodyComponent.m_vecX', 'CBodyComponent.m_vecY', 'CBodyComponent.m_vecZ'
]
  # Prepend 'x_player' to column names
  columns_to_keep = ['tick'] + [f'player_{i}_{col}' for i in range(10) for col in columns_to_keep]

  def getPositionComponent(row, cell_col, vec_col):
    """
    Calculates position from cell and vector components.

    Args:
      row: DataFrame row.
      cell_col: Name of the cell component column.
      vec_col: Name of the vector component column.

    Returns:
      float: Calculated position.
    """
    cell = row[cell_col]
    vec = row[vec_col]
    return cell * 128.0 + vec

  for filename in os.listdir(directory):
    process_time_start = time()
    if filename.endswith(".csv"):
      filepath = os.path.join(directory, filename)
      modified_filepath = os.path.join(directory, output_subfolder, filename[:-4] + "_modified.csv")

      # Read CSV into a DataFrame
      df = pd.read_csv(filepath)

      df = df[columns_to_keep]

      # Calculate and add new position columns
      for i in range(10):
        for axis in ['X', 'Y', 'Z']:
          df[f'player_{i}_CBodyComponent.m_position{axis}'] = df.apply(
              lambda row: getPositionComponent(
                  row,
                  f'player_{i}_CBodyComponent.m_cell{axis}',
                  f'player_{i}_CBodyComponent.m_vec{axis}'
              ),
              axis=1
          )

      # Drop original cell and vector columns
      columns_to_drop = []
      for i in range(10):
        for axis in ['X', 'Y', 'Z']:
          columns_to_drop.extend([
              f'player_{i}_CBodyComponent.m_cell{axis}',
              f'player_{i}_CBodyComponent.m_vec{axis}'
          ])
      df.drop(columns=columns_to_drop, inplace=True)

      for i in range(10):
        for j in range(i + 1, 10):  # Avoid calculating distance with self and duplicates
          df[f'player_{i}_distance_to_player_{j}'] = np.sqrt(
            (df[f'player_{i}_CBodyComponent.m_positionX'] - df[f'player_{j}_CBodyComponent.m_positionX'])**2 +
            (df[f'player_{i}_CBodyComponent.m_positionY'] - df[f'player_{j}_CBodyComponent.m_positionY'])**2 +
            (df[f'player_{i}_CBodyComponent.m_positionZ'] - df[f'player_{j}_CBodyComponent.m_positionZ'])**2
        )

            # Calculate average damage and add bonus for each player
      for i in range(10):
        df[f'player_{i}_average_damage'] = (df[f'player_{i}_m_iDamageMin'] + df[f'player_{i}_m_iDamageMax']) / 2 + df[f'player_{i}_m_iDamageBonus']

            # Drop the original damage columns
      columns_to_drop = []
      for i in range(10):
                columns_to_drop.extend([
                    f'player_{i}_m_iDamageMin',
                    f'player_{i}_m_iDamageMax',
                    f'player_{i}_m_iDamageBonus'
                ])
      df.drop(columns=columns_to_drop, inplace=True)

      # Add 'x_player_isAlive' columns
      for i in range(10):
        df[f'player_{i}_isAlive'] = (df[f'player_{i}_m_iHealth'] > 0).astype(int)

      # Scale 'm_iHealth' and replace original column
      for i in range(10):
        df[f'player_{i}_m_iHealth'] = (
            df[f'player_{i}_m_iHealth'] / df[f'player_{i}_m_iMaxHealth']
        ).fillna(0)  # Handle potential division by zero

        df[f'player_{i}_m_iHealth'] = (
            df[f'player_{i}_m_flMana'] / df[f'player_{i}_m_flMaxMana']
        ).fillna(0)  # Handle potential division by zero

      # Get all 'player_X_m_iCurrentLevel' column names
      level_cols = [col for col in df.columns if col.startswith('player_') and col.endswith('_m_iCurrentLevel')]

      for i in range(10):
        df[f'player_{i}_m_iTeamNum'] = df[f'player_{i}_m_iTeamNum'] % 2

      # Calculate the average level and add it as a new column
      df['average_level'] = df[level_cols].mean(axis=1)  # axis=1 for row-wise average

      for i in range(10):
        df[f'player_{i}_level_diff'] = df[f'player_{i}_m_iCurrentLevel'] - df['average_level']

      df.drop(columns=['average_level'], inplace=True)

      hero_cols = [col for col in df.columns if col.startswith('player_') and col.endswith('_hero')]

      df = df.dropna(subset=hero_cols, how='any')  # Drop if any hero column is null

      # Iterate over hero columns and map to IDs
      for hero_col in hero_cols:
        # Apply mapping function to the column
        df[hero_col] = df[hero_col].apply(
            lambda hero_name: hero_mapping.get((hero_name).replace('CDOTA_Unit_Hero_', '').replace('_', '').lower()).get('id')  # Extract hero name and get ID
        )
      # Save the modified DataFrame to a new CSV

      print(modified_filepath)
      df.to_csv(modified_filepath, index=False)

      # Benchmark
      print(f"file process of size {os.path.getsize(filepath)/1000000}MB took {time()-process_time_start:.2f} sec")