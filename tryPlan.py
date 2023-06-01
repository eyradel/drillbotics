import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from well_plan.well import InterpWell


my_well = InterpWell()
my_well.interpolator = "PchipInterpolator"
my_well.kop = 300

df, tc = my_well.output_data

fig = plt.figure(figsize=(12, 8))

ax = fig.add_subplot(1, 1, 1, projection="3d")

print(tc["Z"])
ax.plot(df["X"], df["Y"], df["Z"], linewidth=5)
ax.scatter(tc["X"], tc["Y"], tc["Z"], c='r', marker='o', label='Targets')


ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_title("Pchip")
plt.gca().invert_zaxis()

fig.tight_layout()
df.to_csv('planData.csv')
plt.show()
# st.pyplot(fig)
