### 📌 Initial Attempt: Python Virtual Environment on Windows PowerShell

At first, we attempted to set up a Python virtual environment directly in Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

However, this ran into **PowerShell Execution Policy Restrictions**:

```
venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

To temporarily bypass this restriction, we ran:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

After activating the virtual environment, we attempted to install Airflow with:

```powershell
pip install apache-airflow
```

This caused a critical issue:

```
Fatal error in launcher: Unable to create process using ...
```

This was caused by an invalid or broken virtual environment path, likely due to moving or renaming folders in the Windows file system after the venv was created. Python hardcodes the paths when creating the venv, so the move broke it.

---

### ⚠️ Realization: Airflow on Windows is Not Officially Supported

Upon further inspection, we found this warning in the logs:

```
Airflow currently can be run on POSIX-compliant Operating Systems...
On Windows you can run it via WSL2 (Windows Subsystem for Linux 2)...
```

Running Airflow directly on Windows is not officially supported and may result in bugs like:

* `os.register_at_fork` not existing on Windows
* Dependency issues
* Broken scheduler/worker behavior

---

### ✅ Switch to WSL (Windows Subsystem for Linux)

We decided to use **Ubuntu via WSL2** to run Airflow in a supported environment.

Steps:

1. **Open Ubuntu** (via Start Menu or typing `wsl` in PowerShell).

2. Created a new project directory:

   ```bash
   mkdir airflow_project
   cd airflow_project
   ```

3. Tried to create the venv:

   ```bash
   python3 -m venv venv
   ```

   ⚠️ Failed with error:

   ```
   The virtual environment was not created successfully because ensurepip is not available.
   ```

4. Fixed by installing the missing system package:

   ```bash
   sudo apt update
   sudo apt install python3.10-venv
   ```

5. Successfully recreated the environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

---

### 🐍 Final Working Setup (on Ubuntu/WSL)

From within the `venv`, we installed Apache Airflow (with pinned dependencies to avoid compatibility issues):

```bash
pip install "apache-airflow==2.8.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.0/constraints-3.10.txt"
```

Now we are able to:

* Write DAGs
* Use Airflow CLI
* Avoid OS-related bugs

---

### 🧪 What We Learned

* Windows is not suitable for Airflow development (use WSL or containers).
* Avoid renaming or moving Python venv folders after creation.
* Always check official support documentation early.
* Errors during environment setup are normal—log them for future reference.


# 🧠 Terminal Cheat Sheet - Proyecto Airflow con WSL

## Pasos para iniciar el entorno de desarrollo

# Resumem
## 1. Abrir Ubuntu (WSL)
### Desde el menú de inicio (buscar "Ubuntu") o correr:
#### wsl

# 2. Navegar al directorio del proyecto (ajustar si es necesario)
## cd ~/airflow_project

# 3. Activar el entorno virtual
## source venv/bin/activate

# 4. Ejecutar tus scripts de Airflow (o cualquier otro script)
## Ejemplo:
### python dags/mi_script_airflow.py


## 🖥️ Uso de Visual Studio Code con WSL y entorno virtual

### 1. Instalar la extensión de WSL en VS Code
Para poder trabajar cómodamente desde Visual Studio Code con WSL (Windows Subsystem for Linux):

- Abrir Visual Studio Code.
- Ir a la pestaña de extensiones (`Ctrl + Shift + X`).
- Buscar **"Remote - WSL"** y hacer clic en instalar.

### 2. Abrir el proyecto desde WSL
Desde la terminal de Ubuntu (WSL), navegar al directorio del proyecto:

cd ~/airflow_project

Y luego ejecutar:

bash
code .

Esto abrirá Visual Studio Code directamente conectado al entorno de Ubuntu.

3. Usar la terminal integrada en VS Code
Dentro de Visual Studio Code, abrir la terminal integrada con Ctrl + ñ o desde el menú Terminal > New Terminal.
Asegurarse de que esté en modo WSL y ejecutar:

bash
source venv/bin/activate
Una vez activado el entorno virtual, se pueden ejecutar los scripts normalmente:

bash
python tu_script.py