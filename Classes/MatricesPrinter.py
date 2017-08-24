class MatricesPrinter():
    def __init__(self, disks):
        f = open('matrices.txt', 'w')		
        for i in range(len(disks) + 1):		
            f.write('1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0\n')