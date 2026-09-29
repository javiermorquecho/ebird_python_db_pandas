import nbformat
from IPython.display import display, Javascript
from pathlib import Path

class Manager:

  messages = {
    "check_table_sql":"👀 Verifica que el SQL de la tabla es correcto, de lo contrario, vuelve a darles valor a las variables ó verifica tu archivo.",
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
    "init_class_txt":"✅ Instancia de clase Data",
    "init_class_db":"✅ Instancia de clase DB",
  }

  def __init__():
      print("Manager")
      return

  def showMessage(self, id_message, data=None):
    # Requests permission and fires a native browser Notification API event
    #js_code = f"""
    #if (Notification.permission !== 'granted') {{
    #  Notification.requestPermission();
    #}} else {{
    #  new Notification('{self.messages[id_message]}');
    #}}
    #"""
    #display(Javascript(js_code))
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
    return

  def show_end_time():
    end_time = datetime.now()
    print(f"--- Process Finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    duration = end_time - start_time
    print(f"Total time elapsed: {duration}")
    return

  def clear_notebook_outputs():
    js_clear_all = '''
    document.querySelectorAll('pre').forEach(element => element.remove());
    '''
    display(Javascript(js_clear_all))
    return

  def get_file_exists(self, file_path):
    file_path = "./../" + file_path
    return file_path
    
  def check_file_exists(self, file_path):
    file_path = Path(file_path)
    
    if file_path.is_file():
      return True
    else:
      return False

  def get_replace_table_if_exist(self, replace_table_if_exist):
    if replace_table_if_exist.strip() == "" or replace_table_if_exist is None:
      return False
    else:
      return replace_table_if_exist.lower() == "true"

  def check_replace_table_if_exist(self, replace_table_if_exist):
    if isinstance(replace_table_if_exist, bool):
      return replace_table_if_exist
    else:
      return False

  def get_delimiter(self, src_sep):
    match src_sep:
      case "tabulador":
        return "\t"
      case "coma":
        return ","
      case "punto_y_coma":
        return ";"
      case "pipe":
        return "|"
    return None

  def check_delimiter(self, src_sep):
    if src_sep is None:
      #print("El delimitador no es el correcto.")
      return False
    return True

  def check_table_name(self, table_name):
    if table_name.strip() == "":
      return False
    return True


  def check_src_sep(self, src_sep):
    if src_sep is None:
      return False
    return True

  def get_params_errors(self, eval_src_txt_file, eval_replace_table_if_exist, eval_table_name, eval_src_sep):
    m_src_txt_file = self.get_error_message(self, eval_src_txt_file, "El archivo txt no existe en la ubicación")
    m_replace_table_if_exist = self.get_error_message(self, eval_replace_table_if_exist, "Error en valor en decisión de si reemplazamos la tabla")
    m_table_name = self.get_error_message(self, eval_table_name, "El nombre de la tabla no está completo")
    m_src_sep = self.get_error_message(self, eval_src_sep, "El separador no es correcto")

    m_eval = all(x is True for x in [m_src_txt_file, m_replace_table_if_exist, m_table_name, m_src_sep])
    
    result = {
      "eval": m_eval,
      "errors":
      {
        "src_txt_file": m_src_txt_file,
        "replace_table_if_exist": m_replace_table_if_exist,
        "table_name": m_table_name,
        "src_sep": m_src_sep,
      }
    }
    return result 

  def get_error_message(self, to_eval, error) -> str | bool:
    if to_eval == False or to_eval is None or to_eval == "":
      return error
    else:
      return True

  def eval_errors(self, errors):
    for key, value in errors:
      if value == True:
        print(f'✅ {key}')
      else:
        print(f'❌ {value}')
    print("Vuelve a correr este script")
    return

  def show_values_selected(self, src_txt_file, replace_table_if_exist, table_name, src_sep):
    print("Valores seleccionados:")
    print(f'✅ Archivo Txt')
    print(f'✅ Reemplzar tabla si existe')
    print(f'✅ Nombre de la tabla')
    print(f'✅ Separador')
    print("Variables configuradas. Continua.")
    return
    