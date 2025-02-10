# 🚀 Instalación de Odoo con Docker y Docker Compose

Este documento describe los pasos necesarios para instalar y configurar **Odoo 18** utilizando **Docker y Docker Compose**.

---

## **📌 1. Instalación de Docker y Docker Compose**

### **🔹 Actualizar paquetes**
```bash
sudo apt update
```

### **🔹 Instalar Docker**
```bash
sudo apt install -y docker.io
```

### **🔹 Iniciar y habilitar Docker**
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### **🔹 Verificar la instalación de Docker**
```bash
docker --version
```

### **🔹 Instalar Docker Compose**
```bash
sudo apt install -y docker-compose
```

### **🔹 Verificar la instalación de Docker Compose**
```bash
docker-compose --version
```

---

## **📌 2. Crear directorios para Odoo**

Ejecuta los siguientes comandos para organizar los archivos de Odoo:

```bash
mkdir evali1-docker
mkdir odoo-18-docker
mkdir odoo-18-dev
```

Luego, accede a los directorios según corresponda:

```bash
cd evali1-docker
cd odoo-18-docker
cd odoo-18-dev
```

---

## **📌 3. Configurar Docker Compose**
Copia los archivos necesarios:
- **`docker-compose.yml`** → Archivo principal de configuración.
- **Carpetas `addons/` y `config/`** → Contienen módulos y configuración personalizada.

---

## **📌 4. Levantar los servicios con Docker Compose**

Ejecuta uno de los siguientes comandos según tu archivo de configuración:

### **🔹 Para iniciar los contenedores**
```bash
docker-compose up -d
```

Si usas archivos de configuración alternativos:

```bash
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose2.yml up -d
```

### **🔹 Para reiniciar Odoo**
```bash
docker-compose -f docker-compose.yml restart odoo
docker-compose -f docker-compose2.yml restart odoo
```

---

## **📌 5. Eliminar contenedores y limpiar Docker**
Si necesitas **borrar todo** y limpiar el sistema, ejecuta:

```bash
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker system prune -a --volumes
sudo systemctl restart docker
docker image prune -a
```

⚠ **⚠ ADVERTENCIA:**  
🚨 **Estos comandos eliminarán TODOS los contenedores, imágenes y volúmenes de Docker.** Asegúrate de respaldar antes de ejecutarlos.

---

## **📌 6. Crear la base de datos en Odoo**

Si es un entorno nuevo, asegúrate de crear la base de datos desde la interfaz de Odoo en tu navegador:

🔗 **Accede a Odoo:**
👉 `http://localhost:8069`

Si estás en un servidor remoto:
👉 `http://IP_DEL_SERVIDOR:8069`

---

