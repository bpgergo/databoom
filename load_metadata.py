import re
from models import Func, Econ
import csv
import logging

pattern1 = re.compile("^(\d\.) (.*)")
s1 = "1. Általános közszolgáltatások"
pattern2 = re.compile("^(\d\d\d\d )(.*)")
s2 = "0111 Államhatalmi, törvényhozó és végrehajtó szervezetek"
pattern3 = re.compile("^(\d\d\d\d\d\d )(.*)")
s3 = "011110 Államhatalmi szervek tevékenysége"


def get_value(s, p):
    m = re.search(p, s)
    if m:
        return m.group(1), m.group(2)
    else:
        return None

def test():
    print(get_value(s1, pattern1))
    print(get_value(s2, pattern2))
    print(get_value(s3, pattern3))
    print("wtf32", get_value(s3, pattern2))
    print("wtf23", get_value(s2, pattern3))


def new_func(value, parent=None):
    id = value[0].replace(".", "").strip()
    val = value[1].replace("*", "").strip()
    func = Func(id=id, value=val)
    if parent:
        func.parent_id = parent.id
    return func


def load_func(fname):
    parent = None
    with open(fname) as f:
        for line in f.readlines():
            res1 = get_value(line, pattern1)
            if res1:
                func = new_func(res1)
                yield func
                parent = func
            else:
                res2 = get_value(line, pattern2)
                res3 = get_value(line, pattern3)
                if res2 and not res3:
                    func = new_func(res2, parent)
                    yield func
                    parent = func
                elif res3:
                    if res3:
                        func = new_func(res3, parent)
                        yield func


econ_parent_ids_raw = \
"15,15,15,15,15,15,15,15,15,15,15,15,15,20,19,19,19,20,271,271,21,21,21,21,21,21,32,32,60,35,35,60,45,45,45,45,45,41,45,45,60,48,48,60,59,59,59,59,54,59,60,271,127,62,62,127,127,75,127,83,127,93,93,127,100,127,103,103,103,103,271,,194,154,154,194,167,194,181,181,181,181,271,203,203,203,203,203,271,208,208,208,271,270,221,270,232,232,270,245,270,258,258,258,258,271,310,"
econ_parent_ids = econ_parent_ids_raw.split(",")
#print(econ_parent_ids)

