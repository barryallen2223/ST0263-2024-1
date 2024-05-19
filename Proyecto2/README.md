# Proyecto 2

## Pasos iniciales

Primero crear 5 VM en GCP, para ello es importante cambiar la configuración de los boot disks, donde el OS será Ubuntu en la versión que coloque por defecto con 20gb de espacio para cada VM.
La definición de las VM es la siguiente:
- MySQL
- NFS
- VM1-master
- VM2-follower
- VM3-follower

## Setup de las VM
Dentro de las VM1, VM2 y VM3, instalar microk8s, para ello, ejecutar los siguientes comandos:

```
microk8s sudo snap install microk8s --classic

sudo usermod -a -G microk8s $USER
mkdir -p ~/.kube
chmod 0700 ~/.kube

newgrp microk8s # Para reiniciar los permisos 

alias kubectl='microk8s kubectl' # Crear un alias por comodidad
```
## Clustering
La idea es configurar todo dentro del master, ya que los cambios se replicarán dentro de las otras VM, pero primero se necesita crear una relación dentro de las VMs, para ello, ejecutar 
```microk8s add-node```, este comando generará un comando así ```microk8s join <IP>:<PORT>```, el cual se ejecutará dentro de cada VM que se desee agregar al master. Una vez hecho esto, dentro del master, podremos ver que todos los cambios se hayan aplicado efectivamente, para esto ```kubectl get no```. Cuando se haya confirmado que todo está bien, vamos a agregar los add-ons con los que se hará el resto de la configuración ```microk8s enable dns dashboard ingress storage```.

## MySQL config
Dentro de la VM, establecer una conexión SSH y ejecutar los siguientes comandos,
```
sudo apt update
sudo apt install mysql-server

sudo mysql_secure_installation

sudo mysql -u root -p # Pedirá por la contraseña, pero al no configurar una, con un enter podremos entrar a mysql
CREATE DATABASE wordpress;
CREATE USER 'wpuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'%';
FLUSH PRIVILEGES;
EXIT;
```
Ahora, configuraremos mysql para que esté escuchando no desde la dirección ip por defecto (127.0.0.1), sino en 0.0.0.0, para ello, cambiaremos una configuración dentro del archivo ```sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf``` y en la parte del archivo donde dice "bind-address", colocar la IP 0.0.0.0. Una vez hecho esto, podemos hacer ```sudo systemctl restart mysql``` para reiniciar y aplicar cambios.

## NFS config
Dentro de la VM, establecer una conexión SSH y ejecutar los siguientes comandos,
```
sudo apt update
sudo apt install nfs-kernel-server

sudo mkdir -p /srv/nfs/wordpress
sudo chown nobody:nogroup /srv/nfs/wordpress
```
Ahora, agregaremos al archivo exports, la carpeta que se va a compartir para las VMs, para ello modificaremos con el comando ```sudo nano /etc/exports``` y agregar al final del archivo "/srv/nfs/wordpress  *(rw,sync,no_subtree_check,no_root_squash)". Por último, aplicar los cambios con los comandos, 
```
sudo exportfs -a
sudo systemctl restart nfs-kernel-server
```

## Deployments
```
kubectl apply -f pv-pvc.yaml # Modificar la IP del NFS a la correspondiente
kubectl apply -f mysql-deployment.yaml
kubectl apply -f wordpress-deployment.yaml
```

## Autoscaling
```
microk8s enable metrics-server
kubectl apply -f hpa.yaml
kubectl get hpa
```

## Ingress
```
kubectl apply -f ingress.yaml # Cambiar el DNS por el correspondiente
kubectl get ingress
```
Modificar el archivo hosts, con el comando ```sudo nano /etc/hosts```, bajo la línea de "127.0.0.1 localhost", agregar "EXTERNAL-IP DNS".

Por último, entrar al DNS configurado y terminar con la creación del usuario y el sample website para poder visualizar la aplicación wordpress autoescalable.
