#import python libraries
import numpy as np
import matplotlib.pyplot as plt
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

def record(f, y_0, t_span, args, epsilon = 1e-7, t_eval = None, output_file = "output"): 
    ''' 
    Use scipy.integrate.solve_ivp to solve ode system
    Note that t_eval allows user to pass array of times to be stored
    This is important for STROBOSCOPE
    ---- > From scipy documentation :
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html:
    t_eval
    array_like or None, optional
    Times at which to store the computed solution, 
    must be sorted and lie within t_span. 
    If None (default), use points selected by the solver.

    Usage:
    sol, path = record(pendulum, u0, t_span, args)
    sol has attributes sol.y (array of arrays with y values) and sol. t
    Integration result are stored in compressed file
    '''

    #See np.integrate.solve_ivp for more information
    sol = solve_ivp(f, t_span, y_0, args=args, vectorized = True, rtol=epsilon, atol=epsilon)
    #Store simulation as compressed filed in data folder
    path = "y0=" + str(u0) + "-t0=" + str(t_span[0])+"-t1=" + str(t_span[1]) \
                +"-gamma="+str(args[0])+"-mu="+str(args[1])+"-omega="+str(args[2])+"-eps="+str(epsilon)+".npz"
    np.savez_compressed(path, t = sol.t, u1 = sol.y[0], u2 = sol.y[1], u3 = sol.y[2])
    return sol, path

def load(path):
    '''
    Take path as string, fix boundaries
    Return t, y1 and y2 array
    '''
    
    data = np.load(path)
    t = data['t']
    u1 = data['u1']
    u2 = data['u2']
    u3 = data['u3']
    return np.array([u1, u2, u3])

import matplotlib.path as mpath
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection

def make_segments(x, y, z):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """

    points = np.array([x, y, z]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments

def colorline(x, y, z, w=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0),
        linewidth=3, alpha=1.0):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """

    # Default colors equally spaced on [0,1]:
    if w is None:
        w = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(w, "__iter__"):  # to check for numerical input -- this is a hack
        w = np.array([w])

    w = np.asarray(w)

    segments = make_segments(x, y, z)
    lc = Line3DCollection(segments, array=w, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)

    ax = plt.gca(projection='3d')
    ax.add_collection(lc)
    return lc


def plot_phase_diagram(x, y, z, args, xlim = [-np.pi, np.pi], ylim = [-1,1], zlim = [-1, 1], cmap = 'copper', animate=False):
    '''
    Note that YlOrRd-colourmap (https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html)
    is light yellow for early times and dark red for late times
    '''
    plt.close()
    fig = plt.figure(figsize=(6,6), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    ax.set_xlim([-70, 70])
    ax.set_ylim([-70, 70])
    ax.set_zlim([0, 50])
    ax.set_title('Lorenz Attractor: Pr ={:.0f}, r={:.2f}, b ={:.2f}'.format(args[0], args[1], args[2]))
    ax.add_collection(colorline(x, y, z, cmap='copper', linewidth=0.5))

    if animate: 
        plt.axis('off')
        for angle in range(360):
            ax.view_init(elev=30*np.sin(2*np.pi*angle/360), azim=angle)
            plt.savefig("videoframes/frame{}.png".format(angle))
        import sheet5_video
        sheet5_video.generate_video("videoframes")
    else:
        ax.scatter(x, z, zdir='y', c=np.linspace(0.0, 1.0, len(x)), cmap=cmap, s=0.02, zs=70)
        ax.scatter(y, z, zdir='x', c=np.linspace(0.0, 1.0, len(x)), cmap=cmap, s=0.02, zs=-70)
        ax.scatter(x, y, zdir='z', c=np.linspace(0.0, 1.0, len(x)), cmap=cmap, s=0.02, zs=0)
        plt.savefig("sheet5_ex1_phase_diagramm.png")

def anifunc(n, ax, x, y, z, cmap):
    ax.view_init(elev=30*np.sin(2*np.pi*n/36), azim=n*10)
    lc = ax.add_collection(colorline(x, y, z, cmap='copper', linewidth=0.5))
    return ax, lc

def plot_trajectory(t, y, args):
    plt.close()
    plt.figure(figsize=(10, 5), dpi=300)
    plt.xlabel(r"$\tau$")
    plt.ylabel(r'$u_3$')
    plt.title('Trajectory of Lorenz map')
    
    plt.plot(t,y, color='grey', label="\n".join(
        [r'Pr ={:.2f}'.format(args[0]),
         r'r={:.2f}'.format(args[1]),
         r'b ={:.2f}'.format(args[2])]))
    plt.legend()
    plt.savefig("sheet5_ex1_trajectory.png")

#Initial values of ODE
t0 = 0
#Start in static equilibrium
u0 = np.array([0., 1.0, 1.05])


#Parameters of L63
Pr=10
r=28
b=2.667

args = [Pr, r, b]

#Precision of integration
epsilon = 1e-8
#Time for integration
t_span = [0., 100]

sol, path = record(lorenz, u0, t_span, epsilon=epsilon, args=args)

plot_phase_diagram(sol.y[0], sol.y[1], sol.y[2], args)
plot_phase_diagram(sol.y[0], sol.y[1], sol.y[2], args, animate=True)
