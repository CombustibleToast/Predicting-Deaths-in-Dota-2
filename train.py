from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

if __name__=="__main__":
    data = pd.read_csv('processed.csv')
    data = data[data['y']>0]

    data_pick = data.drop(['tick', data.columns[0],'hero'], axis=1)
    print(data_pick.shape)

    X = data[[
        'm_iHealth', 'm_iMaxHealth', 'm_flMana', 'm_flMaxMana', 'm_flHealthRegen', 'm_flManaRegen',
        'm_nTotalDamageTaken', 'm_iAttackRange', 'm_iDamageMin', 'm_iDamageMax', 'm_iDamageBonus',
        'm_hItems.0000', 'm_hItems.0001', 'm_hItems.0002', 'm_hItems.0003', 'm_hItems.0004', 'm_hItems.0005', 'm_hItems.0006', 'm_hItems.0007', 
        'm_hItems.0008', 'm_hItems.0009', 'm_hItems.0010', 'm_hItems.0011', 'm_hItems.0012', 'm_hItems.0013', 'm_hItems.0014',
        'm_hItems.0015', 'm_hItems.0016', 'm_hItems.0017', 'm_hItems.0018',
        'm_iCurrentLevel', 'm_iCurrentXP', 'm_bIsMoving', 
        'm_MoveType', 'm_iTaggedAsVisibleByTeam', 'm_iTeamNum', 'm_bVisibleinPVS'
        ]]

    #X = data_pick
    y = data['y_classify']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=16)


    clf = RandomForestClassifier()

    model = clf.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    
    print(classification_report(y_test, y_pred))
