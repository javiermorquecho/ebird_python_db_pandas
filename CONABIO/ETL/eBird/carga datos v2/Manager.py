class Manager:

  messages = {
    "check_table_sql":"⚠️ Verifica que el SQL de la tabla es correcto, de lo contrario, vuelve a darles valor a las variables ó verifica tu archivo.",
    "table_deleted":"✅ Se borró la tabla...",
    "table_created":"✅ Se creó la tabla...",
    "col_index_created":"✅ Se crearon campos para indexar en la tabla...",
    "col_id_add_numbers":"✅ Se agregaron los números consecutivos en el campo Id...",
    "col_indexes_created":"✅ Se crearon los índices de los nuevos campos de la tabla...",
    "csv_loaded":"✅ Se cargo la información del CSV en la tabla...",
    "show_afew_paso_rows":"✅ Mostando algunos registros de la tabla temporal Paso...",
    "paso_loaded":"✅ Termina proceso de la tabla Paso...",
    "wait":"⌛ Esta operación puede tardar...",
    "wait5":"⌛ Espera 5 segundos, por favor...",
    "coor_paso_done":"✅ Proceso de coor paso, hecho...",
  }

  def __init__():
      print("Manager")
      return

  def showMessage(self, id_message, data=None):
    print(self.messages[id_message])
    if data is not None:
      print(data)
    return

  def stop():
    raise SystemExit("❌ La ejecución se detuvo!")
    #raise StopExecution
    #raise SystemExit("Stopping cell execution here.")
    #sys.exit(0)
    return

def show_start_time():
    start_time = datetime.now()
    print(f"--- Process Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')} ---")

def show_end_time():
    end_time = datetime.now()
    print(f"--- Process Finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    duration = end_time - start_time
    print(f"Total time elapsed: {duration}")