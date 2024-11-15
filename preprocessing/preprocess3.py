import pandas as pd
import os
import numpy as np
from time import time
import json

hero_mapping = json.load(open("heroes_parsed.json"))

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
            lambda hero_name: hero_mapping.get((hero_name).split('_')[-1].lower())['id']  # Extract hero name and get ID
        )
      # Save the modified DataFrame to a new CSV

      print(modified_filepath)
      df.to_csv(modified_filepath, index=False)

      # Benchmark
      print(f"file process of size {os.path.getsize(filepath)/1000000}MB took {time()-process_time_start:.2f} sec")
      break # REMOVE TO DO ALL FILES!