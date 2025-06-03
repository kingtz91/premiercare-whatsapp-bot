
from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'premierverifytoken'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
PHONE_NUMBER_ID = 'YOUR_PHONE_NUMBER_ID'

LANGUAGES = {'1': 'english', '2': 'swahili', '3': 'french'}
user_lang = {}

@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return 'Verification failed', 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get('entry'):
        for entry in data['entry']:
            for change in entry['changes']:
                value = change['value']
                messages = value.get('messages')
                if messages:
                    for message in messages:
                        phone = message['from']
                        text = message.get('text', {}).get('body', '').strip()
                        if phone not in user_lang:
                            send_language_selection(phone)
                        else:
                            lang = user_lang[phone]
                            handle_message(phone, text, lang)
    return 'ok', 200

def send_language_selection(phone):
    message = "🤖 Welcome to Premier Care Clinic! Please select your preferred language:\n1 - English\n2 - Kiswahili\n3 - Français"
    send_message(phone, message)

def handle_message(phone, text, lang):
    if lang not in LANGUAGES.values():
        if text in LANGUAGES:
            user_lang[phone] = LANGUAGES[text]
            send_main_menu(phone, LANGUAGES[text])
        else:
            send_language_selection(phone)
        return

    responses = {
        '1': 'consult',
        '2': 'vaccine',
        '3': 'lab',
        '4': 'result',
        '5': 'staff'
    }

    if text in responses:
        send_message(phone, translate(lang, responses[text]))
    else:
        send_main_menu(phone, lang)

def send_main_menu(phone, lang):
    menus = {
        'english': "Please choose a service:\n1 - Book a Consultation\n2 - Vaccination Services\n3 - Self-request Lab Test\n4 - Ask for Test Results\n5 - Speak to Our Staff",
        'swahili': "Tafadhali chagua huduma:\n1 - Panga Ushauri\n2 - Huduma za Chanjo\n3 - Omba Kipimo cha Maabara\n4 - Uliza Matokeo ya Vipimo\n5 - Ongea na Mfanyakazi Wetu",
        'french': "Veuillez choisir un service :\n1 - Prendre un Rendez-vous\n2 - Services de Vaccination\n3 - Demander un Test de Laboratoire\n4 - Demander les Résultats des Tests\n5 - Parler à Notre Personnel"
    }
    send_message(phone, menus.get(lang, menus['english']))

def translate(lang, option):
    content = {
        'consult': {
            'english': "Please provide your full name and preferred appointment date/time.",
            'swahili': "Tafadhali toa jina lako kamili na tarehe/muda wa miadi unaopendelea.",
            'french': "Veuillez fournir votre nom complet et la date/heure de rendez-vous souhaitées."
        },
        'vaccine': {
            'english': "We offer various vaccinations including Yellow Fever. Specify vaccine and branch (Masaki/Namanga).",
            'swahili': "Tunatoa chanjo mbalimbali ikiwa ni pamoja na Homa ya Manjano. Taja chanjo na tawi (Masaki/Namanga).",
            'french': "Nous proposons diverses vaccinations y compris la fièvre jaune. Précisez le vaccin et la succursale (Masaki/Namanga)."
        },
        'lab': {
            'english': "Please list the lab tests you want. We’ll guide you next.",
            'swahili': "Tafadhali orodhesha vipimo unavyotaka. Tutakuongoza zaidi.",
            'french': "Veuillez lister les tests souhaités. Nous vous guiderons."
        },
        'result': {
            'english': "Provide your full name and test date to get your results.",
            'swahili': "Toa jina kamili na tarehe ya kipimo kupata matokeo.",
            'french': "Fournissez votre nom complet et la date du test."
        },
        'staff': {
            'english': "Connecting you to our staff. Please wait...",
            'swahili': "Tunakunganisha na mfanyakazi wetu. Tafadhali subiri...",
            'french': "Connexion avec notre personnel. Veuillez patienter..."
        }
    }
    return content[option][lang]

def send_message(phone, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "text": {"body": message}
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    app.run(debug=True)
