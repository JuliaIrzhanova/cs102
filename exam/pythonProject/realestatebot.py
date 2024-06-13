import telebot
from telebot import types
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
import time

TOKEN = '7340458228:AAHDEn4iZB2WmEzzMCCry0yOY9q7LMOtZdc'
bot = telebot.TeleBot(TOKEN)

data = pd.read_csv('data.csv')

label_encoders = {}
for col in ['Apartment type', 'Region', 'Renovation']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

le_metro = LabelEncoder()
data['Metro station'] = le_metro.fit_transform(data['Metro station'])
label_encoders['Metro station'] = le_metro

with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

params_list = ['Apartment type', 'Metro station', 'Minutes to metro', 'Region', 'Number of rooms',
               'Area', 'Living area', 'Kitchen area', 'Floor', 'Number of floors', 'Renovation']

user_states = {}

theta = np.array([12089836.01186028, 2865510.08611568, -32989.92273134,
                  -612359.86729597, -1554774.13514984, -400848.42611825,
                  5576276.03285642, 19941.79599452, 254923.59812154,
                  324376.45622536, 416419.81924532, 1234254.26881162])
error = 4544637


def standardize(df):
    df = df.copy()
    mean = df.mean()
    std = df.std()
    if np.isscalar(std):
        if std == 0:
            std = 1
    else:
        std[std == 0] = 1
    return (df - mean) / std

X = data.drop(columns=['Price'])
X_standardized = standardize(X).reset_index(drop=True)

def predict(X_test, theta):
    X_test_standardized = standardize(X_test)
    X_test_standardized = np.c_[np.ones(X_test_standardized.shape[0]), X_test_standardized]
    return X_test_standardized.dot(theta)


def find_anomalies(features):
    filtered_data = data.copy()
    for param, value in features.items():
        if value != 'Do not specify parameter' and value != '-':
            if param in label_encoders:
                value = label_encoders[param].transform([value])[0]
            filtered_data = filtered_data[filtered_data[param] == value]

    anomalies = []
    for index, row in filtered_data.iterrows():
        feature_values = [row[param] for param in params_list]
        feature_array = np.array(feature_values).reshape(1, -1)
        predicted_price = predict(feature_array, theta)[0]
        actual_price = row['Price']
        if predicted_price - actual_price > error:
            anomalies.append(row)

    anomalies_df = pd.DataFrame(anomalies)
    anomalies_df = anomalies_df.head(10)
    return decode_anomalies(anomalies_df)


def decode_anomalies(anomalies_df):
    for param, encoder in label_encoders.items():
        if param in anomalies_df.columns:
            anomalies_df[param] = anomalies_df[param].astype(int)
            anomalies_df[param] = encoder.inverse_transform(anomalies_df[param])
    return anomalies_df


def send_next_param(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    current_step = state['step']

    if current_step < len(params_list):
        param_name = params_list[current_step]

        if param_name in label_encoders and param_name != 'Metro station':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            options = list(label_encoders[param_name].classes_)
            for option in options:
                markup.add(types.KeyboardButton(option))
            markup.add(types.KeyboardButton('Do not specify parameter'))
            bot.send_message(chat_id, f"Enter {param_name}:", reply_markup=markup)
        elif param_name == 'Metro station':
            markup = types.ForceReply(selective=False)
            bot.send_message(chat_id, f"Enter {param_name} (in Russian and with capital letter) (or '-' to skip):",
                             reply_markup=markup)
        else:
            markup = types.ForceReply(selective=False)
            bot.send_message(chat_id, f"Enter {param_name} (or '-' to skip):", reply_markup=markup)
    else:
        if state['command'] == 'estimate':
            feature_values = []
            for param in params_list:
                value = state['params'].get(param, '-')
                if param in label_encoders and value != 'Do not specify parameter':
                    value = label_encoders[param].transform([value])[0] if value != '-' else 0
                elif param == 'Metro station' and value != '-':
                    value = label_encoders['Metro station'].transform([value])[0]
                feature_values.append(float(value) if value != '-' else 0)
            feature_array = np.array(feature_values).reshape(1, -1)
            price = predict(feature_array, theta)
            bot.send_message(chat_id, f'Estimated price: {price[0]:.2f} with error: {error:.2f}')
        elif state['command'] == 'anomalies':
            anomalies = find_anomalies(state['params'])
            if not anomalies.empty:
                response = anomalies.to_string(index=False)
                send_long_message(chat_id, f'Anomalously cheap housing:\n{response}')
            else:
                bot.send_message(chat_id, 'No anomalously cheap housing found.')
            user_states.pop(chat_id)

def send_long_message(chat_id, text, chunk_size=4096):
    for i in range(0, len(text), chunk_size):
        try:
            bot.send_message(chat_id, text[i:i + chunk_size])
        except Exception as e:
            print(f"Failed to send message chunk: {e}")
            time.sleep(1)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! I'm a real estate valuation bot in Moscow. Enter /help for a list of commands.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Commands:\n"
        "/estimate - Real estate valuation\n"
        "/anomalies - Find anomalously cheap housing\n"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['estimate'])
def estimate(message):
    user_states[message.chat.id] = {'command': 'estimate', 'params': {}, 'step': 0}
    send_next_param(message)

@bot.message_handler(commands=['anomalies'])
def anomalies(message):
    user_states[message.chat.id] = {'command': 'anomalies', 'params': {}, 'step': 0}
    send_next_param(message)

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def handle_message(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    current_step = state['step']
    param_name = params_list[current_step]
    user_response = message.text.strip()

    if user_response != "Do not specify parameter":
        state['params'][param_name] = user_response

    state['step'] += 1
    send_next_param(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
