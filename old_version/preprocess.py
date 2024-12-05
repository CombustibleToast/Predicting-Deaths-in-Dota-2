import pandas as pd 


if __name__ == "__main__":
    master = pd.read_csv('master.csv')
    col_name = ['tick']
    for col in master.columns.to_list()[1:]:
        col_unit = col[9:]
        if col_unit not in col_name:
            col_name.append(col_unit)
    
    processed = pd.DataFrame(columns=col_name)
    player_lst = []
    lst_y = []

    for player in range(10):
        col_unit = ['tick'] + [f'player_{player}_'+col for col in col_name if col!='tick']
        
        unit = master[col_unit]
        unit = unit.iloc[:-1]
        player_lst += [player for _ in range(unit.shape[0])]
        unit.columns = col_name

        lst_tick_y = unit[unit['m_iHealth']==0]['tick'].to_list()   
    
        lst_y_unit = []

        end_idx=0
        lst_check = [int(t) for t in unit['tick'].to_list()]

        for u in range(unit.shape[0]):
            delta =  int(lst_tick_y[end_idx]) - lst_check[u]
            if delta < 0:
                if end_idx == len(lst_tick_y)-1:
                    delta = -30
                else:
                    end_idx += 1
                    delta = int(lst_tick_y[end_idx]) - lst_check[u]
            
            lst_y_unit.append(delta/30)

        lst_y += lst_y_unit
        processed = pd.concat([processed,unit], axis=0, ignore_index=True)

    processed['player'] = player_lst
    processed['y'] = lst_y
    lst_y_classify = []
    for y in lst_y:
        if y == -1:
            lst_y_classify.append(y)
        elif y <= 5:
            lst_y_classify.append(1)
        else:
            lst_y_classify.append(0)

    processed['y_classify'] = lst_y_classify
    processed.to_csv('processed.csv')
    print(processed)
