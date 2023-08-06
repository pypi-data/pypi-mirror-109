# -*- coding: utf-8 -*-

import win32com.client
import re
import string
import win32gui
import time

class pyezxl:
    my_web_site = "www.halmoney.com"

    def __init__(self, filename=None):
        # 만약 화일의 경로가 있으면 그 화일을 열도록 한다
        self.xlApp = win32com.client.dynamic.Dispatch('Excel.Application')
        self.xlApp.Visible = 1
        self.filename = filename.lower()

        if self.filename == 'activeworkbook' or self.filename == '':
            # activeworkbook으로 된경우는 현재 활성화된 workbook을 그대로 사용한다
            self.xlBook = self.xlApp.ActiveWorkbook
            if self.xlBook == None:
                # 만약 activework북을 부르면서도 화일이 존재하지 않으면 새로운 workbook을 만드는것이다
                try:
                    self.xlApp.WindowState = -4137
                    self.xlBook = self.xlApp.WorkBooks.Add()
                except:
                    win32gui.MessageBox(0, "There is no Activeworkbook", self.my_web_site, 0)

        elif not (self.filename == 'activeworkbook') and self.filename:
            # 만약 화일이름이 따로 주어지면 그화일을 연다
            try:
                self.xlApp.WindowState = -4137
                self.xlBook = self.xlApp.Workbooks.Open(self.filename)
            except:
                win32gui.MessageBox(0, "Please check file path", self.my_web_site, 0)
        else:
            # 빈것으로 된경우는 새로운 workbook을 하나 열도록 한다
            self.xlApp.WindowState = -4137
            self.xlBook = self.xlApp.WorkBooks.Add()

    def change_char_num(self, input_data):
        # input_data : aa => result : 27
        # 문자를 숫자로 바꿔주는 것
        if input_data.isalpha():
            input_data = input_data.lower()
            reversed_input_data = ''.join(reversed(input_data))
            temp_result = [ord(letter) - 96 for letter in reversed_input_data]
            result = 0
            for one in range(len(temp_result)):
                result = result + pow(26, one) * temp_result[one]
        else:
            result = input_data
        return int(result)

    def change_num_char(self, input_data):
        # input_data : 27 => result : aa
        # 숫자를 문자로 바꿔주는 것
        base_number = int(input_data)
        result_01 = ''
        result = []
        while base_number > 0:
            div = base_number // 26
            mod = base_number % 26
            if mod == 0:
                mod = 26
                div = div - 1
            base_number = div
            result.append(mod)
        for one_data in result:
            result_01 = string.ascii_lowercase[one_data - 1] + result_01
        return result_01

    def change_rgb_int(self, input_data):
        # rgb인 값을 color에서 인식이 가능한 값으로 변경하는 것이다
        result = (int(input_data[2]))*(256**2)+(int(input_data[1]))*256+int(input_data[0])
        return result

    def change_sheet_name(self, sheet_name_old, sheet_name_new):
        # 시트이름을 바꿉니다
        self.xlBook.Worksheets(sheet_name_old).Name = sheet_name_new

    def check_address_value(self, address=""):
        # 어떠한 형태의 주소값이 오더라도 결과값을 [x1, y1, x2, y2]의 형태로 만들어 주는것
        # input_data : [1,2],[1,1,2,3],[$A$1], [$A$1:$B$2], [$1:$7], [$A:$B], [A1]
        # output_data : [1,2],[1,1,2,3],[1,1], [1,1,2,2], [1,0,7.0], [0,1,0,2], [1,1]
        check_string = re.compile(r"([:$a-zA-Z]+)")
        check_range = re.compile(r"([:]+)")
        check_num = re.compile(r"([0-9]+)")

        result_final = []
        result_final_01 = []

        if address == "":
            address = self.read_select_address()
        elif type(address) != type([]):
            address = [address]

        for one_data in address:
            one_data = str(one_data)
            one_data = one_data.replace('$', '')
            result_temp = []
            result_final_01 = []
            data_type = {"range": "no", "num_only": "no", "string_only": "no"}
            # 어떤 형태의 주소인지 확인한다

            if check_range.findall(one_data):
                data_type["range"] = "yes"
            if check_num.findall(one_data.split(":")[0]):
                data_type["num_only"] = "yes"
            if check_string.findall(one_data.split(":")[0]):
                data_type["string_only"] = "yes"

            if data_type["range"] == "no" and data_type["num_only"] == "yes" and data_type["string_only"] == "no":
                # [1, 2], [1, 1, 2, 3] => 이런형태이므로 그대로 값을 넣어준다
                result_temp.append(one_data)

            if data_type["range"] == "no" and data_type["num_only"] == "no" and data_type["string_only"] == "yes":
                # [$A$1], [A1] => 이런형태
                temp_value = self.split_eng_num(one_data)
                temp_value1 = self.change_char_num(temp_value[0])
                result_temp.append(int(temp_value[1]))
                result_temp.append(int(temp_value1))

            if data_type["range"] == "no" and data_type["num_only"] == "yes" and data_type["string_only"] == "yes":
                # [$A$1], [A1] => 이런형태
                temp_value = self.split_eng_num(one_data)
                temp_value1 = self.change_char_num(temp_value[0])
                result_temp.append(int(temp_value[1]))
                result_temp.append(int(temp_value1))

            if data_type["range"] == "yes" and data_type["num_only"] == "yes" and data_type["string_only"] == "yes":
                # [$A$1:$B$2] => 이런형태
                for data_001 in one_data.split(":"):
                    temp_value = self.split_eng_num(data_001)
                    temp_value1 = self.change_char_num(temp_value[0])
                    result_temp.append(int(temp_value[1]))
                    result_temp.append(int(temp_value1))

            if data_type["range"] == "yes" and data_type["num_only"] == "no" and data_type["string_only"] == "yes":
                # [$A:$B] => 이런형태
                for data_001 in one_data.split(":"):
                    result_temp.append(int(0))
                    temp_value = self.change_char_num(data_001)
                    result_temp.append(int(temp_value))

            if data_type["range"] == "yes" and data_type["num_only"] == "yes" and data_type["string_only"] == "no":
                # [$1:$7] => 이런형태
                aaa = one_data.split(":")
                for data_001 in aaa:
                    result_temp.append(int(data_001))
                    result_temp.append(int(0))

            result_final.extend(result_temp)
        if len(result_final) == 2: result_final_01 = [int(result_final[0]), int(result_final[1]), int(result_final[0]), int(result_final[1])]
        if len(result_final) == 4: result_final_01 = [int(result_final[0]), int(result_final[1]), int(result_final[2]), int(result_final[3])]

        #혹시 입력한 자료가 [1,2,3,4]의 형태가 아닌 [3,4,1,2]로 되어잇을때 정렬을 다시하는것이다
        temp1 = [result_final_01[0], result_final_01[2]]
        temp1.sort()

        temp2 = [result_final_01[1], result_final_01[3]]
        temp2.sort()

        result_final_02 = [temp1[0], temp2[0], temp1[1], temp2[1]]
        return result_final_02

    def check_range_address(self, xyxy=""):
        #비슷하게 추측이 가능한 함수를 하나더 만든 것이다
        return self.check_address_value(xyxy)

    def check_sheet_name(self, sheet_name=""):
        # sheet이름을 확인해서 돌려준다.
        # 아무것도 없으면 현재 활성화된 activesheet를 돌려준다
        # 시트이름으로 확인하여 없다면, 일단 입력받은 시트이름으로 새로운 시트를 만든다
        # read와 check의 의미 차이는 check는 어떤 조건에서 2개이상의 다른 값을 보여줄때이며
        # read는 조건문등의 구문이 없이 단순히 값을 읽어올때 사용한다
        if str(sheet_name).lower() == "activesheet" or sheet_name == "":
            sheet = self.xlApp.ActiveSheet
        elif sheet_name in self.read_sheet_name():
            sheet = self.xlBook.Worksheets(sheet_name)
        else:
            self.insert_workbook_sheet()
            old_sheet_name = self.read_activesheet_name()
            self.change_sheet_name(old_sheet_name, sheet_name)
            sheet = self.xlBook.Worksheets(sheet_name)
        return sheet

    def return_sheet_object(self, sheet_name=""):
        if str(sheet_name).lower() == "activesheet" or sheet_name == "":
            sheet = self.xlApp.ActiveSheet
        elif sheet_name in self.read_sheet_name():
            sheet = self.xlBook.Worksheets(sheet_name)
        else:
            self.insert_workbook_sheet()
            old_sheet_name = self.read_activesheet_name()
            self.change_sheet_name(old_sheet_name, sheet_name)
            sheet = self.xlBook.Worksheets(sheet_name)
        return sheet


    def check_x_empty(self, sheet_name, x):
        # 열전체가 빈 것인지 확인해서 돌려준다
        # 전체가 비었을때는 0을 돌려준다
        x_check = self.check_xy_address(x)
        x_new = self.change_char_num(str(x_check[0]))
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlApp.WorksheetFunction.CountA(sheet.Rows(int(x_new)).EntireRow)
        return result

    def check_xy_address(self, input_data):
        # 입력의 형태 : 3, [3], [2,3], D, [A,D], [D]
        # 출력 : [3,3], [2,3], [4,4,], [1,4]
        # x나 y의 하나를 확인할때 입력을 잘못하는 경우를 방지하기위해 사용
        result = []
        if type([]) == type(input_data):
            if len(input_data) == 1:
                input_data[0] = self.change_char_num(str(input_data[0]))
                result = [input_data[0], input_data[0]]
            if len(input_data) == 2:
                input_data[0] = self.change_char_num(str(input_data[0]))
                input_data[1] = self.change_char_num(str(input_data[1]))
                result = input_data
        else:
            input_data = str(input_data)
            if re.match('[a-zA-Z0-9]', input_data):
                if re.match('[a-zA-Z]', input_data):
                    input_data = self.change_char_num(input_data)
                    result = [input_data, input_data]
                else:
                    result = [input_data, input_data]
        return result

    def check_y_empty(self, sheet_name, y):
        # 세로열 전체가 빈 것인지 확인해서 돌려준다
        # 전체가 비었을때는 0을 돌려준다
        y_check = self.check_xy_address(y)
        y_new = self.change_char_num(str(y_check[0]))
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlApp.WorksheetFunction.CountA(sheet.Columns(y_new).EntireColumn)
        return result

    def copy_x_line(self, sheet_name1, sheet_name2, xx0, xx1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        xx0_1, xx0_2 = self.check_xy_address(xx0)
        xx1_1, xx1_2 = self.check_xy_address(xx1)

        xx0_1 = self.change_char_num(xx0_1)
        xx0_2 = self.change_char_num(xx0_2)
        xx1_1 = self.change_char_num(xx1_1)
        xx1_2 = self.change_char_num(xx1_2)

        sheet1.Select()
        sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Select()
        sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Copy()
        sheet2.Select()
        sheet2.Rows(str(xx1_1) + ':' + str(xx1_2)).Select()
        sheet2.Paste()

    def copy_y_line(self, sheet_name1, sheet_name2, yy0, yy1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        yy0_1, yy0_2 = self.check_xy_address(yy0)
        yy1_1, yy1_2 = self.check_xy_address(yy1)

        yy0_1 = self.change_num_char(yy0_1)
        yy0_2 = self.change_num_char(yy0_2)
        yy1_1 = self.change_num_char(yy1_1)
        yy1_2 = self.change_num_char(yy1_2)
        #print(yy0_1, yy0_2, yy1_1, yy1_2)

        sheet1.Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Copy()
        sheet2.Select()
        sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Select()
        sheet2.Paste()

    def cut_x_line(self, sheet_name1, sheet_name2, xx0, xx1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        xx0_1, xx0_2 = self.check_xy_address(xx0)
        xx1_1, xx1_2 = self.check_xy_address(xx1)

        xx0_1 = self.change_char_num(xx0_1)
        xx0_2 = self.change_char_num(xx0_2)
        xx1_1 = self.change_char_num(xx1_1)
        xx1_2 = self.change_char_num(xx1_2)

        sheet1.Select()
        sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Select()
        sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Copy()
        sheet2.Select()
        sheet2.Rows(str(xx1_1) + ':' + str(xx1_2)).Select()
        sheet2.Rows(str(xx1_1) + ':' + str(xx1_2)).Insert()

        if sheet1 == sheet2:
            if xx0_1 <= xx1_1:
                sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Delete()
            else:
                new_xx0_1 = self.change_num_char(xx0_1 + xx1_2 - xx1_1)
                new_xx0_2 = self.change_num_char(xx0_2 + xx1_2 - xx1_1)
                sheet1.Rows(str(new_xx0_1) + ':' + str(new_xx0_2)).Delete()
        else:
            sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Delete()

    def cut_y_line(self, sheet_name1, sheet_name2, yy0, yy1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        yy0_1, yy0_2 = self.check_xy_address(yy0)
        yy1_1, yy1_2 = self.check_xy_address(yy1)

        yy0_1 = self.change_num_char(yy0_1)
        yy0_2 = self.change_num_char(yy0_2)
        yy1_1 = self.change_num_char(yy1_1)
        yy1_2 = self.change_num_char(yy1_2)

        sheet1.Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Cut()
        sheet2.Select()
        sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Select()
        sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Insert()

    def cut_y_line_test(self, sheet_name1, sheet_name2, yy0, yy1):
        # 세로의 값을 이동시킵니다
        sheet1 = self.check_sheet_name(sheet_name1)
        sheet2 = self.check_sheet_name(sheet_name2)

        yy0_1, yy0_2 = self.check_xy_address(yy0)
        yy1_1, yy1_2 = self.check_xy_address(yy1)

        yy0_1 = self.change_num_char(yy0_1)
        yy0_2 = self.change_num_char(yy0_2)
        yy1_1 = self.change_num_char(yy1_1)
        yy1_2 = self.change_num_char(yy1_2)

        # 똑같은 갯수를 삽입한후에 복사하고
        sheet1.Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Select()
        sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Cut()
        sheet2.Select()
        sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Select()
        sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Insert()

    def delete_range_color(self, sheet_name, xyxy):
        # 영역의 모든 색을 지운다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.Pattern = -4142
        my_range.Interior.TintAndShade = 0
        my_range.Interior.PatternTintAndShade = 0

    def delete_range_line(self, sheet_name, xyxy):
        # 영역에 선의색을 다 없애는것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Borders.LineStyle = 0

    def delete_range_link(self, sheet_name, xyxy):
        # 영역의 모든 색을 지운다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Hyperlinks.Delete()

    def delete_range_samevalue(self, sheet_name, xyxy):
        # 선택 영역중 2번이상 반복되는 값은 지우는 것이다
        temp_result = []
        select_range = self.read_select_address()
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                temp_data = self.read_cell_value(sheet, [x, y])
                if temp_data in temp_result:
                    self.write_cell_value(sheet, [x, y], "")
                else:
                    temp_result.append(temp_data)

    def delete_range_value(self, sheet_name, xyxy):
        # 선택한영역의 모든 값을 지우는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.ClearContents()

    def delete_range_x(self, sheet_name, xx):
        # 가로 한줄삭제하기
        # 입력형태는 2, [2,3]의 두가지가 가능하다
        sheet = self.check_sheet_name(sheet_name)
        new_xx = self.check_xy_address(xx)
        sheet.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).Delete(-4121)

    def delete_range_xx(self, sheet_name, xx):
        self.delete_range_x(sheet_name, xx)

    def delete_range_y(self, sheet_name, yy):
        # 세로 한줄삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_yy = self.check_xy_address(yy)
        sheet.Columns(str(new_yy[0]) + ':' + str(new_yy[1])).Delete()

    def delete_range_yy(self, sheet_name, yy):
        self.delete_range_y(sheet_name, yy)

    def delete_sheet_rangename(self, sheet_name, range_name):
        # 입력한 이름을 삭제한다
        # name은 workbook으로 되지만 동일하게 하기위하여 sheet_name을 넣은 것이다
        sheet = self.check_sheet_name(sheet_name)
        result = self.xlBook.Names(range_name).Delete()
        return result

    def delete_range_name(self, sheet_name, range_name):
        self.delete_sheet_rangename(sheet_name, range_name)
        # 예전 코드를 위해 남겨놓음

    def delete_sheet_drawing(self, sheet_name=""):
        # 특정 시트안의 그림을 다 지우는 것이다
        sheet = self.check_sheet_name(sheet_name)
        for aa in range(sheet.Shapes.Count, 0, -1):
            # Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
            sheet.Shapes(aa).Delete()
        return

    def delete_sheet_value(self, sheet_name):
        # 시트의 모든 값을 삭제한다
        sheet = self.check_sheet_name(sheet_name)
        sheet.Cells.ClearContents()

    def delete_workbook_sheet(self, sheet_name=""):
        # 시트하나 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        self.xlApp.DisplayAlerts = False
        sheet.Delete()
        self.xlApp.DisplayAlerts = True

    def delete_x_line(self, sheet_name, xx):
        # 한줄삭제하기
        self.delete_range_x(sheet_name, xx)

    def delete_line_x(self, sheet_name, xx):
        # 한줄삭제하기
        self.delete_range_x(sheet_name, xx)

    def delete_x_value(self, sheet_name, xx):
        # 한줄값만 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_xx = self.check_xy_address(xx)
        sheet.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).ClearContents()

    def delete_y_line(self, sheet_name, yy):
        # 한줄삭제하기
        self.delete_range_y(sheet_name, yy)

    def delete_line_y(self, sheet_name, yy):
        # 한줄삭제하기
        self.delete_range_y(sheet_name, yy)

    def delete_y_value(self, sheet_name, yy):
        # 한줄값만 삭제하기
        sheet = self.check_sheet_name(sheet_name)
        new_yy = self.check_xy_address(yy)
        sheet.Columns(str(new_yy[0]) + ':' + str(new_yy[1])).ClearContents()

    def dump_range_value(self, sheet_name, xyxy, input_datas):
        # 영역에 값을 한번에 써 넣는 것이다
        # 차음시작하는 셀을 기준으로 알아서 맞추는 기능이다
        # 입력값과 영역이 맞지 않으면 입력값의 갯수를 더 우선함
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        y_len = len(input_datas[0])
        x_len = len(input_datas)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x1+x_len-1, y1+y_len-1)).value = input_datas

    def dump_newsheet_value(self, input_datas):
        # 새로운 시트에 값을 한번에 써 넣는 것이다
        sheet = self.insert_workbook_sheet()
        sheet.Range("A1").value = input_datas

    def insert_range_button(self, sheet_name, xyxy, macro, title):
        # 버튼을 만들어서 그 버튼에 매크로를 연결하는 것이다
        # 매크로와 같은것을 특정한 버튼에 연결하여 만드는것을 보여주기위한 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        new_btn = sheet.Buttons()
        new_btn.Add(x1, x2, y1, y2)
        new_btn.OnAction = macro
        new_btn.Text = title

    def insert_range_picture(self, sheet_name="", file_name=""):
        # 사진을 입력하는 것
        sheet = self.check_sheet_name(sheet_name)
        sheet.Shapes.AddPicture(file_name, 0, 1, 541.5, 92.25, 192.75, 180)

    def insert_workbook_sheet(self, sheet_name=""):
        # 시트하나 추가하기
            self.xlBook.Worksheets.Add()

    def insert_x_line(self, sheet_name, x):
        # 가로열을 한줄삽입하기
        sheet = self.check_sheet_name(sheet_name)
        x_new = self.check_xy_address(x)
        x_no = self.change_char_num(str(x_new[0]))
        sheet.Range(str(x_no) + ':' + str(x_no)).Insert()

    def insert_line_x(self, sheet_name, x):
        self.insert_x_line(sheet_name, x)
        #예전 코드를 위해 남겨놓음

    def insert_y_line(self, sheet_name, num):
        # 세로행을 한줄삽입하기
        sheet = self.check_sheet_name(sheet_name)
        num_r1 = self.change_num_char(num)
        sheet.Columns(str(num_r1) + ':' + str(num_r1)).Insert()

    def insert_line_y(self, sheet_name, num):
        self.insert_y_line(sheet_name, num)
        #예전 코드를 위해 남겨놓음

    def intersect_range1_range2(self, rng1, rng2):
        # 두개의 영역에서 교차하는 구간을 돌려준다
        # 만약 교차하는게 없으면 ""을 돌려준다
        range_1 = self.check_range_address(rng1)
        range_2 = self.check_range_address(rng2)

        x11, y11, x12, y12 = range_1
        x21, y21, x22, y22 = range_2

        if x11 == 0:
           x11 = 1
           x12 = 1048576
        if x21 == 0:
           x21 = 1
           x22 = 1048576
        if y11 == 0:
           y11 = 1
           y12 = 16384
        if y21 == 0:
           y21 = 1
           y22 = 16384

        new_range_x = [x11, x21, x12, x22]
        new_range_y = [y11, y21, y12, y22]

        new_range_x.sort()
        new_range_y.sort()

        if x11 <= new_range_x[1] and x12 >= new_range_x[2] and y11 <= new_range_y[1] and y12 >= new_range_y[1]:
            result = [new_range_x[1], new_range_y[1], new_range_x[2], new_range_y[2]]
        else:
            result = "교차점없음"
        return result

    def move_activecell_bottom(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4121).Select()
        return "ok"

    def move_activecell_left(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4159).Select()
        return "ok"

    def move_activecell_right(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4161).Select()
        return "ok"

    def move_activecell_top(self, sheet_name="", xyxy=""):
        # 선택한 위치에서 끝부분으로 이동하는것
        # xlDown  : - 4121,  xlToLeft : - 4159, xlToRight  : - 4161, xlUp : - 4162
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).End(- 4162).Select()
        return "ok"

    def move_x_line(self, sheet_name1, sheet_name2, xx0, xx1):
        self.cut_x_line(sheet_name1, sheet_name2, xx0, xx1)

    def move_y_line(self, sheet_name1, sheet_name2, yy0, yy1):
        self.cut_y_line(sheet_name1, sheet_name2, yy0, yy1)

    def read_activesheet_name(self):
        # 현재의 엑셀중에서 활성화된 시트의 이름을 돌려준다
        return self.xlApp.ActiveSheet.Name

    def read_activecell_address(self):
        xy = self.check_address_value(self.xlApp.ActiveCell.Address)
        return xy

    def read_activecell_value(self):
        # 현재 셀 하나의 값을 돌려준다
        # 예전 함수에서 약간 변형한것이다
        value = self.xlApp.ActiveCell.Value
        return value

    def read_activecell_range(self):
        # 돌려주는 값 [x, y]
        xyxy = self.read_activecell_address()
        return xyxy

    def read_cell_value(self, sheet_name, xy):
        # 값을 일정한 영역에서 갖고온다
        # 만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        result = sheet.Cells(x1, y1).value
        return result

    def read_continousrange_value(self, sheet_name, xyxy):
        # 현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다
        # **************다시한번 봐야할 코드이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)

        bottom = x1  # 아래의 행을 찾는다
        while sheet.Cells(bottom, y1).Value not in [None, '']:
            bottom = bottom + 1
        right = y2  # 오른쪽 열
        while sheet.Cells(x2, right).Value not in [None, '']:
            right = right + 1
        return sheet.Range(sheet.Cells(x1, y1), sheet.Cells(bottom, right)).Value

    def read_messagebox_value(self, text_01="www.halmoney.com"):
        # 메세지 박스로 원하는 겂을 알려주는 것이다
        result = self.xlApp.InputBox(text_01)
        return result

    def read_currentregion_address(self, xy=""):
        # 이것은 현재의 셀에서 공백과 공백열로 둘러싸인 활성셀영역을 돌려준다
        if xy == "":
            result = self.check_address_value(self.xlApp.ActiveCell.CurrentRegion.Address)
        else:
            sheet = self.check_sheet_name("")
            result = self.check_address_value(sheet.Cells(xy[0], xy[1]).CurrentRegion.Address)
        return result

    def read_range_unique(self, sheet_name, xyxy):
        # 선택한 자료중에서 고유한 자료만을 골라내는 것이다
        # 자료중에서 고유한것을 찾아내서, 선택영역에 다시 쓴다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        temp_datas = self.read_range_value(sheet, xyxy)
        temp_result = []
        for one_list_data in temp_datas:
            for one_data in one_list_data:
                if one_data in temp_result or type(one_data) == type(None):
                    pass
                else:
                    temp_result.append(one_data)
        self.delete_range_value(sheet, xyxy)

        for num in range(len(temp_result)):
            mox, namuji = divmod(num, x2 - x1 + 1)
            self.write_cell_value(sheet, [x1 + namuji, y1 + mox], temp_result[num])

    def read_range_value(self, sheet_name, xyxy):
        # 값을 일정한 영역에서 갖고온다
        # 만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        temp_result = my_range.Value
        result = []
        if 1 < len(temp_result):
            for one_data in temp_result:
                result.append(list(one_data))
        else:
            result = temp_result
        return result

    def read_rangename_address(self, sheet_name, xyxy_name):
        sheet = self.check_sheet_name(sheet_name)
        temp = sheet.Range(xyxy_name).Address
        result = self.check_address_value(temp)
        return result

    def read_select_address(self):
        # 현재선택된 영역의 주소값을 돌려준다
        result = ""
        temp_address = self.xlApp.Selection.Address
        print(temp_address)
        temp_list = temp_address.split(",")
        if len(temp_list) == 1:
            result = self.check_address_value(self.xlApp.Selection.Address)
        if len(temp_list) > 1:
            result = []
            for one_address in temp_list:
                result.append(self.check_address_value(one_address))
        return result

    def read_range_select(self):
        temp_address = self.xlApp.Selection.Address
        result = self.check_address_value(temp_address)
        return result

    def read_sheet_count(self):
        # 시트의 갯수를 돌려준다
        return self.xlBook.Worksheets.Count

    def read_sheet_name(self):
        # 현재 워크북의 모든 시트알아내기
        temp_list = []
        for var_02 in range(1, self.read_sheet_count() + 1):
            temp_list.append(self.xlBook.Worksheets(var_02).Name)
        return temp_list

    def read_usedrange_address(self, sheet_name=""):
        # 이것은 usedrange를 돌려주는 것이다. 값은 리스트이며 처음은
        # usedrange의 시작셀 ,두번째는 마지막셀값이며 세번째는 전체영역을 돌려주는 것이다
        sheet = self.check_sheet_name(sheet_name)
        result = self.check_address_value(sheet.usedrange.address)
        return result

    def read_workbook_rangename(self):
        # 현재 시트의 이름을 전부 돌려준다
        # [번호, 영역이름, 영역주소]
        names_count = self.xlBook.Names.Count
        result = []
        if names_count > 0:
            for aaa in range(1, names_count + 1):
                name_name = self.xlBook.Names(aaa).Name
                name_range = self.xlBook.Names(aaa)
                result.append([aaa, str(name_name), str(name_range)])
        return result

    def read_workbook_rangenames(self):
        # 현재 워크북의 모든 시트알아내기
        temp_list = []
        for var_02 in range(1, self.read_sheet_count() + 1):
            temp_list.append(self.xlBook.Worksheets(var_02).Name)
        return temp_list

    def read_workbook_fullname(self):
        # application의 이름과 전체경로를 돌려준다
        return self.xlBook.FullName

    def read_workbook_name(self):
        # application의 이름을 돌려준다
        return self.xlBook.Name

    def read_workbook_path(self):
        # application의 경로를 돌려준다
        return self.xlBook.Path

    def read_workbook_username(self):
        #사용자 이름을 읽어온다
        return self.xlApp.Username

    def read_x_value(self, sheet_name, x):
        # 한 가로행의 전체값을 갖고온다
        sheet = self.check_sheet_name(sheet_name)
        x_check = self.change_char_num(x)
        result = sheet.Cells(x_check, 1).EntireRow.Value
        return result

    def set_cell_bold(self, sheet_name, xyxy):
        # 셀안의 값을 진하게 만든다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Font.Bold = True

    def set_cell_color(self, sheet_name, xy, input_data):
        # 셀 하나에 색을 입힌다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.Color = input_data

    def read_cell_color(self, sheet_name, xy):
        # 셀 하나에 색을 입힌다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        result = my_range.Interior.Color
        return result

    def set_cell_picture(self, sheet_name, xy, full_path):
        # 사진을 불러오는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        sheet.Cells(x1, y1).Select()
        aaa = sheet.Pictures
        aaa.Insert(full_path).Select()

    def set_cell_select(self, sheet_name, xyxy):
        #영역을 선택한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Cells(x1, y1).Select()

    def set_range_autofilter(self, sheet_name, row1, row2=None):
        # 엑셀의 자동필터 기능을 추가한 것입니다
        sheet = self.check_sheet_name(sheet_name)
        if row2 == None:
            row2 = row1
        a = str(row1) + ':' + str(row2)
        sheet.Rows(a).Select()
        sheet.Range(a).AutoFilter(1)

    def set_range_clear(self, sheet_name, xyxy):
        # clear기능을 한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.ClearContents()

    def set_range_color(self, sheet_name, xyxy, input_data):
        # 영역에 색깔을 입힌다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Interior.Color = input_data

    def set_range_font(self, sheet_name, xyxy, font):
        # 영역에 글씨체를 설정한다
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.font.Name = font

    def set_range_fontcolor(self, sheet_name, xyxy, font_name):
        # 영역에 글씨체를 설정한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Font.Color = font_name

    def set_range_fontsize(self, sheet_name, xyxy, input_data):
        # 영역에 글씨크기를 설정한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.font.Size = input_data

    def set_range_formula(self, sheet_name, xyxy, input_data):
        #영역에 식을 할당하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Formula = input_data

    def set_range_line(self, sheet_name, xyxy, line_value=""):
        # 안쪽의 선들지정
        # [선의위치, 라인스타일, 굵기, 색깔]
        # 입력예 : [7,1,2,1]
        # 선의위치 (5-대각선 오른쪽, 6-왼쪽대각선, 7:왼쪽, 8;위쪽, 9:아래쪽, 10:오른쪽, 11:안쪽세로, 12:안쪽가로)
        # 라인스타일 (1-실선, 2-점선, 3-가는점선, 6-굵은실선,
        # 굵기 (0-이중, 1-얇게, 2-굵게)
        # 색깔 (0-검정, 1-검정3-빨강),

        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)

        if line_value == "":
            for one in [7,8,9,10]:
                my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Borders(one)
                my_range.Color = 1
                my_range.Weight = 2
                my_range.LineStyle = 1
        else:
            my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Borders(line_value[0])
            print(line_value[0],line_value[1],line_value[2],line_value[3])
            my_range.Color = int(line_value[3])
            my_range.Weight = int(line_value[2])
            #여기에서 linestyle을 제일 나중에 해야지 잘적용이 되며, 만약 다른것을 나중에 하면 점선으로만 나온다
            my_range.LineStyle = int(line_value[1])

    def set_range_merge(self, sheet_name, xyxy):
        # 셀들을 합하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        if x1 == x2:
            sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2)).Merge(0)
        else:
            for a in xyxy(y2 - y1 + 1):
                sheet.Range(sheet.Cells(y1 + a, x1), sheet.Cells(y1 + a, x2)).Merge(0)

    def set_range_nocolor(self, sheet_name, xyxy):
        # 영역에 선의색을 다 없애는것
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = xyxy
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range .Interior.Pattern = 0
        my_range .Interior.PatternTintAndShade = 0

    def set_range_numberformat(self, sheet_name, xyxy, numberformat):
        # 영역에 숫자형식을 지정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.NumberFormat = numberformat

    def set_range_rangename(self, sheet_name, xyxy, name):
        # 영역에 이름으로 설정하는 기능
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range  = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        self.xlBook.Names.Add(name, my_range)

    def set_range_rgbcolor(self, sheet_name, xyxy, input_data):
        # 영역에 색깔을 입힌다
        # 엑셀에서의 색깔의 번호는 아래의 공식처럼 만들어 진다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        rgb_to_int = (int(input_data[2]))*(256**2)+(int(input_data[1]))*256+int(input_data[0])
        my_range.Interior.Color = rgb_to_int

    def set_range_select(self, sheet_name, xyxy):
        #영역을 선택한다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Select()

    def set_range_unmerge(self, sheet_name, xyxy):
        #병합된 것을 푸는 것이다
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.Range(xyxy).UnMerge()

    def set_range_wrap(self, sheet_name, xyxy, input_data):
        # 셀의 줄바꿈을 설정할때 사용한다
        # 만약 status를 false로 하면 줄바꿈이 실행되지 않는다.
        sheet = self.check_sheet_name(sheet_name)
        sheet.Range(xyxy).WrapText = input_data

    def set_sheet_fullscreen(self, fullscreen=1):
        # 전체화면으로 보기
        self.xlApp.DisplayFullScreen = fullscreen

    def set_sheet_hide(self, sheet_name, hide=0):
        # 시트 숨기기
        sheet = self.check_sheet_name(sheet_name)
        sheet.Visible = hide

    def set_sheet_gridline(self):
        # 그리드 라인을 계속 바꾼다
        if self.xlApp.ActiveWindow.DisplayGridlines == 0:
            self.xlApp.ActiveWindow.DisplayGridlines = 1
        else:
            self.xlApp.ActiveWindow.DisplayGridlines = 0

    def set_sheet_preview(self, sheet_name=""):
        # 미리보기기능입니다
        sheet = self.check_sheet_name(sheet_name)
        sheet.PrintPreview()

    def set_sheet_lock(self, sheet_name="", password="1234"):
        # 시트 잠그기
        sheet = self.check_sheet_name(sheet_name)
        sheet.protect(password)

    def set_sheet_unlock(self, sheet_name="", password="1234"):
        # 시트 잠그기 해제
        sheet = self.check_sheet_name(sheet_name)
        sheet.Unprotect(password)

    def set_sheet_visible(self, input_data=0):
        # 실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
        self.xlApp.Visible = input_data

    def set_workbook_close(self):
        # 현재는 close를 시키면 엑셀워크북만이 아니라 엑셀자체도 종료 시킵니다
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    def set_workbook_fullscreen(self, fullscreen=1):
        # 전체화면으로 보기
        self.xlApp.DisplayFullScreen = fullscreen

    def set_workbook_hide(self):
        # 실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
        # visible로 통합
        self.xlApp.Visible = 0

    def set_workbook_save(self, newfilename=None):
        # 별도의 지정이 없으면 기존의 화일이름으로 저장합니다
        if newfilename:
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def set_wrap_on(self, sheet_name, xyxy, input_data):
        # 셀의 줄바꿈을 설정할때 사용한다
        # 만약 status를 false로 하면 줄바꿈이 실행되지 않는다.
        x1, y1, x2, y2 = self.check_address_value(xyxy)
        sheet = self.check_sheet_name(sheet_name)
        my_range = sheet.Range(sheet.Cells(x1, y1), sheet.Cells(x2, y2))
        my_range.WrapText = input_data

    def set_x_length(self, sheet_name, xx, height=13.5):
        # 가로열의 높이를 설정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        new_xx = self.check_xy_address(xx)
        my_range = sheet.Range(sheet.Cells(new_xx[0], 1), sheet.Cells(new_xx[1], 5))
        my_range.Select()
        my_range.EntireRow.RowHeight = height

    def set_y_length(self, sheet_name, yy, length=8.38):
        # 열이나 행의 넓이를 조절한다
        # 엑셀은 기본적으로 넓이는 8.38 로, 높이는 13.5로 되어있읍니다
        sheet = self.check_sheet_name(sheet_name)
        new_yy = self.check_xy_address(yy)
        my_range = sheet.Range(sheet.Cells(1, new_yy[0]), sheet.Cells(1, new_yy[1]))
        my_range.EntireColumn.ColumnWidth = length

    def set_y_numberproperty(self, sheet_name, y_old, style):
        # 각 열을 기준으로 셀의 속성을 설정하는 것이다
        sheet = self.check_sheet_name(sheet_name)
        y_new = self.check_xy_address(y_old)
        y = self.change_char_num(y_new)
        if style == 1:  # 날짜의 설정
            sheet.Columns(y).NumberFormatLocal = "mm/dd/yy"
        elif style == 2:  # 숫자의 설정
            sheet.Columns(y).NumberFormatLocal = "_-* #,##0.00_-;-* #,##0.00_-;_-* '-'_-;_-@_-"
        elif style == 3:  # 문자의 설정
            sheet.Columns(y).NumberFormatLocal = "@"

    def show_messagebox_value(self, input_data, web="www.halmoney.com"):
        # 메세지박스를 이용하여 원하는 내용을 보여준다
        win32gui.MessageBox(0, input_data, web, 0)

    def sort_datas_on(self, input_datas):
        # aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
        # 정렬하는 방법입니다
        result = []
        for one_data in input_datas:
            for one in one_data:
                result.append(one.sort())
        return result

    def split_eng_num(self, data):
        # 단어중에 나와있는 숫자, 영어를 분리하는기능
        re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
        result = re_compile.findall(data)
        new_result = []
        for dim1_data in result:
            for dim2_data in dim1_data:
                new_result.append(dim2_data)
        return new_result

    def swap(self, a, b):
        #a,b를 바꾸는 함수이다
        t = a
        a = b
        b = t
        return [a, b]

    def swap_list_data(self, input_data):
        # input_data : [a, b, c, d]
        # result : [b, a, d, c]
        # 두개의 자료들에 대해서만 자리를 바꾸는 것이다
        result = []
        for one_data in range(int(len(input_data) / 2)):
            result.append(input_data[one_data * 2 + 1])
            result.append(input_data[one_data * 2])
        return result

    def write_cell_value(self, sheet_name, xy, value):
        # 값을 셀에 넣는다. (사용법) write_cell(시트이름, 행번호, 열번호, 넣을값)
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xy)
        sheet.Cells(x1, y1).Value = value

    def write_range_list(self, sheet_name, xyxy, list_datas):
        # 2차원 리스트로 된 값을 영역에 쓰는 것이다
        self.write_range_value(sheet_name, xyxy, list_datas)

    def write_range_value(self, sheet_name, xyxy, input_datas):
        # 영역에 값을 써 넣는 것이다
        # 이것은 각셀을 하나씩 쓰는 것이다
        # 입력값과 영역이 맞지 않으면 입력값의 갯수를 더 우선함
        sheet = self.check_sheet_name(sheet_name)
        x1, y1, x2, y2 = self.check_address_value(xyxy)

        for x in range(len(input_datas)):
            for y in range(len(input_datas[x])):
                sheet.Range(sheet.Cells(x1+x, y1+y), sheet.Cells(x1+x, y1+y)).value = input_datas[x][y]

    def fun_trim(self, input_data):
        # 함수중 trim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
        aaa = self.xlApp.WorksheetFunction.Trim(input_data)
        return aaa

    def fun_ltrim(self, input_data):
        # 함수중 ltrim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
        aaa = self.xlApp.WorksheetFunction.LTrim(input_data)
        return aaa

    def fun_rtrim(self, input_data):
        # 함수중 rtrim을 사용하는 것이며 엑셀 함수의 사용을 보여주기 위하여 만든 것이다
        aaa = self.xlApp.WorksheetFunction.RTrim(input_data)
        return aaa

    def read_time_day(self, time_char=""):
        # 일 -----> ['05', '095']
        if time_char == "":
            time_char = time.localtime(time.time())
        return [time.strftime('%d', time_char), time.strftime('%j', time_char)]

    def read_time_hour(self, time_char=""):
        # 시 -----> ['10', '22', 'PM']
        if time_char == "":
            time_char = time.localtime(time.time())
        return [time.strftime('%I', time_char), time.strftime('%H', time_char), time.strftime('%P', time_char)]

    def read_time_minute(self, time_char=""):
        # 분 -----> ['07']
        if time_char == "":
            time_char = time.localtime(time.time())
        return [time.strftime('%M', time_char)]

    def read_time_month(self, time_char=""):
        # 월 -----> ['04', 'Apr', 'April']
        if time_char == "":
            time_char = time.localtime(time.time())
        return [time.strftime('%m', time_char), time.strftime('%b', time_char), time.strftime('%B', time_char)]

    def read_time_second(self, time_char=""):
        # 초 -----> ['48']
        if time_char == "":
            time_char = time.localtime(time.time())
        return [time.strftime('%S', time_char)]

    def read_time_today(self, time_char=""):
        # 종합 -----> ['2002-04-05', '04/05/02', '22:07:48', '04/05/02 22:07:48']
        if time_char == "":
            time_char = time.localtime(time.time())
        total_dash = time.strftime('%Y', time_char) + "-" + time.strftime('%m', time_char) + "-" + time.strftime('%d', time_char)
        return [total_dash, time.strftime('%Y', time_char), time.strftime('%m', time_char), time.strftime('%d', time_char)]

    def read_time_now(self, time_char=""):
        if time_char == "":
            time_char = time.localtime(time.time())
        # 종합 -----> ['04/05/02', '22:07:48', '04/05/02 22:07:48','2002-04-05']
        now_dash = time.strftime('%H', time_char) + ":" + time.strftime('%M', time_char) + ":" + time.strftime('%S', time_char)
        return [now_dash, time.strftime('%H', time_char), time.strftime('%M', time_char), time.strftime('%S', time_char)]

    def read_time_week(self, time_char=""):
        if time_char == "":
            time_char = time.localtime(time.time())
        # 주 -----> ['5', '13', 'Fri', 'Friday']
        return [time.strftime('%w', time_char), time.strftime('%W', time_char), time.strftime('%a', time_char), time.strftime('%A', time_char)]

    def read_time_year(self, time_char=""):
        if time_char == "":
            time_char = time.localtime(time.time())
        # 년 -----> ['02', '2002']
        return [time.strftime('%y', time_char), time.strftime('%Y', time_char)]

    def change_time_sec(self, input_data=""):
        #input_data = "14:06:23"
        re_compile = re.compile("\d+")
        result = re_compile.findall(input_data)
        total_sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
        return total_sec

    def change_sec_time(self, input_data=""):
        #input_data = 123456
        step_1 = divmod(int(input_data), 60)
        step_2 = divmod(step_1[0], 60)
        final_result = [step_2[0], step_2[1], step_1[1]]
        return final_result

    def ezre(self, input_data):
        input_data = input_data.replace(" ", "")
        # 아래의 내용중 순서가 중요하므로 함부러 바꾸지 않기를 바랍니다
        # 반복되는 단위를 "번" 과 "개"를 둘다 사용할수있도록 변경하여 만듦

        ezre_dic = {
                ":최소반복]": "]?",
                ":1번이상]": "]+",
                ":0번이상]": "]*",
                ":0-1번]": "]?",
                ":1개이상]": "]+",
                ":0개이상]": "]*",
                ":0-1개]": "]?",
                "또는": "|",
                "[특수문자": "[",
                "[not": "[^",

                "(앞에있음:": "(?=",
                "(뒤에있음:": "(?<=",
                "(앞에없음:": "(?!",
                "(뒤에없음:": "(?<!",

                "[1번이상]": "+",
                "[0번이상]": "*",
                "[0-1번]": "?",
                "[1개이상]": "+",
                "[0개이상]": "*",
                "[0-1개]": "?",
                "[맨앞]": "^",
                "[시작]": "^",
                "[맨뒤]": "$",
                "[맨끝]": "$",
                "[끝]": "$",
                "[최소반복]": "?",

                "[공백]": "\s",
                "[문자]": ".",
                "[숫자]": "0-9",
                "[영어]": "[a-zA-Z]",
                "[영어대문자]": "[A-Z]",
                "[영어소문자]": "[a-z]",
                "[한자]": "一-龥",
                "[일본어]": "[ぁ-ゔァ-ヴー々〆〤]",
                "[한글]": "[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]",

                "[영어&숫자]": "\w",
                "[숫자&영어]": "\w",

                "공백&": "\s",
                "문자&": ".",
                "숫자&": "0-9",
                "영어&": "a-zA-Z",
                "영어대문자&": "A-Z",
                "영어소문자&": "a-z",
                "한자&": "一-龥",
                "일본어&": "[ぁ-ゔァ-ヴー々〆〤]",
                "한글&": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",

                "공백": "\s",
                "숫자": "0-9",
                "영어": "a-zA-Z",
                "영어대문자": "A-Z",
                "영어소문자": "a-z",
                "한자": "一-龥",
                "일본어": "[ぁ-ゔァ-ヴー々〆〤]",
                "한글": "ㄱ-ㅎ|ㅏ-ㅣ|가-힣",
            }

        ezre_list = [
                    "\[최소\d*?번\]",
                     "\[최대\d*?번\]",
                     "\[\d*-\d*?번\]",
                     "\[\d*?번\]",
                     ":최소\d*?번\]",
                     ":최대\d*?번\]",
                     ":\d*-\d*?번\]",
                     ":\d*?번\]",
                    "\[최소\d*?개\]",
                     "\[최대\d*?개\]",
                     "\[\d*-\d*?개\]",
                     "\[\d*?개\]",
                     ":최소\d*?개\]",
                     ":최대\d*?개\]",
                     ":\d*-\d*?개\]",
                     ":\d*?개\]",
                    ]

        changed_data = input_data
        print("변환전 ==> ", changed_data)
        new_str=""
        for num_1 in range(len(ezre_list)):
            compile_1 = re.compile(ezre_list[num_1])
            result_1 = compile_1.findall(changed_data)
            if result_1:
                for num in range(len(result_1)):
                    one = result_1[num]
                    compile_1 = re.compile("\d+")
                    no = compile_1.findall(one)
                    if num_1 == 0:
                        new_str = "{" + str(no[0]) + ",}"
                    elif num_1 == 1:
                        new_str = "{," + str(no[0]) + "}"
                    elif num_1 == 2:
                        new_str = "{" + str(no[0]) + "," + str(no[1]) + "}"
                    elif num_1 == 3:
                        new_str = "{" + str(no[0]) + "}"
                    elif num_1 == 4:
                        new_str = "]{" + str(no[0]) + ",}"
                    elif num_1 == 5:
                        new_str = "]{," + str(no[0]) + "}"
                    elif num_1 == 6:
                        new_str = "]{" + str(no[0]) + "," + str(no[1]) + "}"
                    elif num_1 == 7:
                        new_str = "]{" + str(no[0]) + "}"
                    changed_data = changed_data.replace(result_1[num], new_str)

        for ezre_value in ezre_dic.keys():
            re_value = ezre_dic[ezre_value]
            changed_data = changed_data.replace(ezre_value, re_value)
        print("중간변환 ==> ", changed_data)

        #다시한번 문자열을 더 줄일수있는지 보는 것이다
        min_dic = {
            "a-zA-Z0-9": "\w",
            "0-9a-zA-Z": "\w",
            "0-9": "\d",
        }
        for ezre_value in min_dic.keys():
            re_value = min_dic[ezre_value]
            changed_data = changed_data.replace(ezre_value, re_value)

        print("변환완료 ==> ", changed_data)
        return changed_data

    def run_ezre(self, input_text, input_sql):
        re_com = re.compile(input_sql)
        re_results = re_com.finditer(input_text)
        result = []
        if re_results:
            for one in re_results:
                result.append([one.group(), one.start(), one.end()])
        return result

    def read_shape_name(self, sheet_name="", no=""):
        sheet = self.check_sheet_name(sheet_name)
        return sheet.Shapes(no).Name

    def count_sheet_shape(self, sheet_name=""):
        sheet = self.check_sheet_name(sheet_name)
        return sheet.Shapes.Count

    def delete_sheet_shape(self, sheet_name="", name=""):
        sheet = self.check_sheet_name(sheet_name)
        sheet.Shapes(name).Delete()

    def draw_sheet_line(self, **input):
        enum_line = {
            "msoArrowheadNone": 1, "msoArrowheadTriangle": 2, "msoArrowheadOpen": 3, "msoArrowheadStealth": 4,
            "msoArrowheadDiamond": 5, "msoArrowheadOval": 6,
            "": 1, "<": 2, ">o": 3, ">>": 4, ">": 2, "<>": 5, "o": 6,
            "basic": 1, "none": 1, "triangle": 2, "open": 3, "stealth": 4, "diamond": 5, "oval": 6,
            "msoArrowheadNarrow": 1, "msoArrowheadWidthMedium": 2, "msoArrowheadWide": 3,
            "msoArrowheadShort": 1, "msoArrowheadLengthMedium": 2, "msoArrowheadLong": 3,
            "short": 1, "narrow": 1, "medium": 2, "long": 3, "wide": 3,
            "-1": 1, "0": 2, "1": 3,
            "dash": 4, "dashdot": 5, "dashdotdot": 6, "rounddot": 3, "longdash": 7, "longdashdot": 8, "longdashdotdot": 9,
            "squaredot": 2,
            "-": 4, "-.": 5, "-..": 6, ".": 3, "--": 7, "--.": 8, "--..": 9, "ㅁ": 2,
        }

        base_data = {
            "sheet_name": "",
            "xyxy": [100, 100, 0, 0],
            "color": 10058239,
            "line_style": "-.",
            "thickness": 0.5,
            "transparency": 0,
            "head_style": ">",
            "head_length": "0",
            "head_width": "0",
            "tail_style": ">",
            "tail_length": "0",
            "tail_width": "0",
        }

        # 기본자료에 입력받은값을 update하는것이다
        base_data.update(input)

        sheet = self.check_sheet_name(base_data["sheet_name"])
        set_line = sheet.Shapes.AddLine(base_data["xyxy"][0], base_data["xyxy"][1], base_data["xyxy"][2], base_data["xyxy"][3])
        set_line.Select()
        set_line.Line.ForeColor.RGB = base_data["color"]
        set_line.Line.DashStyle = enum_line[base_data["line_style"]]
        set_line.Line.Weight = base_data["thickness"]
        set_line.Line.Transparency = base_data["transparency"]
        #print(set_line.Name)
        #엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다

        set_line.Line.BeginArrowheadStyle = enum_line[base_data["head_style"]]
        set_line.Line.BeginArrowheadLength = enum_line[base_data["head_length"]]
        set_line.Line.BeginArrowheadWidth = enum_line[base_data["head_width"]]
        set_line.Line.EndArrowheadStyle = enum_line[base_data["tail_style"]]  # 화살표의 머리의 모양
        set_line.Line.EndArrowheadLength = enum_line[base_data["tail_length"]]  # 화살표의 길이
        set_line.Line.EndArrowheadWidth = enum_line[base_data["tail_width"]]  # 화살표의 넓이
        result = set_line.Name
        return result

    def draw_sheet_line_old(self, sheet_name="", xyxy="", width=100, style="", color=""):
        sheet = self.check_sheet_name(sheet_name)
        set_line = sheet.Shapes.AddLine(xyxy[0],xyxy[1],xyxy[2],xyxy[3])
        set_line.Line.ForeColor.RGB = color
        set_line.Line.DashStyle = style

