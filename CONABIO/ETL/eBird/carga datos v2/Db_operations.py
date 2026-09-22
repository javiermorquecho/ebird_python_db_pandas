import mysql.connector
from mysql.connector import Error
#import pymysql
from Manager import Manager
import re
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class Db_operations:
  # Tipos de dato conocidos para las columnas estandar del CSV de eBird.
  # Las llaves deben ir en MAYUSCULAS: la comparacion se hace normalizando
  # el encabezado del archivo a mayusculas antes de buscarlo aqui.
  # Cualquier columna que NO aparezca en este diccionario usara VARCHAR(255)
  # por defecto (ver _dibujar_filas_columna).
  db_columns = {
    "AGE/SEX": "TEXT",
    "LATITUDE": "DOUBLE",
    "LONGITUDE": "DOUBLE",
    "OBSERVATION_DATE": "DATETIME",
    "OBSERVER_ORCID_ID": "TEXT",
    "ALL_SPECIES_REPORTED": "INT",
    "HAS_MEDIA": "INT",
    "APPROVED": "INT",
    "REVIEWED": "INT",
    "CHECKLIST_COMMENTS": "LONGTEXT",
    "SPECIES_COMMENTS": "LONGTEXT",
  }

  db_connections = {
    81:{
      "host": "172.16.1.81",
      "user": "si_momja",
      "password": "s1_m0mj4",
      "db": "ebird",
      "port": "3306",
      "allow_local_infile":True,
      "charset":"utf8mb4",
      "read_timeout":None,
      "write_timeout":None,
      "connect_timeout":15,
    },
    248:{
      "host": "172.16.1.248",
      "user": "si_momja",
      "password": "s1_m0mj4",
      "db": "ebird_test",
      "port": "3306",
      "allow_local_infile":True,
      "charset":"utf8mb4",
      "read_timeout":None,
      "write_timeout":None,
      "connect_timeout":15,
    },
  }

  table_prefix = "ebird_"
  Resolver = Manager
  drop_table_if_exist = False
  sql_drop_table = "DROP TABLE IF EXISTS %s"
  default_db_connection = 248

  def __init__(self, name):
    print("Class Db...loaded")

  def query(self, query, db=None, show_results=False, connection_for_loading = False):
    records = []
    #print("Query")
    if db is None:
      db = self.db_connections[self.default_db_connection]
    else:
      db = self.db_connections[db]
    #print(db)
    try:
      connection = self.connect(self, db, connection_for_loading)
      if connection.is_connected():
        #db_info = connection.get_server_info()
        #print(f"✅ Success! Connected to MySQL Server version: {db_info}")
        # 2. Test a basic query (Optional)
        cursor = connection.cursor()
        records = self.connection_query(self, cursor, query, show_results)
    except Error as e:
      print(f"❌ MySQL error: {e}")
    finally:
      # 3. Always close the connection when finished
      if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        #print("MySQL connection is closed.")
    return records

  def connect(self, db, connection_for_loading = False):
    if connection_for_loading == True:
      connection = mysql.connector.connect(**db)
    else:
      connection = mysql.connector.connect(
        host=db["host"],  # Change to your server IP if remote
        user=db["user"],  # Your MySQL username
        password=db["password"],  # Your MySQL password
        database=db["db"]  # The schema you want to connect to
      )

    return connection

  def connection_query(self, cursor, query, show_results=False):
    records = []
    try:
      cursor.execute(query)
      #cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
      print("❌ Error: {}".format(err))
      Manager.stop()
    records = cursor.fetchall()
    if show_results == True:
      print(f"Query: {query}")
      print(f"Result: {records}")
    return records

  def generate_table_sql(self, txt_fields, table_name):
    fields_typed = []
    columns = ""
    sql = ""
    for txt_field in txt_fields:
      sanitized_field = self.sanitizar_nombre_columna(self, txt_field)
      fields_typed.append({
        "field":sanitized_field,
        "type":self.db_columns.get( sanitized_field, "VARCHAR(255)" ),
      })
    columns = [
      f"`{f['field']}` {f['type']}"
      for f in fields_typed
    ]
    sql = f"CREATE TABLE `{self.table_prefix+table_name}` ({', '.join(columns)}) ENGINE=InnoDB"
    self.Resolver.showMessage(self.Resolver, "check_table_sql", sql)
    return sql

  def sanitizar_nombre_columna(self, nombre: str) -> str:
    """Convierte el encabezado del CSV en un nombre de columna SQL valido."""
    nombre = nombre.strip().strip('"').strip("'")
    nombre = re.sub(r"[^0-9a-zA-Z_]", "_", nombre)
    if not nombre:
        nombre = "columna"
    if nombre[0].isdigit():
        nombre = "c_" + nombre
    return nombre

  def create_table(self, table_name, sql_table, drop_table_if_exist=False):
    sql = ""
    table_name = self.table_prefix+table_name
    if drop_table_if_exist is None:
      drop_table_if_exist = self.drop_table_if_exist
    if drop_table_if_exist == True:
      sql = self.sql_drop_table % table_name
      self.query(self, sql, None, True)
      self.Resolver.showMessage(self.Resolver, "table_deleted", table_name)
    sql = sql_table
    self.query(self, sql, None, True)
    self.Resolver.showMessage(self.Resolver, "table_created", table_name)
    return

