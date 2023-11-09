import PySimpleGUI as sg
from S_AES import encrypt, decrypt
from extended_function import extended_function
from multiple_encryption import double_encrypt, double_decrypt, middle_crack
from operating_mode import CBC
def int_(input):
    try:
        # 先尝试将字符串解释为十进制
        decimal_value = int(input)
        return decimal_value
    except ValueError:
        try:
            # 如果失败，则尝试将字符串解释为十六进制
            binary_value = int(input, 2)
            return binary_value
        except ValueError:
            # 如果再次失败，则尝试将字符串解释为二进制
            try:
                hex_value = int(input, 16)
                return hex_value
            except ValueError:
                return input


sg.theme('BlueMono')
layout0 = [
    [sg.Button("普通加密", size=(20, 3)), sg.Button("拓展功能", size=(20, 3))],
    [sg.Button("双重加密", size=(20, 3)), sg.Button("三重加密", size=(20, 3)), sg.Button("操作模式", size=(20, 3))]
]
win0 = sg.Window("window0", layout0, default_element_size=(10, 1))  # 主窗口
win1_active = False  # 普通加密窗口

win2_active = False  # 双重加密窗口
win2_1_active = False  # 双重加密窗口子窗口1普通加密
win2_2_active = False  # 双重加密窗口子窗口2普通解密
win2_3_active = False  # 双重加密窗口子窗口3中间相遇攻击

win3_active = False  # 三重加密窗口
win4_active = False  # 工作模式窗口
win5_active = False  # 拓展功能窗口

