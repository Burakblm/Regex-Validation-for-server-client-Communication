import sqlite3

class Database():
    
    def __init__(self):
        self.conn = sqlite3.connect('example.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Data
                    (DATE, TIME, X, Y, W, H)''')
        self.dt_push()

    def split(self,txt):
        dtime = txt.split()
        return [dtime[0],dtime[1],dtime[2],dtime[3],dtime[4],dtime[5]]

    def add(self,date, time, x, y, w, h):
        self.data = (date, time,x, y, w, h)
        self.c.execute(f"INSERT INTO Data VALUES (?,?,?,?,?,?)",self.data)
        self.conn.commit()

    def dt_push(self):
        try:
            file = open("file.txt","r")
            fil = file.readlines()
            for i in fil:
                dtb = self.split(i)
                self.add(dtb[0],dtb[1],dtb[2],dtb[3],dtb[4],dtb[5])
            self.conn.close()
            print("Database push completed...")
        except IOError:
            print("An error occured!")
        finally:
            file.close()
