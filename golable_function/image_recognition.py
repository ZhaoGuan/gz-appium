# -*- coding: utf-8 -*-# __author__ = 'Gz'from PIL import Imageimport pytesseract# 直接使用这个方法高亮的文字显示是最好用的，并且这个对于不同的语言识别是不一样的，在image_to_string方法下能够选择语言需要看下详细内容。# 现在看成本最低的就是之前吧所有的语言的图片都截图然后在固定的theme中进行对比一直则正确，不够智能# 看看研究下opencv吧# 根据tessdata编写lang_wordbook# 在使用的时候要把相应的语言包装上lang_wordbook = {}def ocr_text(imagepath, set_lang='eng'):    text = ''    try:        img = Image.open(imagepath)        img.load()        try:            text = pytesseract.image_to_string(img, lang=set_lang)        except:            text = pytesseract.image_to_string(img)    except Exception as e:        print(e)    return textif __name__ == '__main__':    text_result = ocr_text('/Users/xm/Desktop/KTS/keyboard_regression/temp/keyboard_back20171024155310.png',                           set_lang='eng')    print(text_result)    text = text_result.split(' ')    print(text)