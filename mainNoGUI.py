from pyAudioRunner import PyAudioRunner
import xlsxwriter

if __name__ == "__main__":

    PyAudioRunner.run()

    workbook = xlsxwriter.Workbook(name + ".xlsx")
    worksheet = workbook.add_worksheet() 
    worksheet.write("A1", name)
    index = 2
    for tapTime in t.tap_list:
        worksheet.write("A"+str(index), tapTime)
        index += 1
    workbook.close() 