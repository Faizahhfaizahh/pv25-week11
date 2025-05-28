from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QFileDialog, QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt 
import sqlite3
import csv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("week11.ui", self)

        self.statusBar.showMessage("Faizah - F1D022043") 
        self.setupDatabase()
        self.tampilkanData()

        self.pushButton_simpan.clicked.connect(self.simpanData)
        self.lineEdit_cariJudul.textChanged.connect(self.cariData)
        self.actionHapus_Data.triggered.connect(self.hapus_data_buku_byMenuBar)
        self.pushButton_hapus.clicked.connect(self.hapus_data_buku_byTombol)
        self.actionEkspor_ke_CSV.triggered.connect(self.ekspor_ke_csv)
        self.tableWidget.cellDoubleClicked.connect(self.edit_data_buku)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.pushButton_pasteClipboard.clicked.connect(self.paste_from_clipboard) 

    # Function untuk setup database
    def setupDatabase(self):
        self.conn = sqlite3.connect("data_buku2.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS buku (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT,
                penulis TEXT,
                tahun INTEGER,
                kategori TEXT,
                tempat TEXT,
                penerbit TEXT
            )
        """)
        self.conn.commit()

    # Function untuk menyimpan data buku
    def simpanData(self):
        judul = self.lineEdit_judul.text()
        penulis = self.lineEdit_penulis.text()
        tahun = self.lineEdit_tahun.text()
        kategori = self.lineEdit_kategori.text()
        tempat = self.lineEdit_tempatTerbit.text()
        penerbit = self.lineEdit_penerbit.text()

        # Validasi untuk memastikan data (input) tidak kosong
        if not all([judul, penulis, tahun, kategori, tempat, penerbit]):
            QMessageBox.warning(self, "Input Tidak Lengkap", "Harap isi semua field.")
            return
        
         # Validasi untuk memastikan tahun berupa angka
        if not tahun.isdigit():
            QMessageBox.warning(self, "Input Tidak Valid", "Tahun harus berupa angka.")
            return

        if judul and penulis and tahun and kategori and tempat and penerbit:
            self.cursor.execute("INSERT INTO buku (judul, penulis, tahun, kategori, tempat, penerbit) VALUES (?, ?, ?, ?, ?, ?)",
                                (judul, penulis, tahun, kategori, tempat, penerbit))
            self.conn.commit()
            self.tampilkanData()
            self.lineEdit_judul.clear()
            self.lineEdit_penulis.clear()
            self.lineEdit_tahun.clear()
            self.lineEdit_kategori.clear()
            self.lineEdit_tempatTerbit.clear()
            self.lineEdit_penerbit.clear()

            QMessageBox.information(self, "Sukses", "Data buku berhasil disimpan!")

    # Function untuk menampilkan data ke TableWidget
    def tampilkanData(self):
        self.cursor.execute("SELECT * FROM buku")
        rows = self.cursor.fetchall()

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(rows):
            self.tableWidget.insertRow(i)
            # self.setReadOnlyItem(i, 0, row[0]) #agar ID tidak dapat diubah/Read-Only
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))    
            self.tableWidget.setItem(i, 1, QTableWidgetItem(row[1]))         
            self.tableWidget.setItem(i, 2, QTableWidgetItem(row[2]))        
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row[3]))) 
            self.tableWidget.setItem(i, 4, QTableWidgetItem(row[4]))         
            self.tableWidget.setItem(i, 5, QTableWidgetItem(row[5]))        
            self.tableWidget.setItem(i, 6, QTableWidgetItem(row[6]))        

    #Function untuk mencari buku berdasarkan judul
    def cariData(self):
        keyword = self.lineEdit_cariJudul.text()
        query = "SELECT * FROM buku WHERE judul LIKE ?"
        self.cursor.execute(query, ('%' + keyword + '%',))
        rows = self.cursor.fetchall()

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(rows):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))    
            self.tableWidget.setItem(i, 1, QTableWidgetItem(row[1]))        
            self.tableWidget.setItem(i, 2, QTableWidgetItem(row[2]))         
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row[3])))   
            self.tableWidget.setItem(i, 4, QTableWidgetItem(row[4]))        
            self.tableWidget.setItem(i, 5, QTableWidgetItem(row[5]))  
            self.tableWidget.setItem(i, 6, QTableWidgetItem(row[6]))  
                   
    #Function menghapus data buku dari Menu Bar Edit bagian Hapus Data
    def hapus_data_buku_byMenuBar(self):
        current_row = self.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Peringatan", "Tidak ada data yang dipilih")
            return
        
        item_id = self.tableWidget.item(current_row, 0).text() #untuk mengambil ID buku nya

        reply = QMessageBox.question(
            self,
            "Konfirmasi",
            f"Yakin ingin menghapus data dengan ID {item_id} ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            item_id = self.tableWidget.item(current_row, 0).text()

            # Hapus data buku dari database
            conn = sqlite3.connect("data_buku.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM buku WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()

            # Hapus data buku dari tabel GUI
            self.tableWidget.removeRow(current_row)

    #Function menghapus data buku dari tombol (button)
    def hapus_data_buku_byTombol(self):
        current_row = self.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Peringatan", "Tidak ada data yang dipilih")
            return

        item_id = self.tableWidget.item(current_row, 0).text()

        reply = QMessageBox.question(
            self,
            "Konfirmasi",
            f"Yakin ingin menghapus data dengan ID {item_id} ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM buku WHERE id = ?", (item_id,))
            self.conn.commit()
            self.tableWidget.removeRow(current_row)

    #Function untuk edit data buku
    def edit_data_buku(self, row, column):
        if column == 0:
            return  # ID tidak boleh diedit

        item_id = self.tableWidget.item(row, 0).text()
        kolom_nama = ["ID", "Judul", "Penulis", "Tahun", "Kategori", "Tempat Terbit", "Penerbit"]
        kolom_field = ["judul", "penulis", "tahun", "kategori", "tempat", "penerbit"]
        field_db = kolom_field[column - 1]

        nilai_lama = self.tableWidget.item(row, column).text()

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit {kolom_nama[column]}")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Edit {kolom_nama[column]}:"))
        input_edit = QLineEdit(nilai_lama)
        layout.addWidget(input_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            nilai_baru = input_edit.text()

            #Update data buku ke database
            query = f"UPDATE buku SET {field_db} = ? WHERE id = ?"
            self.cursor.execute(query, (nilai_baru, item_id))
            self.conn.commit()

            #Refresh tampilan
            self.tampilkanData()


    #Function untuk ekspor ke CSV
    def ekspor_ke_csv(self):
        #Buka dialog Save File dengan filter *.csv 
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Simpan CSV",
            "",
            "CSV Files (*.csv);;All Files (*)",
            options=options
        )
    
        if filename:
            try:
                with open(filename, mode='w', newline='', encoding='utf-8') as file_csv:
                    writer = csv.writer(file_csv)
                    
                    headers = ["ID", "Judul Buku", "Penulis", "Tahun Terbit", "Kategori", "Tempat Terbit", "Penerbit"]
                    writer.writerow(headers)
                    
                    row_count = self.tableWidget.rowCount()
                    col_count = self.tableWidget.columnCount()
                    
                    for row in range(row_count):
                        row_data = []
                        for col in range(col_count):
                            item = self.tableWidget.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                
                QMessageBox.information(self, "Sukses", "Data berhasil diekspor ke CSV!")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal mengekspor data: {str(e)}")

    #Function untuk membuat clipboard
    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        self.lineEdit_judul.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
