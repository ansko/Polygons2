from Classes.Options import Options

from functions.utils import delta


class PropertiesPrinter():
    def __init__(self, disks):
        o = Options()
        E_f = o.getProperty('E_f')
        nu_f = o.getProperty('nu_f')
        E_m = o.getProperty('E_m')
        nu_m = o.getProperty('nu_m')
        E_sh = o.getProperty('E_sh')
        nu_sh = o.getProperty('nu_sh')  
        f = open('materials.txt', 'w')
        C = [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]],		
              [[0, 0, 0], [0, 0, 0], [0, 0, 0]],		
              [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],		
             [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],		
              [[0, 0, 0], [0, 0, 0], [0, 0, 0]],		
              [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],		
             [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],		
              [[0, 0, 0], [0, 0, 0], [0, 0, 0]],		
              [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]]		
        #for particle in range(len(disks)):	
        if len(disks) > 0:
            la = E_f * nu_f / (1.0 - 2 * nu_f) / (1 + nu_f)		
            mu = E_f / 2 / (1 + nu_f)	
            for i in range(3):		
                for j in range(3):		
                    for k in range(3):		
                        for l in range(3):		
                            C[i][j][k][l] = la * delta(i, j) * delta(k, l) 
                            C[i][j][k][l] += mu * delta(i, k) * delta(j, l)
                            C[i][j][k][l] += mu * delta(i, l) * delta(j, k)
                            f.write(str(C[i][j][k][l]) + ' ')
            f.write('\n')
        #for particle in range(len(disks)):
        if len(disks) > 0:
            la = E_sh * nu_sh / (1.0 - 2 * nu_sh) / (1 + nu_sh)	
            mu = E_sh / 2 / (1 + nu_sh)
            for i in range(3):		
                for j in range(3):		
                    for k in range(3):		
                        for l in range(3):		
                            C[i][j][k][l] = la * delta(i, j) * delta(k, l)
                            C[i][j][k][l] += mu * delta(i, k) * delta(j, l)
                            C[i][j][k][l] += mu * delta(i, l) * delta(j, k)
                            f.write(str(C[i][j][k][l]) + ' ')
            f.write('\n')
        la = E_m * nu_m / (1.0 - 2 * nu_m) / (1 + nu_m)		
        mu = E_m / 2 / (1 + nu_m)		
        for i in range(3):		
            for j in range(3):		
                for k in range(3):		
                    for l in range(3):		
                        C[i][j][k][l] = la * delta(i, j) * delta(k, l)
                        C[i][j][k][l] += mu * delta(i, k) * delta(j, l) 
                        C[i][j][k][l] += mu * delta(i, l) * delta(j, k)
                        f.write(str(C[i][j][k][l]) + ' ')
