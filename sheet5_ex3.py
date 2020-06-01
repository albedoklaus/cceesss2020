import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from scipy.integrate import solve_ivp

def lorenz(t, u, Pr=10, r=28, b=2.667):
    '''
    Given:
       x, y, z: a point of interest in three dimensional space
       s, r, b: parameters defining the lorenz attractor
    Returns:
       x_dot, y_dot, z_dot: values of the lorenz attractor's partial
           derivatives at the point x, y, z
    '''
    x_dot = Pr*(u[1] - u[0])
    y_dot = r*u[0] - u[1] - u[0]*u[2]
    z_dot = u[0]*u[1] - b*u[2]
    return [x_dot, y_dot, z_dot]

#Square roots are evil! This is seven times faster than np.linalg.norm
def dist(x,y):
    return (x[0] - y[0])**2+(x[1] - y[1])**2+(x[2] - y[2])**2

#Construct array for initial values and colours
#stride through [-a, a] x [-a,a] x c with step_size
def construct_array(a, c, step_size):
    n = int(2*a/step_size) + 1
    u = np.zeros((n,n,3), dtype=np.float32)
    for i in range(0, n):
        for j in range(0,n):
            u[i][j] = [-a + i*step_size, -a + j*step_size, c]
    bitmap = np.zeros((n,n), dtype=np.int32)
    return u, bitmap

#This is where the magic happens
#1. Create array with values of u
#2. Loop over initial values
#3. Integrate until condition is met or time reaches t1
#4. Store index of the fixpoint to which the trajectory converged in colour array
#   Store index '3' if trajectory has not converged sufficiently close within [t0, t1]
def run(a, b, c, r, grid_resolution, crit_dist, args, epsilon, t_span):    
    #Array suggested in exercise
    #Note that the center of the coordinate system (-a, -a, z) is in the upper left corner of the bitmap array
    #We access specific coordinates like bitmap [y] [x]
    u0, bitmap = construct_array(a, c, grid_resolution)

    #Fixpoints as functions of lorenz map arguments
    fp = [np.array([0,0,0]), np.array([ np.sqrt(b*(r-1)), np.sqrt(b*(r-1)), r-1]), np.array([-np.sqrt(b*(r-1)),-np.sqrt(b*(r-1)), r-1])] 

    #Allocating this memory beforehand also saves a few µs per call
    event_buf = np.zeros(3, dtype=np.float32)

    #Condition to terminate integration
    #Conditions is met when event(t, u)= 0
    def event(t, u, Pr,r,b):
        #Compute distances to Fixpoints
        event_buf[0] = dist(u, fp[0])
        event_buf[1] = dist(u, fp[1])
        event_buf[2] = dist(u, fp[2])
        #Return minimal distance - critical distance
        #Integrator uses Newton solver to check for roots
        return np.min(event_buf) - crit_dist

    #Flag to make integrator terminate when condition is met
    event.terminal = True

    #Loop over initial values
    for i in range(0, len(u0)):
        for j in range(0, len(u0[0])):
            sol = solve_ivp(lorenz, t_span, u0[i][j], args=args, t_eval = [0], events = event, vectorized = True, rtol=epsilon, atol=epsilon)

            #sol.status one indicates that event has been triggered
            if sol.status == 1:
                #Store index of fixpoint to which trajectory converged in array
                bitmap[i][j] = np.argmin(event_buf)
            else:
                #Store 
                bitmap[i][j] = 3         
     #Store simulation as compressed file in data folder
    path = "Data/t0={}-t1={}-Pr={}-r={}-b={}-eps={}-a={}-grid_res={}-c={}.npz".format(*t_span, *args, epsilon, a, grid_resolution, c)
    
    np.savez_compressed(path, colormap = bitmap)
    
    return u0, bitmap

def plot_colormap(bitmap, a, c, Pr, r, b):
    plt.close()
    cmap = plt.get_cmap('copper')
    bounds=[-0.5,0.5,1.5,2.5,3.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    ticks=[0,1,2,3]
    
    fig, ax = plt.subplots()

    # tell imshow about color map so that only set colors are used
    img  = ax.imshow(bitmap, origin='upper', cmap=cmap, norm=norm, extent=[-a, a, a, -a])
    
    ax.set_ylabel('$u_2$')
    ax.set_xlabel('$u_1$')
    ax.set_title('$u_3$ = {}, Pr = {}, r = {}, b = {}'.format(c, Pr, r, b))
    
    # make a color bar
    cbar = fig.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=ticks)
    
    cbar.ax.set_yticklabels(['Converged to $u_0$', 'Converged to $u_+$', 'Converged to $u_-$', 'Did not converge'])  # horizontal colorbar
    plt.savefig("Data/bitmap_r{}.png".format(r))

def createPlot(r):
    #Initial values of ODE
    t0 = 0
    t1 = 50
    t_span = [t0, t1]

    #Parameters of L63
    Pr=10.
    b=2.667

    #Computing precision
    epsilon = 1e-8

    #Size of grid for initial values
    a = 30.
    c = 0.
    grid_resolution = 1

    #Critical distance to determine whether trajectory has converged to FP
    #Square it because we use squared distance
    crit_dist = 1e-8

    args = [Pr, r, b]

    try:
        path = "Data/t0={}-t1={}-Pr={}-r={}-b={}-eps={}-a={}-grid_res={}-c={}.npz".format(*t_span, *args, epsilon, a, grid_resolution, c)
        bitmap = np.load(path)['colormap']
    except FileNotFoundError:
        _, bitmap = run(a, b, c, r, grid_resolution, crit_dist, args, epsilon, t_span)
    finally:
        plot_colormap(bitmap, a, c, *args)  

if __name__ == "__main__":
    r = np.arange(1, 25.5, step=0.5)
    from multiprocessing import Pool
    with Pool(processes=7) as pool:
        pool.map(createPlot, r)