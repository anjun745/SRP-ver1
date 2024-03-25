import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 101)
print(x)
fig = plt.figure()
plt.plot(x*100, (x**0.5)*10)
plt.ylabel('Tying Percentage')
plt.xlabel('Match Count')
plt.show()
fig.savefig('data_prediction', bbox_inches='tight')
