import os, time, xlsxwriter, pymysql

folders_list = []
files_list = []
lista_ignorare = []
DB_connected = False
cur = ''
db = ''

class Folders:
    folders_total = 1

    def __init__(self, folder, path):
        global folders_list
        self.index = Folders.folders_total
        self.folder = folder
        self.path = path
        folders_list.append(self)
        Folders.folders_total += 1


class Files_from_HDD:
    files_total = 1

    def __init__(self, file, path):
        global files_list
        self.index = Files_from_HDD.files_total
        self.nume_fisier = file
        self.nume_fisier_trunchiat = file[0:len(file) - 4]
        self.path = path.replace('\\','\\\\')
        self.size = ""
        self.size = os.path.getsize(os.path.join(self.path, self.nume_fisier))
        self.creation_date = time.ctime(os.path.getctime(os.path.join(self.path, self.nume_fisier)))
        self.modify_date = time.ctime(os.path.getmtime(os.path.join(self.path, self.nume_fisier)))
        files_list.append(self)

class Files_from_DB:

    def __init__(self, element):
        global files_list
        self.id_fisier = element[0]
        self.nume_fisier = element[1]
        self.nume_fisier_trunchiat = element[2]
        self.path = element[3]
        self.size = element[4]
        self.creation_date = element[5]
        self.modify_date = element[6]
        files_list.append(self)       


def Import(cale):
    global lista_ignorare, files_list
    if DB_connected:
        for (path, folders, files) in os.walk(cale):
            for folder in folders:
                if folder not in lista_ignorare:
                    try:
                        obiect = len(globals())
                        globals()[obiect] = Folders(folder, path)
                    except Exception as error:
                        print ('A aparut eroarea: ' + str(error))
            for file in files:
                if path not in lista_ignorare:
                    try:
                        obiect = len(globals())
                        globals()[obiect] = Files_from_HDD(file, path)
                    except Exception as error:
                        print ('A aparut eroarea: ' + str(error))
    scriere_log(str(time.ctime()) + ": Din " + str(cale) + " s-au importat " + str(len(folders_list)) + " foldere")
    scriere_log(str(time.ctime()) + ": Din " + str(cale) + " s-au importat " + str(len(files_list)) + " fisiere")


def remove(cale):
    global lista_ignorare
    lista_ignorare.append(cale)


