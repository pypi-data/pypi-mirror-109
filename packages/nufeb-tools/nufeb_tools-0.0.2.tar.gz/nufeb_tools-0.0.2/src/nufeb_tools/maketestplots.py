from nufeb_tools import utils, plot
import matplotlib.pyplot as plt
import seaborn as sns
# x = utils.get_data(r'D:\CADES Files\runs\Run_15_75_56_1')
x2 = utils.get_data(directory = None,test=True)
f, axes = plt.subplots(ncols=3,nrows=2)
for ax in axes.ravel():
    x2.plot_overall_growth(ax)
f, ax = plt.subplots()
sns.set_context('talk')
sns.set_style('white')
plot.average_nutrients(x2.avg_con,'Sucrose',color='Green',legend=True)
f.tight_layout()
f.savefig('plot.average_nutrients.png')
# x.avg_con
# x2.avg_con
