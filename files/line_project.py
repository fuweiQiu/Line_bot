from flask import Flask, request
from flask import render_template
import json
import csv
import random

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import StickerMessage, StickerSendMessage
from linebot.models import ImageMessage, ImageSendMessage
from linebot.models import LocationAction, LocationSendMessage, LocationMessage
from linebot.models import ButtonsTemplate, TemplateSendMessage, MessageTemplateAction, Template, template
from linebot.models import PostbackAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate

def get_all_question():
        all_data = []
        filename = '/Users/qiufuwei/Library/Mobile Documents/com~apple~CloudDocs/python/112_2_proj/question.csv'
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                all_data.append(row)
        return all_data
app = Flask(__name__)

app.static_folder = '/Users/qiufuwei/Library/Mobile Documents/com~apple~CloudDocs/python/112_2_proj/imgs'
@app.route('/imgs/<string:filename>')
def imgs(filename):
    return app.send_static_file(filename)

@app.route('/question')
def question():
    #不能出現的題號
    log_all = []
    log_filename = '/Users/qiufuwei/Library/Mobile Documents/com~apple~CloudDocs/python/112_2_proj/answer_log.csv'
    with open(log_filename, 'r') as file:
        count_ques = csv.reader(file)
        for i in count_ques:
            log_all.append(i)
    if len(log_all) > 1:
        count = int(log_all[-1][2])
    else:
        count = 0
    if count >= 5:
        return render_template('over.html')
    else:
        print(count)
        ansed_question = []
        with open(log_filename, 'r') as file:
            log_reader = csv.reader(file)
            next(log_reader)
            for i in log_reader:
                if len(i) != 0:
                    ansed_question.append(int(i[4]))
        all_data = []
        filename = '/Users/qiufuwei/Library/Mobile Documents/com~apple~CloudDocs/python/112_2_proj/question.csv'
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                all_data.append(row)
        number = random.randint(1,17)
        while number in ansed_question:
            number = random.randint(1,17)
        print(number)
        ques_number = all_data[number][0]
        ques_content = all_data[number][2]
        option_a, option_b, option_c, option_d = all_data[number][3], all_data[number][4], all_data[number][5], all_data[number][6]
        return render_template('question.html', ques_number = ques_number,A = option_a,B = option_b,C = option_c, D = option_d, question = ques_content, id_num = number)

@app.route('/send_answer', methods=['POST'])
def get_ans(): 
    log_filename = '/Users/qiufuwei/Library/Mobile Documents/com~apple~CloudDocs/python/112_2_proj/answer_log.csv'
    with open(log_filename, 'r') as file:
        log_reader = csv.reader(file)
        original_data = []
        for o in log_reader:
            original_data.append(o)
    with open(log_filename, 'r') as file:
        log_reader = csv.reader(file)
        next(log_reader)
        times = 0
        username = 'U0daabaca1dbc019d5f12607dee82b735'
        for i in log_reader:
            if len(i) != 0:
                username = i[0]
                times = int(i[2])
    id = request.form.get('id')
    user_ans = request.form.get('answer')
    all_data = get_all_question()
    id_num = int(id)
    current = all_data[id_num][7]
    write_times = times + 1
    if current == user_ans:
        status = True
        with open(log_filename, 'w') as file:
            log_writer = csv.writer(file)
            original_data.append(
                [
                    username,
                    status,
                    write_times,
                    True,
                    id_num
                ]
            )
            log_writer.writerows(original_data)
        return render_template('current.html')
    else:
        status = False
        with open(log_filename, 'w') as file:
            log_writer = csv.writer(file)    
            original_data.append(
                    [
                        username,
                        status,
                        write_times,
                        True,
                        id_num
                    ]
            )
            log_writer.writerows(original_data)
        return render_template('error.html')

@app.route('/linebot', methods=['POST'])
def line_bot():
    url = 'https://68e5-61-227-235-200.ngrok-free.app' #ngrok 對外網址
    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        access_token = 'VtYBdIAjqWrreQRXse8eI/Nbrmy2XSrlb/y70uXcio6OD2twfLXnFUC5SRYdewASRa2usBcKW+Pj+XjkMbOtWNgAcJoGgz+K53wQgFVutl/MVX7Y3vVDXmje7YObgTPpU5YYfg+bRksW7lzA7h31xQdB04t89/1O/w1cDnyilFU='
        secret = '471d94d9da13367934ffd36a03b6a887'
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        type = json_data['events'][0]['message']['type']
        if type == 'text':
            text = json_data['events'][0]['message']['text']
            if text == '開始紀錄':
                # original_data = []
                # with open('/Users/qiufuwei/Library/Mobile Documents/com~apple~CloudDocs/python/112_2_proj/answer_log.csv', 'r') as file:
                #     reader = csv.reader(file)
                #     for data in reader:
                #         original_data.append(data)
                # first_log = [json_data['events'][0]['source']['userId'], True, 0, True, 0]
                # original_data.append(first_log)
                # with open('/Users/qiufuwei/Library/Mobile Documents/com~apple~CloudDocs/python/112_2_proj/answer_log.csv', 'w') as file:
                #     file_writer = csv.writer(file)
                #     file_writer.writerows(original_data)
                msg = '已開始紀錄測驗，點擊隨機抽題即可答題'
            elif text == '查看測驗結果':
                log_filename = '/Users/qiufuwei/Library/Mobile Documents/com~apple~CloudDocs/python/112_2_proj/answer_log.csv'
                all_log = []
                current = 0
                with open(log_filename, 'r') as file:
                    reader = csv.reader(file)
                    for i in reader:
                        all_log.append(i)
                    times = all_log[-1][2]
                    for j in all_log:
                        if j[1] == 'True':
                            current = current + 1
                with open(log_filename,'w') as file:
                    writer = csv.writer(file)
                    original_row = ['USER','STATUS','TIMES','START','QUESTION_ID']
                    writer.writerow(original_row)
                msg = f'總共作答{times}題 答對{current}題 正確率{(int(current) / int(times)) * 100}%'
            else:
                msg = '若要開始紀錄 請輸入「開始紀錄測驗」或者點擊選單中的「開始紀錄」'
            line_bot_api.reply_message(tk, TextSendMessage(msg))
    except:
        print(body)
    return 'Finish'

if __name__ == '__main__':
    app.run(port=5218, debug=True)  