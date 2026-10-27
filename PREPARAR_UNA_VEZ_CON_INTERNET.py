from pathlib import Path
from urllib.request import urlopen,Request
import json,tarfile,io,sys
base=Path(__file__).resolve().parent
try:
 for package,version,folder,only in [
  ('three','0.149.0',base/'libs','build/three.min.js'),
  ('@mediapipe/holistic','0.5.1675471629',base/'libs'/'holistic',None)]:
  print('Descargando',package,flush=True)
  url='https://registry.npmjs.org/'+package+'/'+version
  meta=json.load(urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40))
  data=urlopen(Request(meta['dist']['tarball'],headers={'User-Agent':'Mozilla/5.0'}),timeout=120).read()
  with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tar:
   n=0
   for member in tar:
    if not member.isfile() or not member.name.startswith('package/'):continue
    relative=member.name[len('package/'):]
    if only and relative!=only:continue
    if not only and not relative.endswith(('.js','.wasm','.data','.binarypb','.tflite')):continue
    target=folder/(Path(relative).name if only else relative)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(tar.extractfile(member).read());n+=1
   if not n:raise RuntimeError('No se encontraron archivos para '+package)
  print('OK:',n,'archivos')
 print('Listo: se puede jugar sin internet.')
except Exception as e:
 print('ERROR:',e);sys.exit(1)