#-----------------------------------------------------------------------------------------------------------------------
    def ezcolor_list(self):
        # 사용가능한 색깔을 보다 쉽게 표현하기위해 만들었다
        # 색은 3가지로 구분 : 테이블등을 만들때 사용하면 좋은 색 : ez1~15번까지
        # 12가지의 색을 기본, 약간 옅은 테이블색칠용, 파스텔톤의 3가지로 구분
        # 각 3종류는 7개의 형태로 구분하여 +, -의 형태로 표현을 하도록 하였다
        manual = """  
                     1. 빨주노초파남보(무지개) 와 검정, 하양, 회색, 분홍, 고동으로 총 12개의 색을 나타낸다
                        white,black,gray,red,orange,yellow,green,blue,indigo,purple,pink,brown
                     2. 모든색은 기본보다 어두운색, 기본색, 기본보다 밝은색의 3가지로 구분하고
                     3. 각 구분된색은 7단계로 세분하여 총 21가지의 색을 정의하였다
                     4. 2차원의 배열로 표시하였고, 1차원에서 3단게로 구분 : 어두운색은 red[-1], 기본색은 red[0], 좀 밝은색은 red[-1]  
                     5. 2차원에서 -3 ~ 3 까지의 7단계로 구분한다 : red[0][-3] ~ red[0][3]
                     6. 색을 없애는것은 nocolor을 이용
                      """
        nocolor = -4142,
        white = [[16777215, 16777215, 16777215, 16777215, 15790320, 16119285, 16448250, ],
                 [16777215, 16777215, 16777215, 16777215, 15790320, 16119285, 16448250, ],
                 [16777215, 16777215, 16777215, 16777215, 15790320, 16119285, 16448250, ]]
        black = [[0, 1052688, 2171169, 3289650, 0, 0, 0, ], [0, 1052688, 2171169, 3289650, 0, 0, 0, ],
                 [3289650, 4342338, 5460819, 6579300, 0, 1052688, 2171169, ]]
        gray = [[8421504, 9211020, 10066329, 10921638, 5855577, 6710886, 7566195, ],
                [12105912, 13355979, 14606046, 15921906, 8355711, 9605778, 10855845, ],
                [14606046, 15066597, 15461355, 15921906, 13355979, 13750737, 14211288, ]]
        red = [[255, 1710847, 3355647, 5066239, 179, 204, 230, ],
               [8356010, 10329794, 12369370, 14408946, 2303075, 4276858, 6316434, ],
               [6384127, 8094207, 9738751, 11449087, 1384703, 3029503, 4739583, ]]
        orange = [[42495, 1748735, 3389439, 5095679, 29875, 33996, 38374, ],
                  [7379402, 9680091, 11980780, 14347005, 411799, 2712488, 5013177, ],
                  [4699135, 6405887, 8046847, 9753599, 37626, 1351423, 3057919, ]]
        yellow = [[65535, 1769471, 3407871, 5111807, 46003, 52428, 59110, ],
                  [383965, 452584, 586739, 720895, 47292, 115655, 249810, ],
                  [9895421, 11533821, 13172478, 14810878, 4979964, 6618364, 8257021, ]]
        green = [[32768, 39424, 45824, 52480, 13312, 19712, 26368, ],
                 [8563101, 10535351, 12507601, 14545387, 2646351, 4618601, 6590851, ],
                 [7855479, 9167499, 10545056, 11857076, 3853882, 5165902, 6543459, ]]
        blue = [[16711680, 16718362, 16724787, 16731469, 11730944, 13369344, 15073280, ],
                [11379581, 12893340, 14407099, 15986395, 6772768, 8286527, 9800286, ],
                [13616814, 14209470, 14867918, 15460574, 11773054, 12365710, 13024158, ]]
        indigo = [[8519755, 10223706, 11862120, 13566071, 3538975, 5177390, 6881340, ],
                  [11113087, 12693150, 14272956, 15853019, 6373412, 7953218, 9533281, ],
                  [8519755, 10223706, 11862120, 13566071, 3538975, 5177390, 6881340, ]]
        purple = [[8388736, 10092698, 11731123, 13435085, 3407924, 5046349, 6750311, ],
                  [10389650, 12101037, 13812425, 15524069, 5321023, 6966874, 8678262, ],
                  [11902643, 12627134, 13351882, 14076373, 9728913, 10453404, 11178152, ]]
        pink = [[10058239, 11836927, 13615615, 15459839, 4656639, 6435327, 8214015, ],
                [10519295, 11177983, 11836671, 12495615, 8543231, 9201919, 9860607, ],
                [13154559, 14010879, 14867199, 15723519, 10651135, 11441919, 12298239, ]]
        brown = [[5466499, 5795723, 6124947, 6454427, 4478571, 4807795, 5137019, ],
                 [8821426, 9347255, 9873340, 10399425, 7243428, 7769256, 8295341, ],
                 [13949924, 14607338, 15264752, 15922423, 11977425, 12634839, 13292253, ]]

        self.color_list = {
            "white": white,
            "black": black,
            "gray": gray,
            "red": red,
            "orange": orange,
            "yellow": yellow,
            "green": green,
            "blue": blue,
            "indigo": indigo,
            "purple": purple,
            "pink": pink,
            "brown": brown,
        }

        return self.color_list

    def ezcolor(self):
        self.color = {
            "": -4142, "none": -4142,
            "ez1": 6384127, "ez2": 4699135, "ez3": 9895421, "ez4": 7855479, "ez5": 13616814, "ez6": 11902643,
            "ez7": 12566463, "ez8": 12419407, "ez9": 5066944, "ez10": 5880731, "ez11": 10642560, "ez12": 13020235,
            "ez13": 4626167, "ez14": 65535, "ez15": 13566071,
            "white---": 15790320, "white--": 16119285, "white-": 16448250, "white": 16777215, "white+": 16777215,
            "white++": 16777215, "white+++": 16777215,
            "white_t---": 15790320, "white_t--": 16119285, "white_t-": 16448250, "white_t": 16777215,
            "white_t+": 16777215, "white_t++": 16777215, "white_t+++": 16777215,
            "white_p---": 15790320, "white_p--": 16119285, "white_p-": 16448250, "white_p": 16777215,
            "white_p+": 16777215, "white_p++": 16777215, "white_p+++": 16777215,
            "black---": 0, "black--": 0, "black-": 0, "black": 0, "black+": 1052688, "black++": 2171169,
            "black+++": 3289650,
            "black_t---": 0, "black_t--": 0, "black_t-": 0, "black_t": 0, "black_t+": 1052688, "black_t++": 2171169,
            "black_t+++": 3289650,
            "black_p---": 0, "black_p--": 1052688, "black_p-": 2171169, "black_p": 3289650, "black_p+": 4342338,
            "black_p++": 5460819, "black_p+++": 6579300,
            "gray---": 5855577, "gray--": 6710886, "gray-": 7566195, "gray": 8421504, "gray+": 9211020,
            "gray++": 10066329, "gray+++": 10921638,
            "gray_t---": 8355711, "gray_t--": 9605778, "gray_t-": 10855845, "gray_t": 12105912, "gray_t+": 13355979,
            "gray_t++": 14606046, "gray_t+++": 15921906,
            "gray_p---": 13355979, "gray_p--": 13750737, "gray_p-": 14211288, "gray_p": 14606046,
            "gray_p+": 15066597, "gray_p++": 15461355, "gray_p+++": 15921906,
            "red---": 179, "red--": 204, "red-": 230, "red": 255, "red+": 1710847, "red++": 3355647,
            "red+++": 5066239,
            "red_t---": 2303075, "red_t--": 4276858, "red_t-": 6316434, "red_t": 8356010, "red_t+": 10329794,
            "red_t++": 12369370, "red_t+++": 14408946,
            "red_p---": 1384703, "red_p--": 3029503, "red_p-": 4739583, "red_p": 6384127, "red_p+": 8094207,
            "red_p++": 9738751, "red_p+++": 11449087,
            "orange---": 29875, "orange--": 33996, "orange-": 38374, "orange": 42495, "orange+": 1748735,
            "orange++": 3389439, "orange+++": 5095679,
            "orange_t---": 411799, "orange_t--": 2712488, "orange_t-": 5013177, "orange_t": 7379402,
            "orange_t+": 9680091, "orange_t++": 11980780, "orange_t+++": 14347005,
            "orange_p---": 37626, "orange_p--": 1351423, "orange_p-": 3057919, "orange_p": 4699135,
            "orange_p+": 6405887, "orange_p++": 8046847, "orange_p+++": 9753599,
            "yellow---": 46003, "yellow--": 52428, "yellow-": 59110, "yellow": 65535, "yellow+": 1769471,
            "yellow++": 3407871, "yellow+++": 5111807,
            "yellow_t---": 47292, "yellow_t--": 115655, "yellow_t-": 249810, "yellow_t": 383965,
            "yellow_t+": 452584, "yellow_t++": 586739, "yellow_t+++": 720895,
            "yellow_p---": 4979964, "yellow_p--": 6618364, "yellow_p-": 8257021, "yellow_p": 9895421,
            "yellow_p+": 11533821, "yellow_p++": 13172478, "yellow_p+++": 14810878,
            "green---": 13312, "green--": 19712, "green-": 26368, "green": 32768, "green+": 39424, "green++": 45824,
            "green+++": 52480,
            "green_t---": 2646351, "green_t--": 4618601, "green_t-": 6590851, "green_t": 8563101,
            "green_t+": 10535351, "green_t++": 12507601, "green_t+++": 14545387,
            "green_p---": 3853882, "green_p--": 5165902, "green_p-": 6543459, "green_p": 7855479,
            "green_p+": 9167499, "green_p++": 10545056, "green_p+++": 11857076,
            "blue---": 11730944, "blue--": 13369344, "blue-": 15073280, "blue": 16711680, "blue+": 16718362,
            "blue++": 16724787, "blue+++": 16731469,
            "blue_t---": 6772768, "blue_t--": 8286527, "blue_t-": 9800286, "blue_t": 11379581, "blue_t+": 12893340,
            "blue_t++": 14407099, "blue_t+++": 15986395,
            "blue_p---": 11773054, "blue_p--": 12365710, "blue_p-": 13024158, "blue_p": 13616814,
            "blue_p+": 14209470, "blue_p++": 14867918, "blue_p+++": 15460574,
            "indigo---": 3538975, "indigo--": 5177390, "indigo-": 6881340, "indigo": 8519755, "indigo+": 10223706,
            "indigo++": 11862120, "indigo+++": 13566071,
            "indigo_t---": 6373412, "indigo_t--": 7953218, "indigo_t-": 9533281, "indigo_t": 11113087,
            "indigo_t+": 12693150, "indigo_t++": 14272956, "indigo_t+++": 15853019,
            "indigo_p---": 3538975, "indigo_p--": 5177390, "indigo_p-": 6881340, "indigo_p": 8519755,
            "indigo_p+": 10223706, "indigo_p++": 11862120, "indigo_p+++": 13566071,
            "purple---": 3407924, "purple--": 5046349, "purple-": 6750311, "purple": 8388736, "purple+": 10092698,
            "purple++": 11731123, "purple+++": 13435085,
            "purple_t---": 5321023, "purple_t--": 6966874, "purple_t-": 8678262, "purple_t": 10389650,
            "purple_t+": 12101037, "purple_t++": 13812425, "purple_t+++": 15524069,
            "purple_p---": 9728913, "purple_p--": 10453404, "purple_p-": 11178152, "purple_p": 11902643,
            "purple_p+": 12627134, "purple_p++": 13351882, "purple_p+++": 14076373,
            "pink---": 4656639, "pink--": 6435327, "pink-": 8214015, "pink": 10058239, "pink+": 11836927,
            "pink++": 13615615, "pink+++": 15459839,
            "pink_t---": 8543231, "pink_t--": 9201919, "pink_t-": 9860607, "pink_t": 10519295, "pink_t+": 11177983,
            "pink_t++": 11836671, "pink_t+++": 12495615,
            "pink_p---": 10651135, "pink_p--": 11441919, "pink_p-": 12298239, "pink_p": 13154559,
            "pink_p+": 14010879, "pink_p++": 14867199, "pink_p+++": 15723519,
            "brown---": 4478571, "brown--": 4807795, "brown-": 5137019, "brown": 5466499, "brown+": 5795723,
            "brown++": 6124947, "brown+++": 6454427,
            "brown_t---": 7243428, "brown_t--": 7769256, "brown_t-": 8295341, "brown_t": 8821426,
            "brown_t+": 9347255, "brown_t++": 9873340, "brown_t+++": 10399425,
            "brown_p---": 11977425, "brown_p--": 12634839, "brown_p-": 13292253, "brown_p": 13949924,
            "brown_p+": 14607338, "brown_p++": 15264752, "brown_p+++": 15922423,
            1: 0, 2: 16777215, 3: 255, 4: 65280, 5: 16711680, 6: 65535, 7: 16711935, 8: 16776960, 9: 128, 10: 32768,
            11: 8388608, 12: 32896, 13: 8388736, 14: 8421376, 15: 12632256, 16: 8421504, 17: 16751001, 18: 6697881,
            19: 13434879, 20: 16777164,
            21: 6684774, 22: 8421631, 23: 13395456, 24: 16764108, 25: 8388608, 26: 16711935, 27: 65535,
            28: 16776960, 29: 8388736, 30: 128,
            31: 8421376, 32: 16711680, 33: 16763904, 34: 16777164, 35: 13434828, 36: 10092543, 37: 16764057,
            38: 13408767, 39: 16751052, 40: 10079487,
            41: 16737843, 42: 13421619, 43: 52377, 44: 52479, 45: 39423, 46: 26367, 47: 10053222, 48: 9868950,
            49: 6697728, 50: 6723891,
            51: 13056, 52: 13107, 53: 13209, 54: 6697881, 55: 10040115, 56: 3355443,
        }
        return self.color


    def enum_thick(self):
        result = {
        "hairline": 1, "thin": 2, "medium": -4138, "thick": 4,
        "t1": 1, "t2": 2, "t3": -4138, "t4": 4,
        "basic--": 1, "basic-": 2, "basic+": -4138, "basic++": 4,
        }
        return result

    def enum_copy(self):
        result = {
        "": -4104, "basic": -4104, "all": -4104, "memo": -4144,
        "format": -4122, "formula": -4123, "formula+format": 11, "value": -4163, "value+format": 12,
        "pasteall": -4104, "pasteallexceptborders": 7, "pasteallmergingconditionalformats": 14,
        "pasteallusingsourcetheme": 13, "pastecolumnwidths": 8, "pastecomments": -4144,
        "pasteformats": -4122, "pasteformulas": -4123, "pasteformulasandnumberformats": 11,
        "pastevalidation": 6, "pastevalues": -4163, "pastevaluesandnumberformats": 12,
        }
        return result

    def enum_letter(self):
        result = {
        # 시작하는 첫글자로 이름을 사용한다
        # 원으로된 글자는 "a원"처럼 이름을 만듦
        "a": "abcdefghijklmnopqrstuvwxyz",
        "알파벳": "abcdefghijklmnopqrstuvwxyz",
        "영어": "abcdefghijklmnopqrstuvwxyz",
        "alphabet": "abcdefghijklmnopqrstuvwxyz",
        "ㄱ": "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ",
        "자음": "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ",
        "모음": "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ",
        "ㅏ": "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ",
        "가": "가나다라마바사아자차카타파하",
        "1": "1234567890",
        "숫자": "1234567890",
        "α": "αβγδεζήθικλμνξόπρΣτ",
        "그리스문자": "αβγδεζήθικλμνξόπρΣτ",
        "Ⅰ": "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ",
        "로마숫자": "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ",
        "원ㄱ": "㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭",
        "ㄱ원": "㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭",
        "원가": "㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻",
        "가원": "㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻",
        "a원": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
        "원a": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
        "원1": "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿",
        "1원": "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿",
        }
        return result

    def enum_sharp(self):
        result = {
        "10pointStar": 149,  # 10-point star,
        "12pointStar": 150,  # 12-point star,
        "16pointStar": 94,  # 16-point star,
        "24pointStar": 95,  # 24-point star,
        "32pointStar": 96,  # 32-point star,
        "4pointStar": 91,  # 4-point star,
        "5pointStar": 92,  # 5-point star,
        "6pointStar": 147,  # 6-point star,
        "7pointStar": 148,  # 7-point star,
        "8pointStar": 93,  # 8-point star,
        "ActionButtonBackorPrevious": 129,  # Back or Previous button. Supports mouse-click and mouse-over actions.,
        "ActionButtonBeginning": 131,  # Beginning button. Supports mouse-click and mouse-over actions.,
        "ActionButtonCustom": 125,  # Button with no default picture or text. Supports mouse-click and mouse-over actions.,
        "ActionButtonDocument": 134,  # Document button. Supports mouse-click and mouse-over actions.,
        "ActionButtonEnd": 132,  # End button. Supports mouse-click and mouse-over actions.,
        "ActionButtonForwardorNext": 130,  # Forward or Next button. Supports mouse-click and mouse-over actions.,
        "ActionButtonHelp": 127,  # Help button. Supports mouse-click and mouse-over actions.,
        "ActionButtonHome": 126,  # Home button. Supports mouse-click and mouse-over actions.,
        "ActionButtonInformation": 128,  # Information button. Supports mouse-click and mouse-over actions.,
        "ActionButtonMovie": 136,  # Movie button. Supports mouse-click and mouse-over actions.,
        "ActionButtonReturn": 133,  # Return button. Supports mouse-click and mouse-over actions.,
        "ActionButtonSound": 135,  # Sound button. Supports mouse-click and mouse-over actions.,
        "Arc": 25,  # 원호, Arc,
        "Balloon": 137,  # Balloon,
        "BentArrow": 41,  # 화살표(굽음)Block arrow that follows a curved 90-degree angle.,
        "BentUpArrow": 44,  # Block arrow that follows a sharp 90-degree angle. Points up by default.,
        "Bevel": 15,  # 사각형(빗면)Bevel,
        "BlockArc": 20,  # 원형(안이막힌것), Block arc,
        "Can": 13,  # 원통형, Can,
        "ChartPlus": 182,  # Square divided vertically and horizontally into four quarters,
        "ChartStar": 181,  # Square divided into six parts along vertical and diagonal lines,
        "ChartX": 180,  # Square divided into four parts along diagonal lines,
        "Chevron": 52,  # Chevron,
        "Chord": 161,
        # Circle with a line connecting two points on the perimeter through the interior of the circle; a circle with a chord,
        "CircularArrow": 60,  # Block arrow that follows a curved 180-degree angle,
        "Cloud": 179,  # Cloud shape,
        "CloudCallout": 108,  # Cloud callout,
        "Corner": 162,  # Rectangle with rectangular-shaped hole.,
        "CornerTabs": 169,  # Four right triangles aligning along a rectangular path; four 'snipped' corners.,
        "Cross": 11,  # 십자형, Cross,
        "Cube": 14,  # 정육면체, Cube,
        "CurvedDownArrow": 48,  # Block arrow that curves down,
        "CurvedDownRibbon": 100,  # Ribbon banner that curves down,
        "CurvedLeftArrow": 46,  # Block arrow that curves left,
        "CurvedRightArrow": 45,  # Block arrow that curves right,
        "CurvedUpArrow": 47,  # Block arrow that curves up,
        "CurvedUpRibbon": 99,  # Ribbon banner that curves up,
        "Decagon": 144,  # Decagon,
        "DiagonalStripe": 141,  # Rectangle with two triangles-shapes removed; a diagonal stripe,
        "Diamond": 4,  # Diamond,
        "Dodecagon": 146,  # Dodecagon,
        "Donut": 18,  # 원형(빈것)도넛형, Donut,
        "DoubleBrace": 27,  # 중괄호(양쪽)Double brace,
        "DoubleBracket": 26,  # 대괄호(양쪽)Double bracket,
        "DoubleWave": 104,  # Double wave,
        "DownArrow": 36,  # 화살표(아래쪽)Block arrow that points down,
        "DownArrowCallout": 56,  # Callout with arrow that points down,
        "DownRibbon": 98,  # Ribbon banner with center area below ribbon ends,
        "Explosion1": 89,  # Explosion,
        "Explosion2": 90,  # Explosion,
        "FlowchartAlternateProcess": 62,  # Alternate process flowchart symbol,
        "FlowchartCard": 75,  # Card flowchart symbol,
        "FlowchartCollate": 79,  # Collate flowchart symbol,
        "FlowchartConnector": 73,  # Connector flowchart symbol,
        "FlowchartData": 64,  # Data flowchart symbol,
        "FlowchartDecision": 63,  # Decision flowchart symbol,
        "FlowchartDelay": 84,  # Delay flowchart symbol,
        "FlowchartDirectAccessStorage": 87,  # Direct access storage flowchart symbol,
        "FlowchartDisplay": 88,  # Display flowchart symbol,
        "FlowchartDocument": 67,  # Document flowchart symbol,
        "FlowchartExtract": 81,  # Extract flowchart symbol,
        "FlowchartInternalStorage": 66,  # Internal storage flowchart symbol,
        "FlowchartMagneticDisk": 86,  # Magnetic disk flowchart symbol,
        "FlowchartManualInput": 71,  # Manual input flowchart symbol,
        "FlowchartManualOperation": 72,  # Manual operation flowchart symbol,
        "FlowchartMerge": 82,  # Merge flowchart symbol,
        "FlowchartMultidocument": 68,  # Multi-document flowchart symbol,
        "FlowchartOfflineStorage": 139,  # Offline storage flowchart symbol,
        "FlowchartOffpageConnector": 74,  # Off-page connector flowchart symbol,
        "FlowchartOr": 78,  # "Or" flowchart symbol,
        "FlowchartPredefinedProcess": 65,  # Predefined process flowchart symbol,
        "FlowchartPreparation": 70,  # Preparation flowchart symbol,
        "FlowchartProcess": 61,  # Process flowchart symbol,
        "FlowchartPunchedTape": 76,  # Punched tape flowchart symbol,
        "FlowchartSequentialAccessStorage": 85,  # Sequential access storage flowchart symbol,
        "FlowchartSort": 80,  # Sort flowchart symbol,
        "FlowchartStoredData": 83,  # Stored data flowchart symbol,
        "FlowchartSummingJunction": 77,  # Summing junction flowchart symbol,
        "FlowchartTerminator": 69,  # Terminator flowchart symbol,
        "FoldedCorner": 16,  # 사각형(모서리접힘)Folded corner,
        "Frame": 158,  # Rectangular picture frame,
        "Funnel": 174,  # Funnel,
        "Gear6": 172,  # Gear with six teeth,
        "Gear9": 173,  # Gear with nine teeth,
        "HalfFrame": 159,  # Half of a rectangular picture frame,
        "Heart": 21,  # 하트, Heart,
        "Heptagon": 145,  # Heptagon,
        "Hexagon": 10,  # 육각형, Hexagon,
        "HorizontalScroll": 102,  # Horizontal scroll,
        "IsoscelesTriangle": 7,  # 이등변삼각형, Isosceles triangle,
        "LeftArrow": 34,  # 화살표(왼쪽)Block arrow that points left,
        "LeftArrowCallout": 54,  # Callout with arrow that points left,
        "LeftBrace": 31,  # 중괄호(왼쪽)Left brace,
        "LeftBracket": 29,  # 대괄호(왼쪽)Left bracket,
        "LeftCircularArrow": 176,  # Circular arrow pointing counter-clockwise,
        "LeftRightArrow": 37,  # 화살표(왼쪽오른쪽)Block arrow with arrowheads that point both left and right,
        "LeftRightArrowCallout": 57,  # Callout with arrowheads that point both left and right,
        "LeftRightCircularArrow": 177,
        # Circular arrow pointing clockwise and counter-clockwise; a curved arrow with points at both ends,
        "LeftRightRibbon": 140,  # Ribbon with an arrow at both ends,
        "LeftRightUpArrow": 40,  # 화살표(상/좌/우)Block arrow with arrowheads that point left, right, and up,
        "LeftUpArrow": 43,  # 화살표(왼쪽위쪽)Block arrow with arrowheads that point left and up,
        "LightningBolt": 22,  # 번개, Lightning bolt,
        "LineCallout1": 109,  # Callout with border and horizontal callout line,
        "LineCallout1AccentBar": 113,  # Callout with horizontal accent bar,
        "LineCallout1BorderandAccentBar": 121,  # Callout with border and horizontal accent bar,
        "LineCallout1NoBorder": 117,  # Callout with horizontal line,
        "LineCallout2": 110,  # Callout with diagonal straight line,
        "LineCallout2AccentBar": 114,  # Callout with diagonal callout line and accent bar,
        "LineCallout2BorderandAccentBar": 122,  # Callout with border, diagonal straight line, and accent bar,
        "LineCallout2NoBorder": 118,  # Callout with no border and diagonal callout line,
        "LineCallout3": 111,  # Callout with angled line,
        "LineCallout3AccentBar": 115,  # Callout with angled callout line and accent bar,
        "LineCallout3BorderandAccentBar": 123,  # Callout with border, angled callout line, and accent bar,
        "LineCallout3NoBorder": 119,  # Callout with no border and angled callout line,
        "LineCallout4": 112,  # Callout with callout line segments forming a U-shape,
        "LineCallout4AccentBar": 116,  # Callout with accent bar and callout line segments forming a U-shape,
        "LineCallout4BorderandAccentBar": 124,
        # Callout with border, accent bar, and callout line segments forming a U-shape,
        "LineCallout4NoBorder": 120,  # Callout with no border and callout line segments forming a U-shape,
        "LineInverse": 183,  # Line inverse,
        "MathDivide": 166,  # Division symbol ÷,
        "MathEqual": 167,  # Equivalence symbol =,
        "MathMinus": 164,  # Subtraction symbol -,
        "MathMultiply": 165,  # Multiplication symbol x,
        "MathNotEqual": 168,  # Non-equivalence symbol ≠,
        "MathPlus": 163,  # Addition symbol +,
        "Mixed": -2,  # Return value only; indicates a combination of the other states.,
        "Moon": 24,  # 달, Moon,
        "NonIsoscelesTrapezoid": 143,  # Trapezoid with asymmetrical non-parallel sides,
        "NoSymbol": 19,  # "No" symbol,
        "NotchedRightArrow": 50,  # Notched block arrow that points right,
        "NotPrimitive": 138,  # Not supported,
        "Octagon": 6,  # 팔각형, Octagon,
        "Oval": 9,  # 타원형, Oval,
        "OvalCallout": 107,  # Oval-shaped callout,
        "Parallelogram": 2,  # 평행사변형, Parallelogram,
        "Pentagon": 51,  # Pentagon,
        "Pie": 142,  # Circle ('pie') with a portion missing,
        "PieWedge": 175,  # Quarter of a circular shape,
        "Plaque": 28,  # Plaque,
        "PlaqueTabs": 171,  # Four quarter-circles defining a rectangular shape,
        "QuadArrow": 39,  # 화살표(사방)Block arrows that point up, down, left, and right,
        "QuadArrowCallout": 59,  # Callout with arrows that point up, down, left, and right,
        "Rectangle": 1,  # 사각형, Rectangle,
        "RectangularCallout": 105,  # Rectangular callout,
        "RegularPentagon": 12,  # 5각형, Pentagon,
        "RightArrow": 33,  # 화살표(오른쪽)Block arrow that points right,
        "RightArrowCallout": 53,  # Callout with arrow that points right,
        "RightBrace": 32,  # 중괄호(오른쪽)Right brace,
        "RightBracket": 30,  # 대괄호(오른쪽)Right bracket,
        "RightTriangle": 8,  # 직각삼각형, Right triangle,
        "Round1Rectangle": 151,  # Rectangle with one rounded corner,
        "Round2DiagRectangle": 157,  # Rectangle with two rounded corners, diagonally-opposed,
        "Round2SameRectangle": 152,  # Rectangle with two-rounded corners that share a side,
        "RoundedRectangle": 5,  # Rounded rectangle,
        "RoundedRectangularCallout": 106,  # Rounded rectangle-shaped callout,
        "SmileyFace": 17,  # 웃는얼굴, Smiley face,
        "Snip1Rectangle": 155,  # Rectangle with one snipped corner,
        "Snip2DiagRectangle": 157,  # Rectangle with two snipped corners, diagonally-opposed,
        "Snip2SameRectangle": 156,  # Rectangle with two snipped corners that share a side,
        "SnipRoundRectangle": 154,  # 사각형(둥근모서리)Rectangle with one snipped corner and one rounded corner,
        "SquareTabs": 170,  # Four small squares that define a rectangular shape,
        "StripedRightArrow": 49,  # Block arrow that points right with stripes at the tail,
        "Sun": 23,  # 해, Sun,
        "SwooshArrow": 178,  # Curved arrow,
        "Tear": 160,  # Water droplet,
        "Trapezoid": 3,  # 사다리꼴, Trapezoid,
        "UpArrow": 35,  # 화살표(위쪽)Block arrow that points up,
        "UpArrowCallout": 55,  # Callout with arrow that points up,
        "UpDownArrow": 38,  # 화살표(위쪽아래쪽)Block arrow that points up and down,
        "UpDownArrowCallout": 58,  # Callout with arrows that point up and down,
        "UpRibbon": 97,  # Ribbon banner with center area above ribbon ends,
        "UTurnArrow": 42,  # 화살표(U턴)Block arrow forming a U shape,
        "VerticalScroll": 101,  # Vertical scroll,
        "Wave": 103,  # Wave,

        }
        return result

    def ezshape_line(self):
        #shape안의 line에대한 정의
        result = {
            "msoArrowheadNone": 1, "msoArrowheadTriangle": 2, "msoArrowheadOpen": 3, "msoArrowheadStealth": 4,
            "msoArrowheadDiamond": 5, "msoArrowheadOval": 6,
            "": 1, "<": 2, ">o": 3, ">>": 4, ">": 2, "<>": 5, "o": 6,
            "basic": 1, "none": 1, "triangle": 2, "open": 3, "stealth": 4, "diamond": 5, "oval": 6,
            "msoArrowheadNarrow": 1, "msoArrowheadWidthMedium": 2, "msoArrowheadWide": 3,
            "msoArrowheadShort": 1, "msoArrowheadLengthMedium": 2, "msoArrowheadLong": 3,
            "short": 1, "narrow": 1, "medium": 2, "long": 3, "wide": 3,
            "-1": 1, "0": 2, "1": 3,
            "dash": 4, "dashdot": 5, "dashdotdot": 6, "rounddot": 3, "longdash": 7, "longdashdot": 8, "longdashdotdot": 9,
            "squaredot": 2,
            "-": 4, "-.": 5, "-..": 6, ".": 3, "--": 7, "--.": 8, "--..": 9, "ㅁ": 2,
        }
        return result


    def ezline(self):
        result = {
        "": 1, "basic": 1, "-": -4115, "-.": 4, "-..": 5, ".": -4118, "=": -4119, "none": -4142, "/.": 13,
        "t1": 1, "t2": 2, "t3": -4138, "t4": 4,
        "basic--": 1, "basic-": 2, "basic+": -4138, "basic++": 4,
        "\\": 5, "/": 6, "b": 9, "l": 7, "r": 8, "t": 10,
        "in-h": 12, "in-v": 11, "bottom": 9, "left": 7, "right": 10, "top": 8,
        "bottom-in": 12, "top-in": 11, "rightleft-in": 12, "leftright-in": 5,
        "continuous": 1, "dash": -4115, "dashdot": 4, "dashdotdot": 5, "dot": -4118,
        "double": -4119, "slantdashdot": 13, "hairline": 1, "thin": 2, "medium": -4138, "thick": 4,
        "diagonaldown": 5, "diagonalup": 6, "edgebottom": 9, "edgeleft": 7, "edgeright": 8, "edgetop": 10,
        "insidehorizontal": 12, "insidevertical": 11, "inside-h": 12, "inside-v": 11,
        }
        return result
