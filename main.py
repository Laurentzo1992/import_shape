import shapefile_importer as sfi

# === Remote Configuration PostgreSQL ===
sfi.setup_postgres_env(
    host='188.165.58.60',
    port='5434',
    user='aen',
    password='Aen@68860-',
    database='aen',
    pg_bin_path=r"C:\Program Files (x86)\PostgreSQL\8.4\bin"  # facultatif, pour Windows uniquement
)

# === local Configuration PostgreSQL ===
# sfi.setup_postgres_env(
    # host='localhost',
    # port='5432',
    # user='postgres',
    # password='admin',
    # database='aen_bd',
    # pg_bin_path=r"C:\Program Files (x86)\PostgreSQL\8.4\bin"  # facultatif, pour Windows uniquement
# )

# === Répertoire des shapefiles à importer ===
#base_dir = r"C:\Users\HP\Desktop\Projets\import_shape\data_bassin"
base_dir = r"C:\Users\HP\Desktop\Projets\import_shape\bfa_adm_igb_20200323_shp"
# === Lancer l'importation ===
sfi.run_import(base_dir)

