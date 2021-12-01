import pandas as pd    # Modulok meghívása
import os
import csv
from calculater import calculate as cal    # A kalkulátor fájl behívása

final_path = os.path.abspath("..\..\converted_csv_datas\\teams")   # A csapatok mappájának abszolúlt elérési útvonala
start_path = os.path.abspath("..\..\converted_csv_datas\csv_result") # Itt kérdezi meg a terminálban az útvonalat, a csv_result mappát kell belehúzni a terminálba.
print(start_path)

def create_team_csv(): # Függvény kezdete
  result_header = ["Dátum", "Meccs-Id", "Hazai-Csapat", "Ellenfél-Csapat", # A main_result és a csapat_csv-k fejlécének elnevezései
                  "Hazai-Gól", "Ellenfél-Gól", "Hazai-XG", "Ellenfél-XG",
                  "Hazai-PR", "Ellenfél-PR", "PR-diff", "Hazai-xgPR", "Ellenfél-xgPR",
                  "XG-diff","Hazai-Mixed-PR", "Ellenfél-Mixed-PR","Mixed-PR-diff", "H%", "D%", "A%", "ForeCast-W",
                  "ForeCast-D", "ForeCast-A"]
  team_header = ["Dátum", "Meccs-Id", "Fő-Csapat", "Ellenfél-Csapat","Hazai-Gól",
                "Ellenfél-Gól","Hazai-XG","Ellenfél-XG", "Meccs-Előtti-PR", "Meccs-Utáni-PR", "Meccs-Előtti-xgPR",
                "Meccs-Utáni-xgPR", "Meccs-Előtti-Mixed_PR", "Meccs-Utáni-Mixed_PR"]

  f = [] # A "h" tárolja a mappa útvonalakat, az "f" a mappákban lévő fájlok neveit
  g = []
  path = []
  for (dirpath, dirnames, filenames) in os.walk(start_path): # Az os.walk iterál végig a csv_result mappa almappáin és az azokban lévő fájlokon.
    f.extend(filenames)
    g.extend(dirnames)
    path.append(dirpath)
  for dir_results in g: # Az első "for" a mappákon iterál végig, a második "for" a mappákban lévő fájlokon.
    for file in f:
      print(file) 
      try:
        with open(path[0]+"\\"+dir_results+"\\"+file, "r") as file: # Megnyitja a "for" által megadott aktuális csv_result fájlt, "df" változóba kilistázza, aztán végigiterál rajta.
          csv_file = csv.reader(file)
          df = pd.DataFrame(csv_file)
          for row_index, row in df.iterrows():
            if row_index == 0: # Minden fájlban van fejléc. Az új fájl 0-adik indexén a fejléc van.
              if os.path.exists(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv") == False: # Ha ennél a sornál jár az iteráció, megvizsgálja, hogy létezik-e a main_result csv fájl.
                with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv", "w", newline='',encoding="utf-8") as main: # Ha létezik, akkor szimplán átugorja ezt az iterált sort. Ha nem, akkor létrehozza a fájlt és beírja
                  main_list = csv.writer(main, dialect='excel') # Az előzőleg a result_header változóba eltárolt fejlecet.
                  main_list.writerow(result_header)
            else:
                datas=cal(row, team_header) # A cal(row, team_header) meghívásával átadjuk az aktuálisan iterált csv_result fájl sorát és a csapat_csv fejlécét.
                pr = "" # Visszaérkeznek a "calculater" által küldött "datas" adatok.
                date = row[12] # A csv_result-ből kivett adatok "row"-ként vannak behívva, a calculater adatai "datas"-ként szerepel,
                math_id = row[0]
                teams = row[3], row[6]
                score_h = row[8]
                score_a=row[9]
                xg = [row[10], row[11]]
                pr_diff = datas[6]-datas[7]
                xg_diff=datas[8]-datas[9]
                prxg_diff=datas[10]-datas[11]
                if pr_diff == -0 or -0.0: # Itt van javítva a -0 anomália
                  pr_diff=0
                if xg_diff == -0 or -0.0:
                  xg_diff=0
                if prxg_diff == -0 or -0.0:
                  prxg_diff=0
                pr_diff = ("%.1f" % pr_diff) # Itt vannak beállítva a tizedesjegyek hossza
                xg_diff = ("%.1f" % xg_diff)
                prxg_diff = ("%.1f" % prxg_diff)
                datas[0] = ("%.4f" % datas[0])
                datas[1] = ("%.4f" % datas[1])
                datas[2] = ("%.4f" % datas[2])
                datas[3] = ("%.4f" % datas[3])
                datas[4] = ("%.4f" % datas[4])
                datas[5] = ("%.4f" % datas[5])
                forecast = [row[13], row[14], row[15]] # Itt van kitöltve a main_result és a hazai--vendég csapatok kitöltési dataszerkezete attól függően, hazai vagy vendég
                main_result = [date, math_id, teams[0], teams[1], score_h,
                              score_a, xg[0], xg[1], datas[6], datas[7], pr_diff, datas[8], datas[9],xg_diff, datas[10],
                              datas[11],prxg_diff, pr, pr, pr, forecast[0], forecast[1], forecast[2]]
                home_data = [date, math_id,"(H) "+teams[0],
                            "(V) "+teams[1], score_h, score_a,xg[0], xg[1], datas[6], datas[0],
                            datas[8], datas[2], datas[10], datas[4]]
                against_data = [date, math_id,"(V) "+teams[1],
                              "(H) "+teams[0], score_a, score_h,xg[1], xg[0], datas[7], datas[1],
                              datas[9], datas[3], datas[11], datas[5]]
                with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv", "r") as read_main:
                  read_main = csv.reader(read_main)
                  list_id=[]
                  for index,i in enumerate(read_main):
                    if index==0:
                      continue
                    list_id.append(int(i[1]))
                  if int(main_result[1]) in list_id:
                    continue
                  else:
                    with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv", "a", newline='',encoding="utf-8")as main:
                      main = csv.writer(main, dialect='excel')
                      main.writerow(main_result)
                  with open(final_path+"\\"+teams[0]+".csv", "r", newline='', encoding="utf-8") as home_csv_old:
                    home_table_old = csv.reader(home_csv_old)
                    home_old_list = []
                    for home_list in home_table_old:
                      home_old_list.append(home_list)
                    if [home_data] not in home_old_list:
                      with open(final_path+"\\"+teams[0]+".csv", "a", newline='', encoding="utf-8") as home_csv:
                        home_table = csv.writer(home_csv, dialect='excel')
                        home_table.writerow(home_data)
                  with open(final_path+"\\"+teams[1]+".csv", "r", newline='', encoding="utf-8") as against_csv_old:
                    against_table_old = csv.reader(against_csv_old)
                    against_old_list = []
                    for against_list in against_table_old:
                      against_old_list.append(
                      against_list)
                  with open(final_path+"\\"+teams[1]+".csv", "a", newline='', encoding="utf-8") as against_csv:
                    against_table = csv.writer(against_csv, dialect='excel')
                    if against_data not in against_old_list:
                      against_table.writerow(against_data)
      except FileNotFoundError:
        continue
create_team_csv()