def incarcare_fisiere_din_HDD_in_RAM():
    remove('F:\\Deea\\back-up andreea\\documente\\proiecte andreea\\FACULTATE\\licenta\\licenta cd')
    remove('F:\\Deea\\back-up andreea\\Foldere de pe desktop\\mesaje 24.05.2010\\inbox all')
    remove('F:\\Deea\\back-up andreea\\kmy\\diverse\\')
    remove('F:\\Deea\\back-up andreea\\documente\\proiecte andreea\\FACULTATE\\an II sem I\\proiect tp sampoane')
    remove('F:\\Deea\\back-up andreea\\documente\\proiecte andreea\\FACULTATE\\an III sem II\\b2b individual')
    remove('F:\\Deea\\back-up andreea\\Foldere de pe desktop\\mesaje 24.05.2010\\outbox all\\2')
    remove('F:\\Deea\\back-up andreea\\Foldere de pe desktop\\mesaje 24.05.2010\\outbox all\\1')
    remove('F:\\Deea\\back-up andreea\\poze bumb\\ionut')
    remove('F:\\Deea\\back-up andreea\\2009 - 2\\sf mihail 2009')
    remove("F:\\Deea\\back-up andreea\\D\\poze\\2009\\2009 - 1")
    remove("F:\\Deea\\back-up andreea\\2009 - 2\\")
    remove("F:\\Deea\\back-up andreea\\2009 - 1\\herastrau noi2009")
    remove("F:\\Deea\\back-up andreea\\D\\poze\\2009\\2009 - 1\\herastrau noi2009")
    remove("F:\\Deea\\back-up andreea\\D\\poze\\2009\\2009 - 1\\21noi2009")
    remove("F:\\Deea\\back-up andreea\\2009 - 1\\luminite 2009")
    remove("F:\\Deea\\back-up andreea\\2009 - 1\\moieciu 19-20 dec 2009")
    remove("F:\\Deea\\back-up andreea\\D\\deskt\\rent a car")
    remove("F:\\Deea\\back-up andreea\\D\\Foldere de pe desktop\\mesaje 24.05.2010\\inbox all")
    remove("F:\\Deea\\back-up andreea\\D\\Foldere de pe desktop\\mesaje 24.05.2010\\outbox all\\1")
    remove("F:\\Deea\\back-up andreea\\D\\Foldere de pe desktop\\mesaje 24.05.2010\\outbox all\\2")
    remove("F:\\Deea\\back-up andreea\\D\\Foldere de pe desktop\\muzica 2012")
    remove("F:\\Deea\\back-up andreea\\D\\Foldere de pe desktop\\Poze album, puzzle\\Poze album Mickey")
    remove("F:\\Deea\\back-up andreea\\D\\ionut- camy\\poze\\bumbu,tzuti moieciu 01,05-08\\Imagini")
    remove("F:\\Deea\\back-up andreea\\D\\ionut- camy\\radoi\\muzica")
    remove("F:\\Deea\\back-up andreea\\D\\poze\\2008\\moeciu 1-5 aug2008\\tel")
    remove("F:\\Deea\\back-up andreea\\Foldere de pe desktop\\mesaje 24.05.2010")
    remove("F:\\Deea\\back-up andreea\\kmy\\poze servici kmy")
    remove("F:\\Deea\\back-up andreea\\2009 - 1\\Padure călugăreni")e
    remove('F:\\D\\raman\\Mesaje E50')
    remove('F:\\Deea\\back-up andreea\\GAMES\\Atomic Bomberman')
    remove('F:\\Deea\\back-up andreea\\deskt\\kituri programe')
    remove('F:\\Deea\\back-up andreea\\foto camy')
    remove('')
    remove('')
    Import("F:\\")


def scriere_log(mesaj):
##    LogFile = open("LogFileDuplicateFileFinder.txt", "a")
##    LogFile.write(mesaj + "\n")
    print (mesaj)
##    LogFile.close()


def conectare_db():
    global DB_connected, cur, db
    try:
        db = pymysql.connect(host="127.0.0.1",
                             user="root",
                             passwd="",
                             db="duplicate_file_finder2")
        cur = db.cursor()
        DB_connected = True
        print ('Conectat la DB')
    except Exception as error:
        print (str(error))


def query_without_reply(query):
    global cur, db
    try:
        cur.execute(query)
        db.commit()
    except Exception as error:
        print ('A aparut eroarea: ' + str(error))
        print ('Query-ul incercat a fost: ' + query)


def query_with_reply(query):
    global cur, db
    try:
        cur.execute(query)
        db.commit()
        return cur.fetchall()
    except Exception as error:
        print ('A aparut eroarea: ' + str(error))
        print ('Query-ul incercat a fost: ' + query)


def inserare_fisiere_in_DB():
    global DB_connected, folders_list, files_list, cur, db
    if DB_connected:
        for obiect in files_list:
            if obiect.nume_fisier != "Thumbs.db":
                try:
                    query = 'INSERT INTO fisier VALUES (default,"{0}","{1}","{2}","{3}","{4}","{5}")'.format(
                        obiect.nume_fisier, obiect.nume_fisier_trunchiat, obiect.path, obiect.size,
                        obiect.creation_date, obiect.modify_date)
                    query_without_reply(query)
                except Exception as error:
                    print ('A aparut eroarea: ' + str(error))
            del obiect
        folders_list = []
        files_list = []


def incarcare_din_DB_in_RAM():
    global DB_connected, cur, db
    if DB_connected:
        try:
            query = "select * from fisier"
            cur.execute(query)
            db.commit()
            rezultat = cur.fetchall()
            if len(rezultat) > 0:
                for element in rezultat:
                    obiect = len(globals())
                    globals()[obiect] = Files_from_DB(element)
        except Exception as error:
            print ('A aparut eroarea: ' + str(error))