# query(self, query, db=None, show_results=False, connection_for_loading = False)
  #def load_csv_data(self, df, table_name, separator, db=None):
  def load_csv_data(self, csv_path, table_name, separator, db=None):
    table_name = self.table_prefix+table_name
    if db is None:
      db = self.db_connections[self.default_db_connection]
    else:
      db = self.db_connections[db]
    try:
      connection = self.connect(self, db, True)
      db_info = connection.get_server_info()
      print(f"✅ Success! Connected to MySQL Server version: {db_info}")
      self.Resolver.showMessage(self.Resolver, "wait", table_name)
      if connection.is_connected():
        cursor = connection.cursor()
        self.set_checks(self, cursor, 0)  # Disable checks
        # Load data
        sql = (
          f"LOAD DATA LOCAL INFILE '{csv_path}' "
          f"INTO TABLE `{table_name}` "
          f"FIELDS TERMINATED BY '\\t' "
          f"LINES TERMINATED BY '\\n' "
          f"IGNORE 1 LINES;"
        )
        #print(f"Query: {sql}")
        records = self.connection_query(self, cursor, sql, True)
        self.commit(self, cursor)  # Commit
        self.show_warnings(self, cursor)  # Warnings
        self.set_checks(self, cursor)  # Enable checks
    except Error as e:
      print(f"❌ MySQL error: {e}")
    finally:
      if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        self.Resolver.showMessage(self.Resolver, "csv_loaded", table_name)
    return


  def load_df(self, df, table_name, db=None):
    table_name = self.table_prefix+table_name
    if db is None:
      db = self.db_connections[self.default_db_connection]
    else:
      db = self.db_connections[db]
      
    engine = create_engine(f"mysql+mysqlconnector://{db["user"]}:{db["password"]}@{db["host"]}:{db["port"]}/{db["db"]}?charset=utf8mb4")
    #df.to_sql(name=table_name, con=engine, if_exists="append", index=False, chunksize=5000,method='multi')
    successful_rows = 0
    failed_rows_list = []
    chunk_size = 5
    
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        
        try:
            # Try importing the whole chunk at once
            chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            successful_rows += len(chunk)
            
        except SQLAlchemyError as batch_error:
            # A row in this chunk caused an error! Fall back to row-by-row processing for this chunk.
            for _, row in chunk.iterrows():
                # Convert row to a single-row DataFrame
                single_row_df = pd.DataFrame([row])
                
                try:
                    single_row_df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
                    successful_rows += 1
                except SQLAlchemyError as row_error:
                    # Capture the exact data row and the exact database error message
                    error_record = row.to_dict()
                    
                    # Extract the cleanest possible error message string
                    error_record['DB_ERROR_MESSAGE'] = str(row_error.__dict__.get('orig', row_error))
                    
                    failed_rows_list.append(error_record)
    
    # 4. Summary & Report Generation
    print("\n=== IMPORT SUMMARY ===")
    print(f"Total Rows Processed: {len(df)}")
    print(f"Successfully Inserted: {successful_rows}")
    print(f"Failed Rows: {len(failed_rows_list)}")
    
    if failed_rows_list:
        # Convert errors to a DataFrame
        error_report_df = pd.DataFrame(failed_rows_list)
        
        # Save the report to a CSV file
        report_filename = "mysql_import_error_report.csv"
        error_report_df.to_csv(report_filename, index=False)
        
        print(f"\n⚠️ CRITICAL: {len(failed_rows_list)} rows failed. Report saved to: '{report_filename}'")
        
        # Preview the first few errors right in Jupyter Notebook
        display(error_report_df[['DB_ERROR_MESSAGE'] + list(df.columns)].head())
    else:
        print("\n🎉 Success! All rows inserted without any errors.")
    
    print("Data loaded successfully!")
    return


  def set_checks(self, cursor, status=1):
    sql = f"SET SESSION unique_checks = {status}"
    #print(f"Query: {sql}")
    records = self.connection_query(self, cursor, sql, True)

    # Disable check and verifications
    sql = f"SET SESSION foreign_key_checks = {status}"
    #print(f"Query: {sql}")
    records = self.connection_query(self, cursor, sql, True)
    
    return

  def show_warnings(self, cursor):
    # Warnings
    sql = "SELECT @@warning_count"
    #print(f"Query: {sql}")
    records = self.connection_query(self, cursor, sql, True)

    # Warnings
    sql = "SHOW WARNINGS;"
    #print(f"Query: {sql}")
    records = self.connection_query(self, cursor, sql, True)
    
    return

  def commit(self, cursor=None):
    sql = "COMMIT;"
    if cursor is not None:
      records = self.connection_query(self, cursor, sql, True)
    else:
      self.query(self, sql, None, False)

    return

  def create_indx_cols(self, table_name):
    table_name = self.table_prefix+table_name
    sql = f"""ALTER TABLE {table_name} ADD COLUMN (Id INT),
	ADD COLUMN (val_sp INT DEFAULT 1),
    ADD COLUMN (MRD INT DEFAULT 1),
    ADD COLUMN (id_coord INT DEFAULT NULL),
    ADD COLUMN (ID_FAM INT DEFAULT NULL),
    ADD COLUMN (gui_snib INT DEFAULT 1);"""
    self.query(self, sql, None, True)
    self.Resolver.showMessage(self.Resolver, "col_index_created", table_name)
    return

  def set_id_values(self, table_name):
    table_name = self.table_prefix+table_name
    sql = f"""SET @rownum:= 0;
    UPDATE {table_name} SET Id = (SELECT @rownum:= @rownum + 1);"""
    self.query(self, sql, None, True)
    self.commit(self)
    self.Resolver.showMessage(self.Resolver, "col_id_add_numbers", table_name)
    return

  def add_indx_2_cols(self, table_name):
    table_name = self.table_prefix+table_name
    sql = f"""ALTER TABLE {table_name} ADD INDEX (Id),
    ADD INDEX (LATITUDE),
    ADD INDEX (LONGITUDE),
    ADD INDEX (SCIENTIFIC_NAME),
    ADD INDEX (CATEGORY),
    ADD INDEX (id_coord);"""
    self.query(self, sql, None, True)
    self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def drop_dep_table(self, table_name):
    sql = f'DROP TABLE IF EXISTS dep_{table_name};'
    self.query(self, sql, None, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def create_dep_table(self, table_name):
    sql = f'''CREATE TABLE dep_{table_name}(
	`Id` int(11) NOT NULL AUTO_INCREMENT,
	`GLOBAL_UNIQUE_IDENTIFIER` varchar(255) NOT NULL,
	`SEI_NUM` int(11) DEFAULT NULL,
	`GI_NUM` int(11) DEFAULT NULL,
    `APPROVED` int(11) DEFAULT NULL,
	`MRD` int(11) DEFAULT NULL,
    `gui_snib` int(11) DEFAULT NULL,
	PRIMARY KEY (`Id`)
	) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;'''
    self.query(self, sql, None, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def add_dep_seinum_index(self, table_name):
    sql = f'ALTER TABLE dep_{table_name} ADD INDEX (SEI_NUM);'
    self.query(self, sql, None, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def populate_dep_table(self, table_name):
    sql = f'''INSERT INTO dep_{table_name}(Id, GLOBAL_UNIQUE_IDENTIFIER, SEI_NUM, GI_NUM, APPROVED, MRD, gui_snib)
	(SELECT Id, GLOBAL_UNIQUE_IDENTIFIER,
	REPLACE(`SAMPLING_EVENT_IDENTIFIER`,'S','') AS SAMPLING_EVENT_IDENTIFIER,
	IF(REPLACE(GROUP_IDENTIFIER,'G','') = '', NULL, REPLACE(GROUP_IDENTIFIER,'G','')) AS GROUP_IDENTIFIER, APPROVED, MRD, gui_snib
	FROM ebird_{table_name});'''
    self.query(self, sql, None, True)
    self.commit(self)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def set_gi_num(self, table_name):
    sql = f'UPDATE dep_{table_name} SET GI_NUM = 99 WHERE GI_NUM IS NULL OR GI_NUM = 0;'
    self.query(self, sql, None, True)
    self.commit(self)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def set_dep_mrd(self, table_name):
    sql = f'UPDATE dep_{table_name} SET MRD = 0 WHERE APPROVED = 0;'
    self.query(self, sql, None, True)
    self.commit(self)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def set_dep_mrd_2(self, table_name):
    sql = f'UPDATE dep_{table_name} SET MRD = 3 WHERE GI_NUM != 99 AND APPROVED != 0;'
    self.query(self, sql, None, True)
    self.commit(self)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def drop_paso_table(self, cursor):
    sql = f'DROP TEMPORARY TABLE IF EXISTS Paso;'
    records = self.connection_query(self, cursor, sql, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def create_paso_table(self, cursor, table_name):
    sql = f'''CREATE TEMPORARY TABLE Paso (SELECT GI_NUM, MIN(SEI_NUM) AS SEI_NUM 
    FROM dep_{table_name} GROUP BY GI_NUM ORDER BY GI_NUM, SEI_NUM ASC);'''
    records = self.connection_query(self, cursor, sql, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def add_paso_seinum_index(self, cursor):
    sql = f'ALTER TABLE Paso ADD INDEX(SEI_NUM);'
    records = self.connection_query(self, cursor, sql, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def set_paso_mrd(self, cursor, table_name):
    sql = f'UPDATE dep_{table_name} d, Paso p SET MRD = 2 WHERE d.SEI_NUM = p.SEI_NUM AND APPROVED != 0;'
    records = self.connection_query(self, cursor, sql, True)
    self.commit(self, cursor)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def set_paso_mrd_2(self, cursor, table_name):
    sql = f'UPDATE ebird_{table_name} t, dep_{table_name} d SET t.MRD = d.MRD WHERE t.id = d.id;'
    records = self.connection_query(self, cursor, sql, True)
    self.commit(self, cursor)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def paso_last_rows(self, cursor):
    sql = f'SELECT * FROM dep_26sep LIMIT 10;'
    records = self.connection_query(self, cursor, sql, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def tmp_paso(self, table_name, db=None):
    if db is None:
      db = self.db_connections[self.default_db_connection]
    else:
      db = self.db_connections[db]
    try:
      connection = self.connect(self, db, True)
      db_info = connection.get_server_info()
      print(f"✅ Success! Connected to MySQL Server version: {db_info}")
      if connection.is_connected():
        cursor = connection.cursor()
        self.drop_paso_table(self,cursor)
        self.create_paso_table(self,cursor, table_name)
        self.add_paso_seinum_index(self,cursor)
        self.set_paso_mrd(self,cursor, table_name)
        self.set_paso_mrd_2(self,cursor, table_name)
        self.Resolver.showMessage(self.Resolver, "show_afew_paso_rows", table_name)
        self.paso_last_rows(self,cursor)
    except Error as e:
      print(f"❌ MySQL error: {e}")
    finally:
      if 'connection' in locals() and connection.is_connected():
        cursor.close()
        #connection.close()
        self.Resolver.showMessage(self.Resolver, "paso_loaded", table_name)
    return connection

  def taxo_cle_avmx_add_index(self):
    sql = f'ALTER TABLE taxones_clements_avesmx ADD INDEX (SCIENTIFIC_NAME), ADD INDEX (CATEGORY);'
    self.query(self, sql, None, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def update_taxo_cavmx(self,table_name):
    sql = f'UPDATE ebird_{table_name} e INNER JOIN taxones_clements_avesmx d ON e.SCIENTIFIC_NAME = d.SCIENTIFIC_NAME AND e.CATEGORY = d.CATEGORY SET e.val_sp = d.val_sp, e.ID_FAM = d.ID_FAM;'
    self.query(self, sql, None, False)
    self.commit(self)
    self.Resolver.showMessage(self.Resolver, "wait", table_name)
    return

  def add_gui_snib(self):
    sql = 'DROP TABLE IF EXISTS gui_snib;'
    self.query(self, sql, None, False)
    sql = f"CREATE TABLE gui_snib ENGINE=InnoDB SELECT idejemplaroriginal as gui_snib, REPLACE (idejemplaroriginal, 'URN:CornellLabOfOrnithology:EBIRD:OBS','') as LLAVE FROM snib.ejemplar_curatorial e INNER JOIN snib.proyecto p USING(llaveproyecto) WHERE p.proyecto = 'averAves' AND e.estadoregistro = '';"
    self.query(self, sql, None, False)
    self.Resolver.showMessage(self.Resolver, "wait", table_name)
    return

  def llave_operations(self,table_name):
    sql = f'ALTER TABLE ebird_{table_name} ADD COLUMN (LLAVE bigint);'
    self.query(self, sql, None, False)
    sql = f"UPDATE ebird_{table_name} SET LLAVE = REPLACE (GLOBAL_UNIQUE_IDENTIFIER, 'URN:CornellLabOfOrnithology:EBIRD:OBS','');"
    self.query(self, sql, None, False)
    self.commit(self)
    sql = f'ALTER TABLE ebird_{table_name} ADD INDEX (LLAVE);'
    self.query(self, sql, None, False)
    sql = 'ALTER TABLE gui_snib ADD INDEX (LLAVE);'
    self.query(self, sql, None, False)
    sql = f'UPDATE gui_snib s, ebird_{table_name} d SET d.gui_snib = 2 ""WHERE s.LLAVE = d.LLAVE;'
    self.query(self, sql, None, False)
    self.commit(self)
    return

  def add_snib_version(self,table_name):
    sql = f'DROP TABLE IF EXISTS SNIB_{table_name};'
    self.query(self, sql, None, False)
    sql = f'CREATE TABLE SNIB_{table_name} ENGINE=InnoDB (SELECT * FROM ebird_{table_name} WHERE Approved = 1 AND gui_snib = 1 AND MRD < 3 AND val_sp < 5);'
    self.query(self, sql, None, False)
    return

  def add_coord(self,table_name):
    sql = f'DROP TABLE IF EXISTS coord_{table_name}";'
    self.query(self, sql, None, False)
    sql = f'''CREATE TABLE coord_{table_name} (`Id_coord` int(11) NOT NULL AUTO_INCREMENT, 
    `LATITUDE` double DEFAULT NULL,
	`LONGITUDE` double DEFAULT NULL,
	PRIMARY KEY (`Id_coord`)
    ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;'''
    self.query(self, sql, None, False)
    return

  def insert_coord(self,table_name):
    sql = f'INSERT INTO coord_{table_name} (LATITUDE, LONGITUDE) (SELECT DISTINCT LATITUDE, LONGITUDE FROM ebird_{table_name} ORDER BY LATITUDE desc, LONGITUDE asc);'
    self.query(self, sql, None, False)
    self.commit(self)
    sql = f'''UPDATE ebird_{table_name} t, coord_{table_name} c SET t.id_coord = c.Id_coord 
	WHERE t.LATITUDE = c.LATITUDE 
	AND t.LONGITUDE = c.LONGITUDE;'''
    self.query(self, sql, None, False)
    self.commit(self)
    return

  def tmp_coor_paso(self, connection, table_name):
    try:
      connection = self.connect(self, db, True)
      db_info = connection.get_server_info()
      print(f"✅ Success! Connected to MySQL Server version: {db_info}")
      if connection.is_connected():
        cursor = connection.cursor()
        self.drop_coor_paso_table(self,cursor)
        self.create_coor_paso_table(self,cursor, table_name)
        self.add_coor_paso_index(self,cursor)
        self.insert_coor_paso(self,cursor, table_name)
        self.Resolver.showMessage(self.Resolver, "coor_paso_done", table_name)
    except Error as e:
      print(f"❌ MySQL error: {e}")
    finally:
      if 'connection' in locals() and connection.is_connected():
        cursor.close()
        #connection.close()
        self.Resolver.showMessage(self.Resolver, "paso_loaded", table_name)
    return connection

  def drop_coor_paso_table(self, cursor):
    sql = f'DROP TEMPORARY TABLE IF EXISTS coorPaso;'
    records = self.connection_query(self, cursor, sql, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def create_coor_paso_table(self, cursor, table_name):
    sql = f'''CREATE TEMPORARY TABLE coorPaso (id_coord int(11),
	SCIENTIFIC_NAME VARCHAR(100),  
    STATE VARCHAR(255),
    OBSERVATION_COUNT_NUM INT(11),
    OBSERVATIONDATE DATETIME);'''
    records = self.connection_query(self, cursor, sql, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def add_coor_paso_index(self, cursor):
    sql = 'ALTER table coorPaso ADD INDEX (id_coord), ADD INDEX (SCIENTIFIC_NAME);'
    records = self.connection_query(self, cursor, sql, True)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def insert_coor_paso(self, cursor, table_name):
    sql = f'INSERT INTO coorPaso (SELECT id_coord, SCIENTIFIC_NAME, STATE, OBSERVATION_COUNT_NUM, OBSERVATION_DATE FROM ebird_{table_name} WHERE APPROVED = 1);'
    records = self.connection_query(self, cursor, sql, True)
    self.commit(self, cursor)
    #self.Resolver.showMessage(self.Resolver, "col_indexes_created", table_name)
    return

  def add_coord_agrup(self,table_name):
    sql = f'DROP TABLE IF EXISTS coord_agrup_{table_name}";'
    self.query(self, sql, None, False)
    sql = f'''CREATE TABLE coord_agrup_{table_name} (`id_coord` int(11) DEFAULT NULL,
			 `SCIENTIFIC_NAME` varchar(100) DEFAULT NULL,
			 `STATE` varchar(100) DEFAULT NULL, 
			`CONTEO_MAX` int(11) DEFAULT NULL, 
			`FECHA_MIN` datetime DEFAULT NULL, 
			`FECHA_MAX` datetime DEFAULT NULL,
			`NUMERO_REGISTROS` INT DEFAULT NULL
			) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''
    self.query(self, sql, None, False)
    return

  def insert_coord_agroup(self,table_name):
    sql = f'''INSERT INTO coord_agrup_{table_name} (
      SELECT id_coord, SCIENTIFIC_NAME, STATE, MAX(OBSERVATION_COUNT_NUM) AS CONTEO_MAX, 
        min(OBSERVATIONDATE) as FECHA_MIN, max(OBSERVATIONDATE) as FECHA_MAX, COUNT(1) as NUMERO_REGISTROS 
      FROM coorPaso
      GROUP BY id_coord, SCIENTIFIC_NAME);'''
    self.query(self, sql, None, False)
    self.commit(self)
    return

  def add_ebird_snib(self,table_name):
    sql = f'Create table ebird_snib{table_name} SELECT * FROM `ebird`.`ebird_{table_name}` e WHERE e.APPROVED = 1 AND e.gui_snib = 1 AND e.MRD <3 AND e.val_sp <5;'
    self.query(self, sql, None, False)
    return