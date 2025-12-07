import os
import subprocess
import datetime
import platform

IS_WINDOWS = platform.system() == 'Windows'

# === Fichier de log ===
log_file = os.path.join(os.getcwd(), "log.txt")

def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def setup_postgres_env(host, port, user, password, database, pg_bin_path=None):
    """
    Configure les variables d’environnement PostgreSQL et le PATH.
    """
    if IS_WINDOWS and pg_bin_path:
        os.environ['PATH'] += f';{pg_bin_path}'

    os.environ['PGHOST'] = host
    os.environ['PGPORT'] = port
    os.environ['PGUSER'] = user
    os.environ['PGPASSWORD'] = password
    os.environ['PGDATABASE'] = database

def check_postgres_connection():
    """
    Vérifie la connexion PostgreSQL avec psql.
    """
    try:
        result = subprocess.run(["psql", "-c", "SELECT 1;"], capture_output=True, text=True)
        if result.returncode != 0:
            log("[ERROR] Connexion à PostgreSQL échouée.")
            log(result.stderr)
            return False
        log("[OK] Connexion PostgreSQL réussie.")
        return True
    except Exception as e:
        log(f"[EXCEPTION] {e}")
        return False

def find_shapefiles(directory):
    """
    Retourne la liste des fichiers .shp dans un répertoire donné (récursivement).
    """
    shapefiles = []
    for source, dirs, files in os.walk(directory):
        for file_ in files:
            if file_.lower().endswith('.shp'):
                shapefiles.append(os.path.join(source, file_))
    return shapefiles

def import_shapefiles(shapefile_list):
    """
    Importe chaque shapefile dans une table PostgreSQL (nommée d'après le fichier).
    """
    for shape_path in shapefile_list:
        table_name = os.path.splitext(os.path.basename(shape_path))[0].lower()
        cmd = f'shp2pgsql -I "{shape_path}" {table_name} | psql'
        log(f"[INFO] Importation de '{shape_path}' vers la table '{table_name}'...")
        result = subprocess.call(cmd, shell=True)
        if result == 0:
            log(f"[OK] Table '{table_name}' importée avec succès.")
        else:
            log(f"[ERROR] Échec de l'import de '{shape_path}'.")

def run_import(base_dir):
    """
    Fonction principale à appeler depuis un script externe.
    """
    log("=== Début de l'import des shapefiles ===")
    if check_postgres_connection():
        shapefiles = find_shapefiles(base_dir)
        if shapefiles:
            import_shapefiles(shapefiles)
        else:
            log("[INFO] Aucun fichier .shp trouvé.")
    else:
        log("[FATAL] Import annulé : connexion PostgreSQL impossible.")
    log("=== Fin du traitement ===\n")