def main():
    conectare_db()
##    incarcare_fisiere_din_HDD_in_RAM() #Se ruleaza o singura data!!!
##    inserare_fisiere_in_DB() #Se ruleaza o singura data!!!
    incarcare_din_DB_in_RAM()
    parcurgere_lista_DB()
    query = 'SELECT SUM(run_time) FROM run_times'
    total_time = round (query_with_reply(query)[0][0] / 60)
    print ('Verificarea fisierelor a durat {0} minute'.format(total_time))


def parcurgere_lista_DB():
    global DB_connected

    primul_timp = time.time()

    for i in range(len(files_list)):
        id_fisier1 = files_list[i].id_fisier
        nume_fisier1 = files_list[i].nume_fisier
        path1 = files_list[i].path
        size1 = files_list[i].size
        creation_date1 = files_list[i].creation_date
        modify_date1 = files_list[i].modify_date
        print ("Suntem la iteratia1: {0} {1}".format(id_fisier1, nume_fisier1))

        for j in range(i+1, len(files_list)):
            id_fisier2 = files_list[j].id_fisier
            nume_fisier2 = files_list[j].nume_fisier
            path2 = files_list[j].path
            size2 = files_list[j].size
            creation_date2 = files_list[j].creation_date
            modify_date2 = files_list[j].modify_date
            Verificare(nume_fisier1, path1, size1, creation_date1, modify_date1, nume_fisier2, path2, size2, creation_date2, modify_date2)

        query = "DELETE FROM fisier WHERE id_fisier = {0}".format(id_fisier1)
        query_without_reply(query)

        timp_doi = time.time() #resetare parametru final
        diferenta_timp = timp_doi - primul_timp
        primul_timp = time.time() #resetare parametru initial
        query = 'INSERT INTO run_times values (default,"{0}")'.format(round(diferenta_timp,14))
        query_without_reply(query)


def Verificare(nume_fisier1, path1, size1, creation_date1, modify_date1, nume_fisier2, path2, size2, creation_date2, modify_date2):
    if nume_fisier1 == nume_fisier2 and size1 == size2:
        query = 'INSERT INTO duplicates VALUES (default,"{0}","{1}","{2}")'.format(path1.replace('\\','\\\\') + '\\\\' + nume_fisier1, path2.replace('\\','\\\\') + '\\\\' + nume_fisier2, 'fisiere identice')
        query_without_reply(query)
        scriere_log(str(time.ctime()) + ": S-au gasit 2 fisiere identice: " + nume_fisier1)
        scriere_log(path1 + '\\' + nume_fisier1)
        scriere_log(path2 + '\\' + nume_fisier2 + "\n")

    elif creation_date1 == creation_date2 and size1 == size2:
        query = 'INSERT INTO duplicates VALUES (default,"{0}","{1}","{2}")'.format(path1.replace('\\','\\\\') + '\\\\' + nume_fisier1, path2.replace('\\','\\\\') + '\\\\' + nume_fisier2, 'fisierele au aceeasi data de creare')
        query_without_reply(query)
        scriere_log(str(time.ctime()) + ": S-au gasit 2 fisiere care au aceeasi data de creare: ")
        scriere_log(path1 + '\\' + nume_fisier1)
        scriere_log(path2 + '\\' + nume_fisier2 + "\n")

    elif modify_date1 == modify_date2 and size1 == size2:
        query = 'INSERT INTO duplicates VALUES (default,"{0}","{1}","{2}")'.format(path1.replace('\\','\\\\') + '\\\\' + nume_fisier1, path2.replace('\\','\\\\') + '\\\\' + nume_fisier2, 'fisierele au aceeasi data de modificare')
        query_without_reply(query)
        scriere_log(str(time.ctime()) + ": S-au gasit 2 fisiere care au aceeasi data de modificare: " + nume_fisier1)
        scriere_log(path1 + '\\' + nume_fisier1)
        scriere_log(path2 + '\\' + nume_fisier2 + "\n")


main()
db.close()
input("Apasa <enter> pentru a iesi")
