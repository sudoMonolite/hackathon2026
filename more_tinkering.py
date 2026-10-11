import numpy as np
import math

# Geometry functions oren spent 6 hours on
# Also oren please comment your work
# No one understands ts math
#nah wdym its perfectly understandable
#js lock in
plane=[[[-0.02,-0.004,0],[-0.02,0.001,0],[0.04,0.001,0]],[[-0.02,-0.004,0],[0.04,-0.004,0],[0.04,0.001,0]],[[-0.02,0.001,-0.03],[-0.02,0.001,0.03],[0.04,0.001,0]],[0.01,0,0]]
def test_plane(plane, launch_direction, launch_speed):
    def center_of_mass_triangle(points):
        side1=math.sqrt(((points[1][0]-points[0][0])**2)+((points[1][1]-points[0][1])**2)+((points[1][2]-points[0][2])**2))
        side2=math.sqrt(((points[2][0]-points[0][0])**2)+((points[2][1]-points[0][1])**2)+((points[2][2]-points[0][2])**2))
        side3=math.sqrt(((points[1][0]-points[2][0])**2)+((points[1][1]-points[2][1])**2)+((points[1][2]-points[2][2])**2))
        s=(side1+side2+side3)/2
        trianglemass=math.sqrt(s*(s-side1)*(s-side2)*(s-side3))
        return([round(((points[0][0]+points[1][0]+points[2][0])/3)*1000000)/1000000,round(((points[0][1]+points[1][1]+points[2][1])/3)*1000000)/1000000,round(((points[0][2]+points[1][2]+points[2][2])/3)*1000000)/1000000,round(trianglemass*1000000)/1000000])

    def weighted_center_of_mass(masspoints):
        xvalues=0
        yvalues=0
        zvalues=0
        totalmass=0
        for i in range(len(masspoints)):
            xvalues+=(masspoints[i][0])*(masspoints[i][3])
            yvalues+=(masspoints[i][1])*(masspoints[i][3])
            zvalues+=(masspoints[i][2])*(masspoints[i][3])
            totalmass+=masspoints[i][3]
        return([round(xvalues/totalmass*1000000)/1000000,round(yvalues/totalmass*1000000)/1000000,round(zvalues/totalmass*1000000)/1000000])

    def point_in_triangle(vertex1, vertex2, vertex3, point):
        tolerance=0.000000001
        vertex1,vertex2,vertex3,point = map(np.array,[vertex1,vertex2,vertex3,point])
        vector1,vector2,vector3 = (vertex3 - vertex1),(vertex2-vertex1),(point-vertex1)
        dot00=np.dot(vector1, vector1)
        dot01=np.dot(vector1, vector2)
        dot02=np.dot(vector1, vector3)
        dot11=np.dot(vector2, vector2)
        dot12=np.dot(vector2, vector3)
        denom=(dot00*dot11-dot01*dot01)
        if abs(denom)<0.000000001:
            return False
        u=(dot11*dot02-dot01*dot12)/denom
        v=(dot00*dot12-dot01*dot02)/denom
        normal=np.cross(vector1,vector2)
        if(np.abs(np.dot(normal,vector3))/np.linalg.norm(normal))<=tolerance:
            if (u>=-tolerance) and (v>=-tolerance) and (u+v<=1.0+tolerance):
                return True
        return(False)
        

    masspoints=[]
    for i in range(len(plane)-1):
        masspoints.append(center_of_mass_triangle(plane[i]))

    center_of_mass=weighted_center_of_mass(masspoints)

    center_of_mass_offset=plane[len(plane)-1]
    point_final=[]
    for i in range(1000):
        point_check=[center_of_mass[0]+(1+i/100)*center_of_mass_offset[0],center_of_mass[1]+(1+i/100)*center_of_mass_offset[1],center_of_mass[2]+(1+i/100)*center_of_mass_offset[2]]
        ye_or_no=False
        for k in range(len(plane)-1):
            if point_in_triangle(plane[k][0],plane[k][1],plane[k][2],point_check):
                ye_or_no=True
        if ye_or_no:        
            point_final=point_check
    if point_final==[]:
        weight=999999
    else:
        leverage_value=math.sqrt(((point_final[0]-(center_of_mass[0]+center_of_mass_offset[0]))**2)+((point_final[1]-(center_of_mass[1]+center_of_mass_offset[1]))**2)+((point_final[2]-(center_of_mass[2]+center_of_mass_offset[2]))**2))
        offset_value=math.sqrt((center_of_mass_offset[0]**2)+(center_of_mass_offset[1]**2)+(center_of_mass_offset[2]**2))
        first_weight=0
        for j in range(len(plane)-1):
            first_weight+=center_of_mass_triangle(plane[j])[3]
        weight=(round(((first_weight*2381)+((first_weight*2381)/(leverage_value/offset_value)))*1000000))/1000000
    plane.append(weight)

    xconstant=-(center_of_mass[0]+center_of_mass_offset[0])
    yconstant=-(center_of_mass[1]+center_of_mass_offset[1])
    zconstant=-(center_of_mass[2]+center_of_mass_offset[2])

    for l in range(len(plane)-2):
        for u in range(3):
            plane[l][u][0]+=xconstant
            plane[l][u][1]+=yconstant
            plane[l][u][2]+=zconstant
    plane[len(plane)-2]=[0,0,0]

    triangles = [item for item in plane if isinstance(item, list) and len(item) == 3 and isinstance(item[0], list)]
    num_triangles = len(triangles)

    masspoints = []
    for i in range(num_triangles):
        masspoints.append(center_of_mass_triangle(triangles[i]))

    center_of_mass = weighted_center_of_mass(masspoints)

    # x coordinate extraction for bounds of graph
    all_x_coords = [vertex[0] for t in triangles for vertex in t]
    min_x, max_x = min(all_x_coords), max(all_x_coords)
    total_length = max_x - min_x

    # center of mass alignments for flight physics
    geometric_center_x = (min_x + max_x) / 2.0
    com_x = center_of_mass[0]

    max_bias_angle = np.radians(15.0)
    com_percentage_shift = (com_x - geometric_center_x) / (total_length / 2.0)
    com_pitch_bias = com_percentage_shift * max_bias_angle

    # units and such
    # they in SI units btw
    g = 9.81
    m = 0.005  
    rho = 1.225  
    wing_area = 0.023
    W = m * g

    cl_alpha = 4.5       
    cl0 = 0.1            
    cd0 = 0.02           
    k = 0.15             


    # Physics things
    def flightvectors(state):
        # state tracks: [velocity, flight_path_angle (launch_direction), pitch_angle, pitch_rate]
        v, launch_direction, pitch, pitch_rate = state

        if v <= 0.001: 
            v = 0.001

        # dynamic angle of attack
        alpha = pitch - launch_direction - com_pitch_bias

        lift_coefficient = cl0 + cl_alpha * alpha
        drag_coefficient = cd0 + k * (lift_coefficient ** 2)

        L = 0.5 * rho * v**2 * wing_area * lift_coefficient
        D = 0.5 * rho * v**2 * wing_area * drag_coefficient

        force_along_path = -D - W * np.sin(launch_direction)
        force_perp_path = L - W * np.cos(launch_direction)

        forward_accel = force_along_path / m
        angular_accel = force_perp_path / (m * v)
        
        stiffness_torque = -15.0 * alpha  
        damping_torque = -2.5 * pitch_rate  
        pitch_accel = stiffness_torque + damping_torque

        return np.array([forward_accel, angular_accel, pitch_rate, pitch_accel])

    # W Runge and Kutta
    def rk4step(state, deltat):
        k1 = flightvectors(state)
        k2 = flightvectors(state + 0.5 * deltat * k1)
        k3 = flightvectors(state + 0.5 * deltat * k2)
        k4 = flightvectors(state + deltat * k3)
        return state + (deltat / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

    # After 15 hours of work:
    init_angle = np.radians(30)
    # state: [velocity, flight_path_angle, nose_pitch, pitch_rate]
    state = np.array([12.0, init_angle, init_angle, 0.0])

    # starting x and y pos
    x, y = 0.0, 10.0
    deltat = 0.01
    stepcount = 0

    print(f"Simulation Start (Triangles Counted: {num_triangles} | CoM Shift: {com_percentage_shift*100:.1f}%)")

    trajectory = [(x, y)]

    while y > 0 and stepcount < 2000:
        stepcount += 1
        state = rk4step(state, deltat)
        launch_speed, current_theta, current_pitch, _ = state

        if np.isnan(launch_speed) or launch_speed < 0.1:
            print(f"\nStep {stepcount}: The plane lost all its forward velocity or stalled!")
            break

        x += launch_speed * np.cos(current_theta) * deltat
        y += launch_speed * np.sin(current_theta) * deltat

        # stepcount % (n), n is how many 0.01 seconds in a step
        if stepcount % 1 == 0:
            aoa_deg = np.degrees(current_pitch - current_theta)
            print(f"Time: {stepcount*deltat:.2f}s | Pos: ({x:.2f}, {y:.2f}) | Speed: {launch_speed:.2f} m/s | Path: {np.degrees(current_theta):.1f}° | Nose Pitch: {np.degrees(current_pitch):.1f}° | AoA: {aoa_deg:.1f}°")
            
            trajectory.append((x, y))

    print("Simulation End")

    # Took me an hour too long
    print("\nTrajectory History")
    formatted_trajectory = ", ".join([f"({x_val:.2f}, {y_val:.2f})" for x_val, y_val in trajectory])
    return trajectory

#return list where first value is total distance travelled, everything after that is the collected

