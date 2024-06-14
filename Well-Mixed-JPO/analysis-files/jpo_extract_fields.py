"""
Extract field values at the final time from the last checkpoint file.

Usage:
    jpo_extract_fields.py <foldername>... [--filename=<filename>]

Options:
    --filename=<filename>  	file name [default: last]
"""

import numpy as np
import h5py, re, pathlib, os
from docopt import docopt
args = docopt(__doc__)

filename = args['--filename']
foldername = args['<foldername>'][0]
print(foldername)
print(__file__)
source = foldername+'checkpoints/'
last_file_num = len([entry for entry in os.listdir(source) if os.path.isfile(os.path.join(source, entry))])

last_file = source+'checkpoints_s%i.h5'%last_file_num
print(last_file_num,last_file)

regex = re.compile(r'\d+')
Re, At, Pr, Le, _, TD100000,  _, _ = [int(x) for x in regex.findall(last_file)]

data = h5py.File(str(last_file), mode='r')
x = data['tasks/p'].dims[1][0][:].ravel()
y = data['tasks/p'].dims[2][0][:].ravel()
z = data['tasks/p'].dims[3][0][:].ravel()
t = data['scales/sim_time'][-1]
dt = data['scales/timestep'][-1]
p = data['tasks/p'][-1]
u = data['tasks/u'][:][-1]
tau_p = data['tasks/tau_p'][-1]
tau_u1 = data['tasks/tau_u1'][:][-1]
tau_u2 = data['tasks/tau_u2'][:][-1]
if Le<1000:
  T = data['tasks/T'][-1]
  S = data['tasks/S'][-1]
  tau_T1 = data['tasks/tau_T1'][-1]
  tau_T2 = data['tasks/tau_T2'][-1]
  tau_S1 = data['tasks/tau_S1'][-1]
  tau_S2 = data['tasks/tau_S2'][-1]
  np.savez(filename+'_%i_%i_%i_%i_%i.npz'%(Re,At,Pr,Le,TD100000),t=t,dt=dt,x=x,y=y,z=z,T=T,S=S,u=u,p=p,tau_p=tau_p,tau_u1=tau_u1,tau_u2=tau_u2,tau_T1=tau_T1,tau_T2=tau_T2,tau_S1=tau_S1,tau_S2=tau_S2)
else:
  TD = data['tasks/TD'][-1]
  tau_TD1 = data['tasks/tau_TD1'][-1]
  tau_TD2 = data['tasks/tau_TD2'][-1]
  np.savez(filename+'_%i_%i_%i_%i_%i.npz'%(Re,At,Pr,Le,TD100000),t=t,dt=dt,x=x,y=y,z=z,TD=TD,u=u,p=p,tau_p=tau_p,tau_u1=tau_u1,tau_u2=tau_u2,tau_TD1=tau_TD1,tau_TD2=tau_TD2)

print(p.shape,z.shape)


