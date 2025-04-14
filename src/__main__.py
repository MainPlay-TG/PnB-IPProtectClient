import sys
try:
  import requests
  import requests.auth
  from MainPlaySoft import MPSoft
  from MainShortcuts2 import ms
except Exception:
  import subprocess
  print("У вас не установлены необходимые библиотеки, придётся немного подождать",file=sys.stderr)
  subprocess.call([sys.executable,"-m","pip","install","-U","requests","MainPlaySoft","MainShortcuts2"])
  import requests
  import requests.auth
  from MainPlaySoft import MPSoft
  from MainShortcuts2 import ms
try:
  ms.utils.main_func
except Exception:
  import subprocess
  print("MainShortcuts2 устарел, обновляю",file=sys.stderr)
  subprocess.call([sys.executable,"-m","pip","install","-U","MainShortcuts2"])
  print("Перезапустите программу",file=sys.stderr)
  sys.exit(1)
mpsoft=MPSoft("MainPlay_TG","PawsNBlocksClient")
cfg=ms.cfg(mpsoft.dir.data+"/cfg.json")
cfg.default["host"]="mainplay-tg.ru"
cfg.default["http.timeout"]=10
cfg.default["nickname"]=None
cfg.default["token"]=None
cfg.dload(True)
def remove_alt_domain():
  alt_warn=False
  if "host.alt" in cfg:
    alt_warn=True
    del cfg["host.alt"]
  if "use_alt" in cfg:
    alt_warn=True
    del cfg["use_alt"]
  if alt_warn:
    print("Альт. адрес больше не может быть использован. Можно обращаться к API только напрямую. Конфиг изменён",file=sys.stderr)
    cfg.save()
  if cfg["host"] in ["mainplay-tg.ddns.net","mistvpn.ddns.net"]:
    print("Домен %s больше не действителен. Конфиг изменён"%cfg["host"],file=sys.stderr)
    cfg["host"]="mainplay-tg.ru"
    cfg.save()
remove_alt_domain()
@ms.utils.main_func(__name__)
def main():
  need_save=False
  if cfg["nickname"] is None:
    cfg["nickname"]=input("Введите свой ник\n> ").strip()
    need_save=True
  if cfg["token"] is None:
    import getpass
    cfg["token"]=getpass.getpass("Введите API токен\n> ").strip()
    need_save=True
  if need_save:
    cfg.save()
  AUTH=requests.auth.HTTPBasicAuth(cfg["nickname"],cfg["token"])
  with requests.Session() as http:
    kw={}
    kw["auth"]=AUTH
    kw["json"]={}
    kw["timeout"]=cfg["http.timeout"]
    kw["url"]="https://%s/PawsNBlocks/api/client/allowed_ip"%cfg["host"]
    try:
      with http.post(**kw) as resp:
        if resp.status_code==403:
          print("Ошибка авторизации. Запросите новый API токен и повторите попытку",file=sys.stderr)
          cfg["token"]=None
          cfg.save()
          return
        resp.raise_for_status()
      return
    except Exception as exc:
      print("Не удалось соединиться с сервером. Проверьте подключение к интернету и попробуйте снова. Если проблема повторяется, спросите в чате https://t.me/PawsNBlocks/1",file=sys.stderr)
      sys.exit(1)