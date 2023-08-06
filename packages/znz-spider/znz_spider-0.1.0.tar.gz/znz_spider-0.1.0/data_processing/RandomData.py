import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

class Random_list():
    def __init__(self, datas):
        self.random_list = []
        self.datas = datas

    def test_learnning(self, test_filname, sep=',',add_filname='clear_data.txt'):
        ddis = []
        test_data = pd.read_csv(test_filname)
        test_x, test_y = test_data.iloc[:, :-1], test_data.iloc[:, -1]
        rf = RandomForestClassifier(n_estimators=10)
        for inds in self.random_list:
            X, Y = self.datas.iloc[inds, :-1], self.datas.iloc[inds, -1]
            rf.fit(X, Y)
            ddis.append(rf.score(test_x, test_y))
        with open(add_filname, 'w',encoding='utf-8') as w:
            [w.write(list(self.datas)[listname] +
                     (sep if listname != len(list(self.datas)) - 1 else '\n'))
             for listname in range(len(list(self.datas)))]
            [w.write(str(i[j]) + (sep if j != len(i) - 1 else '\n'))
             for i in self.datas.iloc[self.random_list[ddis.index(sorted(ddis)[-1])]].values
             for j in range(len(i))]

    def ran_list(self, hang=5, cout=20):
        self.random_list = [self.ran_out_list(self.datas, cout) for i in range(hang)]

    def ran_out_list(self, datas, cout):
        out_ind = []
        for jishu in range(cout):
            dis = self.ran_in_list(datas)
            [out_ind.append(ii) for ii in [dis.index(x_dis) for x_dis in sorted(dis)[:5]]]
        return list(set(out_ind))

    def ran_in_list(self, datas):
        index_num = random.choice(range(len(datas)))
        return [((datas.iloc[index_num][0] - datas.iloc[ind][0]) ** 2 +
                 (datas.iloc[index_num][1] - datas.iloc[ind][1]) ** 2 +
                 (datas.iloc[index_num][2] - datas.iloc[ind][2]) ** 2) ** 0.5
                for ind in range(len(datas))]
