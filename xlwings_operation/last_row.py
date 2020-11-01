
import xlwings as xw

def main(sheet):
    max_col = sheet.range(1, sheet.cells.last_cell.column).end('left').column
    last_row = 2
    for i in range(max_col + 1)[1:]:
        max_row = sheet.range(sheet.cells.last_cell.row, i).end('up').row
        if max_row > last_row:
            last_row = max_row
    return last_row

if __name__ == '__main__':
    main()