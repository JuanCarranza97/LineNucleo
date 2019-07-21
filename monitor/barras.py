import matplotlib.pyplot as plt

fig = plt.figure("Line Follower Sensors",   figsize=(10,5), dpi=100) # Figure
ax = fig.add_subplot(111) # Axes

nombres = ['Sen 1','Sen 2','Sen 3','Sen 4','Sen 5','Sen 6','Sen 7','Sen 8','Sen 9','Sen 10','Sen 11','Sen 12','Sen 13','Sen 14','Sen 15','Sen 16']
datos = [100,200,300,400,500,600,700,800,800,700,600,500,400,300,200,100]

ax.bar(range(len(datos)), datos, width=.5, align='center')
ax.set_xticks(xx)
ax.set_xticklabels(nombres)

plt.show()