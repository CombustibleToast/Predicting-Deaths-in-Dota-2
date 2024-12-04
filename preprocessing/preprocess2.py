import pandas as pd

data_path = "./data/"
sample_filename = "sample.dem.csv"

def process_file(filename):
	raw = pd.read_csv(f"{data_path}{filename}")
    
	player_teams = []
	for i in range(10):
		player_teams.append(f"player_{i}_m_iTeamNum")
	teams = raw[player_teams]
	print(teams)
    

if __name__ == "__main__":
    # For now, process a single sample file
    process_file(sample_filename)