while True:
    ev0, vals0 = win0.read(timeout=100)
    win0_active = True
    if ev0 == sg.WIN_CLOSED:
        break
    if ev0 == "普通加密" and not win1_active:  # 窗口1 普通加密
        win1_active = True
        win0.hide()
        layout1 = [
            [sg.Text('请输入您的明密文与密钥')],
            [sg.Text('输入明密文'), sg.InputText('')],
            [sg.Text('输入密钥'), sg.InputText('')],
            [sg.Button('加密', size=(20, 2)), sg.Button('解密', size=(20, 2))],
        ]
        win1 = sg.Window("window1", layout1, default_element_size=(30, 2))
        while True:
            ev1, vals1 = win1.read(timeout=100)  # 读取加密窗口内事件
            if ev1 == sg.WIN_CLOSED:
                win1_active = False
                win1.close()
                win0.UnHide()
                break
            # 在下方if输入函数
            elif ev1 == '加密':
                #     vals1[0]是字符串内容 vals1[1]是密钥内容
                ciphertext = encrypt(int_(vals1[0]), int_(vals1[1]))
                sg.popup_scrolled('密文是: ' + str(ciphertext))  # 弹出密文
            elif ev1 == '解密':
                #     vals1[0]是字符串内容 vals1[1]是密钥内容
                plaintext = decrypt(int_(vals1[0]), int_(vals1[1]))
                sg.popup_scrolled('明文是: ' + str(plaintext))  # 弹出明文

    if ev0 == "拓展功能" and not win5_active:  # 窗口5 拓展功能
        win5_active = True
        win0.hide()
        layout5 = [
            [sg.Text('请输入您的明密文与密钥')],
            [sg.Text('输入明密文'), sg.InputText('')],
            [sg.Text('输入密钥'), sg.InputText('')],
            [sg.Button('加密', size=(20, 2)), sg.Button('解密', size=(20, 2))],
        ]
        win5 = sg.Window("window5", layout5, default_element_size=(30, 2))
        while True:
            ev5, vals5 = win5.read(timeout=100)  # 读取加密窗口内事件
            if ev5 == sg.WIN_CLOSED:
                win5_active = False
                win5.close()
                win0.UnHide()
                break
            # 在下方if输入函数
            elif ev5 == '加密':
                #     vals5[0]是字符串内容 vals5[1]是密钥内容
                ciphertext = extended_function((vals5[0]), int_(vals5[1]))
                sg.popup_scrolled('密文是: ' + str(ciphertext))  # 弹出密文
            elif ev5 == '解密':
                #     vals5[0]是字符串内容 vals5[1]是密钥内容
                plaintext = extended_function((vals5[0]), int_(vals5[1]), True)
                sg.popup_scrolled('明文是: ' + str(plaintext))  # 弹出明文


    if ev0 == "双重加密" and not win2_active:  # 窗口2 双重加密
        win2_active = True
        win0.hide()
        layout2 = [
             [sg.Button('加密', size=(40, 6)), sg.Button('解密', size=(40, 6)), sg.Button('中间相遇攻击', size=(40, 6))]
        ]
        win2 = sg.Window("window2", layout2, default_element_size=(30, 2))
        while True:
            ev2, vals2 = win2.read(timeout=100)  # 读取窗口2 内事件
            if ev2 == sg.WIN_CLOSED:
                win2_active = False
                win2.close()
                win0.UnHide()
                break

            # 进入窗口2_1
            elif ev2 == '加密' and not win2_1_active:
                win2_1_active = True
                win2.hide()
                layout2_1 = [
                    [sg.Text('请输入您的明密文与密钥')],
                    [sg.Text('输入明密文'), sg.InputText('')],
                    [sg.Text('输入密钥1'), sg.InputText('')],
                    [sg.Text('输入密钥2'), sg.InputText('')],
                    [sg.Button('加密', size=(65, 3))],
                ]
                win2_1 = sg.Window("window2_1", layout2_1, default_element_size=(60, 2))
                while True:
                    ev2_1, vals2_1 = win2_1.read(timeout=100)  # 读取解密窗口内事件
                    if ev2_1 == sg.WIN_CLOSED:
                        win2_1_active = False
                        win2_1.close()
                        win2.UnHide()
                        break
                    # 在下方if输入函数
                    if ev2_1 == '加密':
                        # vals2_1[0]是密文内容 vals2_1[1]是密钥1内容 vals2_1[2]是密钥2内容
                        ciphertext = double_encrypt(vals2_1[0], int_(vals2_1[1]), int_(vals2_1[2]))
                        sg.popup_scrolled('密文是: ' + str(ciphertext))  # 弹出密文
            # 进入窗口2_2
            elif ev2 == '解密' and not win2_2_active:
                win2_2_active = True
                win2.hide()
                layout2_2 = [
                    [sg.Text('请输入您的明密文与密钥')],
                    [sg.Text('输入明密文'), sg.InputText('')],
                    [sg.Text('输入密钥1'), sg.InputText('')],
                    [sg.Text('输入密钥2'), sg.InputText('')],
                    [sg.Button('解密', size=(65, 3))],
                ]
                win2_2 = sg.Window("window2_2", layout2_2, default_element_size=(60, 2))
                while True:
                    ev2_2, vals2_2 = win2_2.read(timeout=100)  # 读取解密窗口内事件
                    if ev2_2 == sg.WIN_CLOSED:
                        win2_2_active = False
                        win2_2.close()
                        win2.UnHide()
                        break
                    # 在下方if输入函数
                    if ev2_2 == '解密':
                        # vals2_2[0]是密文内容 vals2_2[1]是密钥1内容 vals2_2[2]是密钥2内容
                        plaintext = double_decrypt(vals2_2[0], int_(vals2_2[1]), int_(vals2_2[2]))
                        sg.popup_scrolled('密文是: ' + str(plaintext))  # 弹出密文
            # 进入窗口2_3
            elif ev2 == '中间相遇攻击' and not win2_3_active:
                win2_3_active = True
                win2.hide()
                layout2_3 = [
                    [sg.Text('请输入您的明密文')],
                    [sg.Text('输入明文'), sg.InputText('')],
                    [sg.Text('输入密文'), sg.InputText('')],
                    [sg.Button('中间相遇攻击', size=(60, 3))],
                ]
                win2_3 = sg.Window("window2_3", layout2_3, default_element_size=(60, 2))
                while True:
                    ev2_3, vals2_3 = win2_3.read(timeout=100)  # 读取解密窗口内事件
                    if ev2_3 == sg.WIN_CLOSED:
                        win2_3_active = False
                        win2_3.close()
                        win2.UnHide()
                        break
                    # 在下方if输入函数
                    if ev2_3 == '中间相遇攻击':
                        # vals2_3[0]是明文内容 vals2_3[1]是密文内容
                        text = middle_crack(vals2_3[0], vals2_3[1])
                        sg.popup_scrolled('密钥是:\n' + str(text))  # 弹出明文
    if ev0 == "三重加密" and not win3_active:  # 窗口1 普通加密
        win3_active = True
        win0.hide()
        layout3 = [
            [sg.Text('请输入您的明密文与密钥')],
            [sg.Text('输入明密文'), sg.InputText('')],
            [sg.Text('输入密钥1'), sg.InputText('')],
            [sg.Text('输入密钥2'), sg.InputText('')],
            [sg.Text('输入密钥3'), sg.InputText('')],
            [sg.Button('加密', size=(20, 2)), sg.Button('解密', size=(20, 2))],
        ]
        win3 = sg.Window("window3", layout3, default_element_size=(30, 2))
        while True:
            ev3, vals3 = win3.read(timeout=100)  # 读取加密窗口内事件
            if ev3 == sg.WIN_CLOSED:
                win3_active = False
                win3.close()
                win0.UnHide()
                break
            # 在下方if输入函数
            elif ev3 == '加密':
                #     vals3[0]是字符串内容 vals3[1]是密钥内容
                ciphertext = extended_function(double_encrypt(vals3[0], int_(vals3[1]), int_(vals3[2])), int_(vals3[3]))
                sg.popup_scrolled('密文是：' + str(ciphertext))  # 弹出密文
            elif ev3 == '解密':
                #     vals3[0]是字符串内容 vals3[1]是密钥内容
                plaintext = double_decrypt(extended_function(vals3[0], int_(vals3[3]), True), int_(vals3[1]), int_(vals3[2]))
                sg.popup_scrolled('明文是：' + str(plaintext))  # 弹出明文
    if ev0 == "操作模式" and not win4_active:  # 窗口1 普通加密
        win4_active = True
        win0.hide()
        layout4 = [
            [sg.Text('请输入您的明密文与密钥、IV')],
            [sg.Text('输入明密文'), sg.InputText('')],
            [sg.Text('输入密钥'), sg.InputText('')],
            [sg.Text('输入IV'), sg.InputText('')],
            [sg.Button('加解密', size=(20, 2)), sg.Button('混淆', size=(20, 2))],
        ]
        win4 = sg.Window("window4", layout4, default_element_size=(30, 2))
        while True:
            ev4, vals4 = win4.read(timeout=100)  # 读取加密窗口内事件
            if ev4 == sg.WIN_CLOSED:
                win4_active = False
                win4.close()
                win0.UnHide()
                break
            # 在下方if输入函数
            elif ev4 == '加解密':
                #     vals4[0]是字符串内容 vals4[1]是密钥内容
                cipher_text = CBC(vals4[0], int_(vals4[1]), int_(vals4[2]))  # 密文
                text = CBC(cipher_text, int_(vals4[1]), int_(vals4[2]), True)  # 加解密后的明文
                sg.popup_scrolled('密文是：' + str(cipher_text) + '\n翻译后的明文是：' + str(text))  # 弹出密文
            elif ev4 == '混淆':
                #     vals4[0]是字符串内容 vals4[1]是密钥内容
                cipher_text = CBC(vals4[0], int_(vals4[1]), int_(vals4[2]))  # 密文
                changed_cipher_text = ''.join([cipher_text[-1], *cipher_text[1:-1], *cipher_text[0]])  # 改变了的密文
                changed_text = CBC(changed_cipher_text, int_(vals4[1]), int_(vals4[2]), True)  # 用上一个密文解密后的明文

                sg.popup_scrolled('混淆密文是：' + str(changed_cipher_text) + '\n翻译后的明文是：' + str(changed_text))  # 混淆

win0.close()
