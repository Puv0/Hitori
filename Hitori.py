def sayıları_al():
    dosya = open ("hitori_bulmaca.txt", "r")
    sayılar = dosya.read ()
    dosya.seek (0)
    global sütun
    sütun = len (dosya.readlines ())
    dosya.seek (0)
    sayılar_listesi = [i.split () for i in dosya.readlines ()]
    for i in range (len (sayılar_listesi)):
        for j in sayılar_listesi:
            j[i] = j[i].replace (j[i], f'-{j[i]}-')
    dosya.close ()
    sayılar_listesi.insert (0, "")
    return sayılar_listesi

def tiresiz_sayılar():
    dosya = open ("hitori_bulmaca.txt", "r")
    tiresiz_liste = [i.split () for i in dosya.readlines ()]
    dosya.close ()
    return tiresiz_liste


def kazanma_durumu(tiresiz_liste):
    sütun_için = []
    y = tiresiz_liste
    win= None
    for i in tiresiz_liste:
        for j in i:
            sütun_için.append (j)
    x = len (tiresiz_liste)  # eleman sayısının kaç olduğunu bulmak için kullanılıyor
    for i in range (len (tiresiz_liste)):
        y = y[1::]
        for eleman in tiresiz_liste[i]:  # i indexteki elemanları döndürüyor
            indeks = tiresiz_liste[i].index (eleman)
            if tiresiz_liste[i].count (eleman) != 1 and eleman != "X":  # satırdaki aynı elemanları kontrol ediyor
                return False
            uzunluk = len (y)
            say = 0
            while say != uzunluk:
                say += 1
                if eleman == y[say - 1][indeks] and eleman != "X": # sütumdaki aynı elemanları kontrol ediyor

                    return False
    try:
        sayım = 0
        for l in range (len (sütun_için)):
            while True:
                if sütun_için[l] == "X" and sütun_için[x + sayım] == "X": #Sütundaki x leri kontrol ediyor
                    return False
                else:
                    sayım += 1
                    break
    except IndexError:
        pass

    try:
        for p in range(len(tiresiz_liste)): # X'lerin yan yana gelme durumu
            for g in range(len(tiresiz_liste)):
                if tiresiz_liste[p][g] != "X":
                    break
                elif tiresiz_liste[p][g] == "X" and tiresiz_liste[p][g+1] =="X":
                    return False
                else:
                    break
    except IndexError:
        pass

    return win


def kullanıcı_işlemleri():
    while True:
        uzunluk1 = sayıları_al ()
        uzunluk = len (uzunluk1) - 1
        aksiyon = input (f'Satır numarasını ({1}-{uzunluk}), sütun numarasını ({1}-{uzunluk}) ve işlem kodunu (B:boş, D:dolu, N:normal/işaretsiz) aralarında boşluk bırakarak giriniz:')
        if len (aksiyon) != 5:
            print ("Lütfen Boşluklu Giriniz")
            continue
        boşluk_için = [""]
        say = 0
        işlem = []  # kullanıcı verileri için #1 satır #2 satır #3 işlem
        for i in aksiyon.split ():
            if i.isspace () == False:
                boşluk_için.append (i)
        for j in boşluk_için:
            say += 1
            if say == 2 or say == 3:
                işlem.append (int (j))
        işlem.insert (2, boşluk_için[3])
        işlem.insert (0, "")
        if işlem[1] > uzunluk or işlem[2] > uzunluk or işlem[1] < 1 or işlem[2] < 1:
            print ("Lütfen Sayıları Doğru Giriniz:")
            continue
        elif işlem[3] != "B" and işlem[3] != "b" and işlem[3] != "N" and işlem[3] != "n" and işlem[3] != "d" and işlem[3] != "D":
            print ("Lütfen Hamlenizi Doğru Seçiniz")
            continue
        else:
            return işlem


def oyun_tahta(işlem_görcek_sayı):
    sayılar = işlem_görcek_sayı
    sütun = len (sayılar) - 1

    for k in range (1, sütun + 1):
        print ("     ", k, end="")
    print (" ")
    c = 0
    for i in sayılar:
        if i == "":
            continue
        c += 1
        print (c, end=" -  ")
        for j in i:
            print (j, end="    ")
        print ("")


def main():
    sayılar = sayıları_al ()
    oyun_tahta (sayılar)
    hamle_say = 0  # sayıları alı 1 kere kullanmak için
    while True:
        hamle_say += 1
        işlem = kullanıcı_işlemleri ()

        if hamle_say == 1:
            işlem_görcek_sayı = sayıları_al ()
            boş_için = sayıları_al ()
            tiresiz_liste = tiresiz_sayılar ()
            tiresiz_boş = tiresiz_sayılar ()
        if işlem[3] == "B" or işlem[3] == "b":
            işlem[3] = "-X-"
            tiresiz_liste[işlem[1] - 1][işlem[2] - 1] = "X"
        elif işlem[3] == "D" or işlem[3] == "d":
            x = işlem_görcek_sayı[işlem[1]][işlem[2] - 1]  # tireyi silmek için yapılmıştır
            işlem[3] = x.replace (x, f'({x[1:2]})')
        elif işlem[3] == "N" or işlem[3] == "n":
            işlem[3] = boş_için[işlem[1]][işlem[2] - 1]
            tiresiz_liste[işlem[1] - 1][işlem[2] - 1] = tiresiz_boş[işlem[1] - 1][işlem[2] - 1] #kazanma durumunu kontrol edebilmek için
        işlem_görcek_sayı[işlem[1]][işlem[2] - 1] = işlem[3] # işlemi oyuna yansıtmak için
        oyun_tahta (işlem_görcek_sayı)
        win = kazanma_durumu (tiresiz_liste)
        if win != False:
            print ("Tebrikler Kazandınız!")
            break
main ()