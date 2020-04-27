import fuzzy_system
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from mpl_toolkits.mplot3d import Axes3D


driving_sample = np.linspace(0, 100, 100)
journey_time_sample = np.linspace(0, 20, 20)
x, y = np.meshgrid(driving_sample, journey_time_sample)
z = np.zeros_like(x)
#output = []
dict_measurements = fuzzy_system.my_dictionary()

for i in range(20):
    for j in range(100):
        dict_measurements['driving'] = j
        dict_measurements['journey_time'] = i
        membership_value_dictionary = fuzzy_system.membership_value_calculation(dict_measurements, fuzzy_system.dict_fuzzy_sets)
        dict_rules_fuzzified = fuzzy_system.parse_calculate_rule(fuzzy_system.rule_list, membership_value_dictionary)
        z[i, j] =(fuzzy_system.defuzzification(fuzzy_system.dict_fuzzy_sets, dict_measurements, dict_rules_fuzzified))

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                       linewidth=0.4, antialiased=True)


ax.set_zlim(0, 200)

# cset = ax.contourf(x, y, z, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
# cset = ax.contourf(x, y, z, zdir='x', offset=3, cmap='viridis', alpha=0.5)
# cset = ax.contourf(x, y, z, zdir='y', offset=3, cmap='viridis', alpha=0.5)

ax.view_init(30, 200)
plt.show()