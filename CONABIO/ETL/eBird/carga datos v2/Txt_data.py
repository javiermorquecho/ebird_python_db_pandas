import pandas as pd

class Txt_data:
  src_txt = "" #src txt file
  src_sep = "\t"  # separador de campos en archivo origen
  chunk_size = 100  # tamaño de la muestra
  # Las columnas con problemas de lectura se consideran cadenas(str), evitando errores
  ebird_dtypes_for_reading = {
    "BREEDING CODE": str,
    "BREEDING CATEGORY": str,
    "BEHAVIOR CODE": str,
    "AGE/SEX": str,
    "SPECIES COMMENTS": str,
    "OBSERVER ORCID ID": str,
    "PROJECT NAMES": str,
    "GROUP IDENTIFIER": str,
    "OBSERVATION COUNT": str,
    "CHECKLIST COMMENTS": str,
    "SUBSPECIES COMMON NAME": str,
    "SUBSPECIES SCIENTIFIC NAME": str,
    "EXOTIC CODE": str,
    "IBA CODE": str,
    "USFWS CODE": str,
    "PROJECT IDENTIFIERS": str,
  }
    
  def __init__(self, txt, sep, size ):
    self.src_txt = txt
    self.src_sep = sep
    self.chunk_size = size
    print(f"Init done with src:{self.src_txt}")

  def get_headers(self, src=None):
    if src is None:
        src_file = self.src_txt
    else:
        src_file = src
    reader = pd.read_csv(
        src_file,
        sep=self.src_sep,
        nrows=1
    )

    return list(reader.columns)

  def read_csv_file(self):
    print(self.src_txt);
    reader = pd.read_csv(
        self.src_txt,
        sep=self.src_sep,
        #chunksize=chunk_size,
        dtype=self.ebird_dtypes_for_reading,
    )
    return reader