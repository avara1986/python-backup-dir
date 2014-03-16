#!/usr/bin/env python

# Backup files - As published in Python Cookbook
import sys, os, shutil, filecmp
import time, csv
#folder_in = "/mnt/samba/WWW_WEBS/PRUEBAS/"
folder_in = "/var/www/test-django2/"
folder_dest = "/root/Desktop/backup1/"

script_folder = os.path.dirname(os.path.realpath(__file__))
log_file = script_folder+'/my_backup_result.csv'

# Verificar si existen los ficheros y directorios
if not os.path.exists(script_folder):
    sys.exit("NO EXISTE EL DIRECTORIO DE ORIGEN "+script_folder)
if not os.path.exists(folder_dest):
    sys.exit("NO EXISTE EL DIRECTORIO DE DESTINO "+folder_dest)
if not os.path.isfile(log_file):
    sys.exit("NO EXISTE EL FICHERO DE LOG "+log_file)

# Abrir el fichero de log
ofile  = open(log_file, "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
row = ['FECHA', 
       'ACCION', 
       'ORIGEN', 
       'DESTINO'
       ]
writer.writerow(row)
# Limite de copias
max_copies = 0

# Recorrer el directorio a buscar
i = 0
for dir, subdirs, files in os.walk(folder_in):
    if i >= max_copies and max_copies != 0:
        break
    print "DIR" + str(dir)
    print "SUBDIR" + str(subdirs)
    for f in files:
        if os.path.isfile(dir + '/' + f):
            action = ''
            dir_dest = dir.replace(folder_in, folder_dest)
            print "["+time.strftime("%d/%m/%Y %H:%M:%S")+"] -- FILES " + dir + '/' + f
            print "["+time.strftime("%d/%m/%Y %H:%M:%S")+"] -- FILES DEST: " + dir_dest + '/' + f
            # Verificar si existe el directorio
            if not os.path.exists(dir_dest):
                os.makedirs(dir_dest)
                print "["+time.strftime("%d/%m/%Y %H:%M:%S")+"] - NEW DIRECTORY " + dir_dest
            # Verificar si existe el fichero
            if not os.path.isfile(dir_dest + '/' + f):
                action = 'COPY'
            else:
                last_update_in = os.path.getmtime(dir + '/' + f)
                #print time.ctime(last_update_in)
                #print last_update_in
                last_update_dest = os.path.getmtime(dir_dest + '/' + f)
                #print time.ctime(last_update_dest)
                print last_update_dest
                if int(last_update_dest) < int(last_update_in):
                    action = 'UPDATE'
                else:
                    action = 'NONE'
            print "["+time.strftime("%d/%m/%Y %H:%M:%S")+"] ---- "+action
            #COPIAR FICHEROS
            if action != 'NONE':
                shutil.copy2(dir + '/' + f, dir_dest + '/' + f)
                row = [time.strftime("%d/%m/%Y %H:%M:%S"), 
                       action, 
                       dir + '' + f, 
                       dir_dest + '' + f
                       ]
                writer.writerow(row)
                i +=1
        else:
            print "--###### NO EXISTE EL FICHERO "+dir + '/' + f
print str(i) + " FICHEROS COPIADOS"
ofile.close()