econ_ids_raw = \
"1 Törvény szerinti illetmények munkabérek K1101 ,2 Normatív jutalmak K1102 ,3 Céljuttatás projektprémium K1103 ,4 Készenléti ügyeleti helyettesítési díj túlóra túlszolgálat K1104 ,5 Végkielégítés K1105 ,6 Jubileumi jutalom K1106 ,7 Béren kívüli juttatások K1107 ,8 Ruházati költségtérítés K1108 ,9 Közlekedési költségtérítés K1109 ,10 Egyéb költségtérítések K1110 ,11 Lakhatási támogatások K1111 ,12 Szociális támogatások K1112 ,13 Foglalkoztatottak egyéb személyi juttatásai 14 K1113 ,15 Foglalkoztatottak személyi juttatásai 01 13 K11 ,16 Választott tisztségviselők juttatásai K121 ,17 Munkavégzésre irányuló egyéb jogviszonyban nem saját foglalkoztatottnak fizetett juttatások K122 ,18 Egyéb külső személyi juttatások K123 ,19 Külső személyi juttatások 16 17 18 K12 ,20 Személyi juttatások összesen 15 19 K1 ,21 Munkaadókat terhelő járulékok és szociális hozzájárulási adó 22 28 K2 ,22 ebből szociális hozzájárulási adó K2,23 ebből rehabilitációs hozzájárulás K2,24 ebből korkedvezmény biztosítási járulék K2 ,25 ebből egészségügyi hozzájárulás K2 ,26 ebből táppénz hozzájárulás K2 ,28 ebből munkáltatót terhelő személyi jövedelemadó K2 ,29 Szakmai anyagok beszerzése K311 ,30 Üzemeltetési anyagok beszerzése K312 ,32 Készletbeszerzés 29 30 31 K31 ,33 Informatikai szolgáltatások igénybevétele K321 ,34 Egyéb kommunikációs szolgáltatások K322 ,35 Kommunikációs szolgáltatások 33 34 K32 ,36 Közüzemi díjak K331 ,37 Vásárolt élelmezés K332 ,38 Bérleti és lízing díjak 39 K333 ,40 Karbantartási kisjavítási szolgáltatások K334 ,41 Közvetített szolgáltatások 42 K335 ,42 ebből államháztartáson belül K335 ,43 Szakmai tevékenységet segítő szolgáltatások K336 ,44 Egyéb szolgáltatások K337 ,45 Szolgáltatási kiadások 36 37 38 40 41 43 44 K33 ,46 Kiküldetések kiadásai K341 ,47 Reklám és propagandakiadások K342 ,48 Kiküldetések reklám és propagandakiadások 46 47 K34 ,49 Működési célú előzetesen felszámított általános forgalmi adó K351 ,50 Fizetendő általános forgalmi adó K352 ,51 Kamatkiadások 52 53 K353 ,54 Egyéb pénzügyi műveletek kiadásai 55 57 K354 ,55 ebből valuta deviza eszközök realizált árfolyamvesztesége K354 ,58 Egyéb dologi kiadások K355 ,59 Különféle befizetések és egyéb dologi kiadások 49 50 51 54 58 K35 ,60 Dologi kiadások 32 35 45 48 59 K3 ,62 Családi támogatások 63 73 K42 ,72 ebből óvodáztatási támogatás Gyvt 20 C K42 ,73 ebből az egyéb pénzbeli és természetbeni gyermekvédelmi támogatások K42 ,74 Pénzbeli kárpótlások kártérítések K43 ,75 Betegséggel kapcsolatos nem társadalombiztosítási ellátások 76 82 K44 ,82 ebből helyi megállapítású közgyógyellátás Szoctv 50 3 bek K44 ,83 Foglalkoztatással munkanélküliséggel kapcsolatos ellátások 84 92 K45 ,91 ebből foglalkoztatást helyettesítő támogatás Szoctv 35 1 bek K45 ,93 Lakhatással kapcsolatos ellátások 94 99 K46 ,96 ebből lakásfenntartási támogatás Szoctv 38 1 bek a és b pontok K46 ,97 ebből adósságcsökkentési támogatás Szoctv 55 A 1 bek b pont K46 ,100 Intézményi ellátottak pénzbeli juttatásai 101 102 K47 ,102 ebből oktatásban résztvevők pénzbeli juttatásai K47 ,103 Egyéb nem intézményi ellátások 104 126 K48 ,118 ebből rendszeres szociális segély Szoctv 37 1 bek a d pontok K48 ,120 ebből egyéb az önkormányzat rendeletében megállapított juttatás K48 ,122 ebből átmeneti segély Szoctv 47 1 bek c pont K48 ,123 ebből köztemetés Szoctv 48 K48 ,127 Ellátottak pénzbeli juttatásai 61 62 74 75 83 93 100 103 K4 ,130 Elvonások és befizetések K502 ,154 Egyéb működési célú támogatások államháztartáson belülre 155 164 K506 ,155 ebből központi költségvetési szervek K506 ,163 ebből nemzetiségi önkormányzatok és költségvetési szerveik K506 ,167 Működési célú visszatérítendő támogatások kölcsönök nyújtása államháztartáson kívülre 168 178 K508 ,170 ebből egyéb civil szervezetek K508 ,181 Egyéb működési célú támogatások államháztartáson kívülre 182 192 K511 ,182 ebből egyházi jogi személyek K511 ,184 ebből egyéb civil szervezetek K511 ,185 ebből háztartások K511 ,188 ebből önkormányzati többségi tulajdonú nem pénzügyi vállalkozások K511 ,194 Egyéb működési célú kiadások 128 130 131 132 143 154 165 167 179 180 181 193 K5 ,195 Immateriális javak beszerzése létesítése K61 ,196 Ingatlanok beszerzése létesítése 197 K62 ,198 Informatikai eszközök beszerzése létesítése K63 ,199 Egyéb tárgyi eszközök beszerzése létesítése K64 ,202 Beruházási célú előzetesen felszámított általános forgalmi adó K67 ,203 Beruházások 195 196 198 202 K6 ,204 Ingatlanok felújítása K71 ,206 Egyéb tárgyi eszközök felújítása K73 ,207 Felújítási célú előzetesen felszámított általános forgalmi adó K74 ,208 Felújítások 204 207 K7 ,221 Felhalmozási célú visszatérítendő támogatások kölcsönök törlesztése államháztartáson belülre 222 231 K83 ,222 ebből központi költségvetési szervek K83 ,232 Egyéb felhalmozási célú támogatások államháztartáson belülre 233 242 K84 ,233 ebből központi költségvetési szervek K84 ,239 ebből helyi önkormányzatok és költségvetési szerveik K84 ,245 Felhalmozási célú visszatérítendő támogatások kölcsönök nyújtása államháztartáson kívülre 246 256 K86 ,249 ebből háztartások K86 ,258 Egyéb felhalmozási célú támogatások államháztartáson kívülre 259 269 K88 ,259 ebből egyházi jogi személyek K88 ,261 ebből egyéb civil szervezetek K88 ,262 ebből háztartások K88 ,265 ebből önkormányzati többségi tulajdonú nem pénzügyi vállalkozások K88 ,270 Egyéb felhalmozási célú kiadások 209 210 221 232 243 245 257 258 K8 ,271 Költségvetési kiadások 20 21 60 127 194 203 208 270 K1 K8 ,310 Költségvetési kiadások összesen"
econ_ids = econ_ids_raw.split(",")
#print(econ_ids)

pattern_e = re.compile("(\d+ )([a-zöüóőúéűáíA-ZÖÓÜŐÚÉÁŰÍ ]+).*")
se = "62 Családi támogatások 63 73 K42 "

def test_econs():
    print(get_value(se, pattern_e))

def load_econ():
    try:
        assert (len(econ_parent_ids) == len(econ_ids))
    except:
        print("parent len", len(econ_parent_ids))
        print("len", len(econ_ids))
        raise

    for i, input in enumerate(econ_ids):
        res = get_value(input, pattern_e)
        val = res[1]
        if val:
            val = val.strip()
        if val and val[-2] == " K":
            val = val[0:-2]
        parent_id = econ_parent_ids[i].strip()
        if len(parent_id) == 0:
            parent_id = None
        econ = Econ(id=res[0].strip(), parent_id=parent_id, value=val)
        yield econ


def generate_tags(fname):
    with open(fname) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        cnt = 0
        for row in reader:
            logging.info("processing row:%s" % row)
            id = get_value(row[0], pattern3)[0].strip()
            tags = row[1].strip()
            logging.info("processing id:%s, tags:%s" % (id, tags))
            yield (id, tags)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    #load_func("func_ids.txt")
    #test_econs()
    for t in generate_tags("tags.csv"):
        print(t[0], "--", t[1])
