# -*- coding: utf-8 -*-

import string
import time
import re

class pyeztext:
    my_web_site = "www.halmoney.com"

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
        # 숫자를 문자로 바꿔주는 것 ( 27 => aa)
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

    def between_a_b(self, input_data, text_a, text_b):
        # 입력된 자료에서 두개문자사이의 글자를 갖고오는것
        replace_lists=[
            ["(","\("],
            [")", "\)"],
        ]
        origin_a = text_a
        origin_b = text_b

        for one_list in replace_lists:
            text_a = text_a.replace(one_list[0], one_list[1])
            text_b = text_b.replace(one_list[0], one_list[1])
        re_basic =text_a+"[^"+str(origin_b)+"]*"+text_b
        result = re.findall(re_basic, input_data)
        return result

    def email_address(self, input_data):
        # 이메일주소 입력
        re_basic ="^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
        result = re.findall(re_basic, input_data)
        return result

    def ip_address(self, input_data):
        # 이메일주소 입력
        re_basic ="((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))"
        result = re.findall(re_basic, input_data)
        return result

    def no_times(self, input_data, m, n):
        # 이메일주소 입력
        re_basic ="^\d{"+str(m)+","+str(n) +"}$"
        result = re.findall(re_basic, input_data)
        return result

    def text_length(self, input_data, m, n):
        # 문자수제한 : m다 크고 n보다 작은 문자
        re_basic ="^.{"+str(m)+","+str(n) +"}$"
        result = re.findall(re_basic, input_data)
        return result

    def check_all_cap(self, input_data):
        # 모두 알파벳대문자
        re_basic ="^[A-Z]+$"
        result = re.findall(re_basic, input_data)
        return result

    def check_date_422 (self, input_data):
        # 모두 알파벳대문자
        re_basic ="^\d{4}-\d{1,2}-\d{1,2}$"
        result = re.findall(re_basic, input_data)
        return result

    def check_korean_only (self, input_data):
        # 모두 한글인지
        re_basic ="[ㄱ-ㅣ가-힣]"
        result = re.findall(re_basic, input_data)
        return result

    def check_korean_only (self, input_data):
        # 모두 영문인지
        re_basic ="[a-zA-Z]"
        result = re.findall(re_basic, input_data)
        return result

    def check_special_char (self, input_data):
        # 특수문자가들어가있는지
        re_basic ="^[a-zA-Z0-9]"
        result = re.findall(re_basic, input_data)
        return result

    def check_handphone (self, input_data):
        # 특수문자가들어가있는지
        re_basic ="^(010|019|011)-\d{4}-\d{4}"
        result = re.findall(re_basic, input_data)
        return result

    def check_basic (self, input_data, re_text):
        # 특수문자가들어가있는지
        re_basic = str(re_text)
        result = re.findall(re_basic, input_data)
        return result
