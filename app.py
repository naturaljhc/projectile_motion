import streamlit as st
import numpy as np

st.title("Projectile Motion Lab")

st.markdown("**NOTE: Make sure to write down ALL inputs AND outputs for the lab submission!**")
st.markdown("**NOTE: Make sure to write down ALL inputs AND outputs for the lab submission!**")
st.markdown("**NOTE: Make sure to write down ALL inputs AND outputs for the lab submission!**")
st.markdown("**NOTE: Make sure to write down ALL inputs AND outputs for the lab submission!**")
st.markdown("**NOTE: Make sure to write down ALL inputs AND outputs for the lab submission!**")

# Step 1: Input initial height of the launcher
st.header("Step 1: Enter the initial height of the launcher (h)")
st.write(r"1. Set the angle of the projectile launcher to $\theta = 0^\circ$.")
st.write(r"2. Measure the height, $h$, from the ground to the launch point.")
h = st.number_input("Initial height (meters)", value=0.0, format="%.3f")

# Step 2: Input ranges and calculate the average range
st.header("Step 2: Enter the ranges")
st.write(r"1. Use a plumb bob and tape it to the launch point.")
st.write(r"2. Mark the approximate spot on the floor with tape and then use a pen to mark the exact point on the tape. This is the origin.")
st.write(r"3. Launch a couple of test shots and keep track of where the ball landed.")
st.write(r"4. Tape a piece of a paper at the approximate location.")
st.write(r"5. Do a few more test shots to make sure the paper is in a good spot. If the ball lands outside of the paper, move it.")
st.write(r"6. Measure the distance from the origin (step 2) to the close side of the paper. We'll call this $x_1$.")
x1 = st.number_input(r"$x_1$ (meters)", value=0.0, format="%.3f")
st.write(r"7. Put a sheet of carbon paper over the taped piece of paper.")
st.write(r"8. Fire the projectile 25-40 times.")
st.write(r"9. Remove the carbon paper and measure the distance of each dot from the close side of the paper that was used in step 6. We'll call this $x_2$.")
st.write(r"Enter the measured ranges in meters. Only non-zero values will be included in the calculation for the average $R$.")

# Create columns to arrange input boxes
num_columns = 5  # Number of columns
input_boxes = []

columns = st.columns(num_columns)
for i in range(40):
    with columns[i % num_columns]:
        range_value = st.number_input(f"#{i+1}", value=0.0, format="%.3f")
        input_boxes.append(range_value)

# Filter out non-zero inputs
ranges = [value + x1 for value in input_boxes if value != 0.0]

# if (ranges and len(ranges) < 25):
#     st.header(r"Enter AT LEAST 25 values of $x_2$")
#     R = None
# el
if ranges:
    R = sum(ranges) / len(ranges)
    st.write(rf"Average Range ($R$): {R:.3f} meters")
else:
    R = None

# Calculate the initial velocity
if R is not None and h > 0:
    g = 9.8  # acceleration due to gravity in m/s^2
    v_0 = R * np.sqrt(g / (2 * h))
    st.write(rf"Initial Velocity ($v_0$): {v_0:.2f} m/s")
else:
    v_0 = None

# Step 3: Input the angle and new height of the launcher
st.header("Step 3: Using a new angle and height of the launcher")
st.write(r"1. Set the launcher to the desired angle.")
st.write(r"2. (Optional) Re-measure the height of the launch point - this will be set to the height from step 1 by default. Setting a new angle may change the initial position slightly depending on the pivot point. If you choose to re-measure the height, the change in the range will be accounted for by using")
st.latex(r"\Delta x = \frac{\Delta h}{\sin\theta} - \Delta h\cot\theta")
theta = st.number_input("Angle (degrees)", value=0.0, format="%.1f")
h_0 = st.number_input("New height (meters)", value=h, format="%.3f")

if h_0 == h:
    delx = 0.0
else:
    delh = h_0 - h
    theta_rad = np.radians(theta)
    delx = delh/np.sin(theta_rad) - delh/np.tan(theta_rad)

# Step 4: Determining where to put the can
st.header("Step 4: Where to put the can:")
if v_0 is not None and theta >= 0 and h_0 >= 0:
    theta_rad = np.radians(theta)
    theoretical_R = (v_0 * np.cos(theta_rad) * 
                      (v_0 * np.sin(theta_rad) + np.sqrt((v_0 * np.sin(theta_rad))**2 + 2 * g * h_0))) / g + delx
    st.write(rf"Place the can on the floor, {theoretical_R:.3f} meters in front of the launch point")

# Step 5: Where to put the hoop
st.header("Step 5: Where to put the hoop:")
st.write(r"There are two options for this step. Option 1 uses the max height of the ball. Option 2 finds the point when the ball falls down to height of the launcher again.")
st.header("Step 5a:")
if v_0 is not None and theta >= 0 and h_0 >= 0:
    # Calculate the maximum height
    h_max = (v_0 * np.sin(theta_rad))**2 / (2 * g) + h_0
    # st.write(rf"y = {h_max:.2f} meters")
    
    # Calculate the locations for the hoop
    x_max = v_0**2*np.sin(2*theta_rad)/(2*g) + delx
    # st.write(f"x = {x:.2f} meters")

    st.write(rf"Set the hoop at $(x, y) = (${x_max:.2f} m$,$ {h_max:.2f} m$)$ relative to the origin")

st.header("Step 5b:")
if v_0 is not None and theta >= 0 and h_0 >= 0:
    x_par = v_0**2*np.sin(2*theta_rad)/(g) + delx
    # st.write(f"x = {x:.2f} meters")

    st.write(rf"Set the hoop at $(x, y) = (${x_par:.2f} m$,$ {h_0:.2f} m$)$ relative to the origin")

import matplotlib.pyplot as plt

if v_0 is not None:
    x_vals = np.linspace(0, theoretical_R, 10000)
    y_vals = -g/(2*(v_0*np.cos(theta_rad))**2)*x_vals**2 + x_vals*np.tan(theta_rad) + h_0
    
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.scatter(theoretical_R, 0, color = 'k')
    ax.text(theoretical_R, .03*h_max, f'({theoretical_R:.2f}, {0.00})', color='black', fontsize=12, ha='right')
    ax.scatter(x_max, h_max, color = 'k')
    ax.text(x_max, 1.03*h_max, f'({x_max:.2f}, {h_max:.2f})', color='black', fontsize=12, ha='left')
    if h_0 != h_max:
        ax.scatter(x_par, h_0, color = 'k')
        ax.text(x_par, h_0 - .05*h_max, f'({x_par:.2f}, {h_0:.2f})', color='black', fontsize=12, ha='left')
    ax.set_ylim(-.05*h_max, 1.1*h_max)
    ax.set_xlim(0, 1.1*theoretical_R)
    ax.set_xlabel("Distance (m)", fontsize = 14)
    ax.set_ylabel("Height (m)", fontsize = 14)
    ax.set_title("Projectile Motion", fontsize = 18)
    ax.grid()
    st.pyplot(fig)
