from flask import Flask, render_template, request
import pickle  # Use this if the model is saved as a .pkl file

import pandas as pd


with open(r"C:\Users\FATHIMA SHEMEEMA\Music\internship\App_Hotspot\App_Hotspot\model.pkl", 'rb') as file:
    model = pickle.load(file)

with open(r'C:\Users\FATHIMA SHEMEEMA\Music\internship\App_Hotspot\App_Hotspot\accident_counts_encoded.pkl', 'rb') as file:
    accident_counts_encoder = pickle.load(file)


PS_Name_df=pd.read_csv(r'C:\Users\FATHIMA SHEMEEMA\Music\internship\App_Hotspot\App_Hotspot\PS_Name_df.csv')
district_df=pd.read_csv(r'C:\Users\FATHIMA SHEMEEMA\Music\internship\App_Hotspot\App_Hotspot\district_df.csv')
Spot_Accident_df=pd.read_csv(r'C:\Users\FATHIMA SHEMEEMA\Music\internship\App_Hotspot\App_Hotspot\Spot_Accident_df.csv')


district_map = dict(zip(district_df['District'], district_df['District_enc']))
spot_accident_map = dict(zip(Spot_Accident_df['Spot Accident'], Spot_Accident_df['Spot Accident_enc']))
ps_name_map = dict(zip(PS_Name_df['PS Name'], PS_Name_df['PS Name_enc']))


app = Flask(__name__)

# District and PS Name Data
district_data = {
    'THIRUVANANTHAPURAM CITY': ['Vattiyoorkavu', 'Vanchiyoor', 'Thumba', 'Kazhakkuttom', 'Thiruvallam',
                                'Nemom', 'Medical College', 'Poonthura', 'Peroorkada', 'Sreekariyam',
                                'Fort', 'Valiyathura', 'Poojappura', 'Museum', 'Vizhinjam', 'Thampanoor',
                                'Cantonment', 'Pettah', 'Kovalam', 'Mannanthala', 'Karamana'],
    'THIRUVANANTHAPURAM RURAL': ['Kadinamkulam', 'Varkala', 'Balaramapuram', 'Aruvikkara', 'Chirayinkil',
                                 'Kattakkada', 'Attingal', 'Neyyattinkara', 'Palode', 'Vellarada',
                                 'Pothencode', 'Vattappara', 'Maranalloor', 'Ayiroor', 'Pozhiyoor',
                                 'Kallambalam', 'Poovar', 'Kilimanoor', 'Malayinkil', 'Mangalapuram',
                                 'Pangode', 'Nedumangad', 'Parassala', 'Naruvamoodu', 'Kanjiramkulam',
                                 'Marayamuttom', 'Ariyancode', 'Valiyamala', 'Anchuthengu', 'Venjarammood',
                                 'Pallickal', 'Kadakkavoor', 'Aryanad', 'Neyyardam', 'Nagarur',
                                 'Vilappilsala', 'Vithura', 'Ponmudi'],
    'KOLLAM CITY': ['Karunagappally PS', 'Kottiyam PS', 'Eravipuram', 'Paravoor PS', 'Kilikollur PS',
                    'Pallithottam PS', 'Kannanelure PS', 'Chavara PS', 'Sakthikulangara PS', 'Parippally PS',
                    'Anchalumoodu PS', 'Ochira PS', 'Chavara Thekkumbhagam', 'Kollam East PS', 'Kollam West PS',
                    'Chathannoor PS'],
    'KOLLAM RURAL': ['Kundara PS', 'Eroor PS', 'Puthoor PS', 'Anchal PS', 'Chithara (Valavupacha) PS',
                     'Punalur PS', 'Sooranad PS', 'Kottarakkara PS', 'Thenmala PS', 'Pooyappally PS',
                     'Pathanapuram PS', 'Kunnikode PS', 'East Kallada PS', 'Sasthamcotta PS', 'Kadakkal PS',
                     'Ezhukone PS', 'Kulathupuzha PS', 'Chadayamangalam PS'],
    'PATHANAMTHITTA': ['Chittar', 'Thiruvalla', 'Enathu (old Kakkad)', 'Ranny', 'Adoor', 'Aranmula',
                       'Konni', 'Pandalam', 'Elavumthitta PS', 'Perunadu', 'Kodumon', 'Koipuram',
                       'Vechoochira', 'Perumpetty', 'Pathanamthitta', 'Malayalapuzha', 'Pulikeezhu',
                       'Keezhvaipur', 'Vadasserikkara', 'Koodal', 'Thannithodu', 'Pampa'],
    'ALAPPUZHA': ['Cherthala', 'Mannachery', 'Kareelakulangara', 'Alappuzha North', 'Pattanakkadu',
                  'Ambalapuzha', 'Nedumudy', 'Mannar', 'Kayamkulam', 'Muhamma', 'Kuthiathode PS',
                  'Kurathikad', 'Poochakkal', 'Aroor', 'Mavelikara', 'Kanakakunnu', 'Nooranadu',
                  'Harippad', 'Edathua', 'Mararikkulam', 'Pulincunnu', 'Alappuzha South', 'Punnapra',
                  'Vallikunnam', 'Thrikkunnapuzha', 'Chengannur', 'Arthinkal', 'Ramankari',
                  'Venmony', 'Veeyapuram'],
    'KOTTAYAM': ['Vaikom', 'Kuravilangadu', 'Ramapuram', 'Thidanadu', 'Gandhinagar', 'Pala',
                 'Ettumanoor', 'Pallikkathodu', 'Velloor', 'Vakathanam', 'Kumarakom', 'Chingavanam',
                 'Thalayolaparambu', 'Kaduthuruthy', 'Changanachery', 'Thrikkodithanam',
                 'Ponkunnam', 'Kidangoor', 'Erumely', 'Karukachal', 'Pampady', 'Mundakayam',
                 'Manarcadu', 'Ayarkunnam', 'Kanjirappally', 'Erattupetta', 'Kottayam East',
                 'Kottayam West', 'Manimala', 'Marangattupally', 'Melukavu'],
    'IDUKKI': ['Peerumedu', 'Thodupuzha', 'Thankamoney', 'Vandiperiyar', 'Munnar', 'Kanjikuzhy',
               'Santhanpara', 'Devikulam', 'Karimannoor', 'Karimkunnam', 'Rajakkadu', 'Nedumkandam',
               'Kumali', 'Vellathooval', 'Kattappana', 'Adimali', 'Kaliyar', 'Kanjar', 'Muttom',
               'Peruvanthanam', 'Vandanmedu', 'Udummbanchola PS', 'Cumbummettu', 'Upputhara',
               'Idukki', 'Kulamavu', 'Marayoor', 'Karimanal'],
     'ERNAKULAM CITY': [
        'Elamakkara', 'Hill Palace (Thrippunnithura)', 'Ernakulam Central', 'Infopark', 'Palluruthy Kasaba',
        'Kadavanthra', 'Palarivattom', 'Ernakulam Town South', 'Udayamperoor', 'Cheranelloor', 'Mattancherry',
        'Ambalamedu', 'Panangad', 'Fort Kochi', 'Thrikkakara', 'Mulavukadu', 'Kannamali', 'Maradu', 'Kalamassery',
        'Ernakulam Town North', 'Harbour', 'Thoppumpady', 'Eloor'
    ],
    'ERNAKULAM RURAL': [
        'Njarakkal', 'Aluva West', 'North Parur', 'Puthencruz', 'Oonnukal', 'Nedumbassery', 'Kuruppumpady',
        'Vadakkekara', 'Aluva', 'Muvattupuzha', 'Chottanikkara', 'Puthenvelikkara', 'Binanipuram', 'Vazhakulam',
        'Kunnathunadu', 'Angamaly', 'Kothamangalam', 'Munambam', 'Kalady', 'Perumbavoor', 'Kalloorkadu',
        'Kuttampuzha', 'Edathala', 'Thadiyittaparambu', 'Mulamthuruthy', 'Varapuzha', 'Kodanadu', 'Ramamangalam',
        'Pothanikkadu', 'Piravom', 'Kottapady', 'Ayyampuzha', 'Koothattukulam', 'Chengamanadu'
    ],
    'THRISSUR CITY': [
        'Thrissur Town East', 'Viyyur', 'Chelakkara', 'Chavakkad', 'Kunnamkulam', 'Medical College PS',
        'Wadakkanchery', 'Thrissur Town West', 'Nedupuzha', 'Ollur', 'Peramangalam', 'Vadakkekkad', 'Guruvayoor',
        'Peechi', 'Guruvayoor Temple PS', 'Cheruthuruthy', 'Pavaratty', 'Mannuthy', 'Erumapetty', 'Pazhayannoor'
    ],
    'THRISSUR RURAL': [
        'Chalakkudy', 'Anthikad', 'Mala', 'Cherpu', 'Vellikulangara', 'Koratty', 'Valappad', 'Kodungallur',
        'Aloor', 'Kaipamangalam', 'Vadanappally', 'Kattoor', 'Irinjalakkuda', 'Mathilakam', 'Varantharappally',
        'Pudukkad', 'Kodakara', 'Athirappally/ Vettilappara'
    ],
    'PALAKKAD': [
        'Kongad', 'Shornur', 'Nemmara', 'Kadambazhippuram', 'Sreekrishnapuram', 'Cherpulassery', 'Kollengode',
        'Palakkad Town South', 'Chittur', 'Alathur', 'Vadakkenchery', 'Mannarkkad', 'Ottappalam', 'Palakkad Town North',
        'Pattambi', 'Mankara', 'Walayar', 'Meenakshipuram', 'Kozhinjampara', 'Nalleppilly', 'Nattukal', 'Agali',
        'Govindapuram', 'Kinassery', 'Peruvemba', 'Kanjirampuzha', 'Alanallur', 'Cheruppulassery', 'Parli',
        'Elappully', 'Koppam', 'Kumaramputhur'
    ],
    'MALAPPURAM': [
        'Edakkara', 'Tirur', 'Kondotty', 'Kottakkal', 'Pandikkad', 'Vazhikkadavu', 'Nilambur', 'Vandoor', 'Areekode',
        'Kalpakancheri', 'Tanur', 'Parappanangadi', 'Chemmad', 'Karipur', 'Manjeri', 'Melattoor', 'Valanchery',
        'Malappuram', 'Tirurangadi', 'Kalikavu', 'Ponnani', 'Pothukkal', 'Kolathur', 'Kuzhalmannam'
    ],
    'KOZHIKODE CITY': [
        'Feroke', 'Kunnamangalam', 'Mukkom', 'Medical College PS', 'Chelannur', 'Vellayil', 'Kakkur', 'Karanthur',
        'Elathur', 'Kozhikode Town West', 'Mepayur', 'Kozhikode Town', 'Balussery', 'Kozhikode Town South', 'Koduvally',
        'Thamarassery', 'Kozhikode Town East', 'Meenchanda'
    ], 
    
    'KOZHIKODE RURAL': ['Koyilandy', 'Thamarassery', 'Koduvally', 'Kuttiady', 'Kakkur', 'Atholi', 'Thiruvambady', 
                        'Meppayur', 'Perambra', 'Vatakara', 'Mukkom', 'Payyoli', 'Thotilpalam', 'Edachery', 
                        'Valayam', 'Balussery', 'Chompala', 'Peruvannamoozhi', 'Kodenchery', 'Nadapuram', 
                        'Koorachundu'],
    'WAYANAD': ['Ambalavayal', 'Noolpuzha', 'Kambalakkad', 'Mananthavadi', 'Sulthan Batheri', 'Meenangadi', 
                'Vythiri', 'Kalpetta', 'Meppadi', 'Padinjarethara', 'Vellamunda', 'Thondarnadu', 'Thirunelli', 
                'Panamaram', 'Pulpally', 'Thalappuzha', 'Kenichira'],
    'KANNUR CITY': ['Panoor', 'Edakkad', 'Chockly', 'New Mahe', 'Chakkarakkal', 'Kathirur', 'Valapattanam', 
                    'Mattannur', 'Dharmadam', 'Mayyil', 'Kuthuparamba', 'Kolavallur', 'Kannavam', 'Thalassery', 
                    'Pinarayi', 'Kannur Town', 'Kannapuram'],
    'KASARAGOD': ['Bedakam', 'Hosdurg', 'Manjeshwar', 'Badiadka', 'Vellarikundu', 'Kasaragod', 'Adhur', 
                  'Cheemeni', 'Chittarikkal', 'Kumbla', 'Chandera', 'Nileshwar', 'Bekal', 'Vidyanagar', 
                  'Amabalathara', 'Melparamba PS', 'Rajapuram'],
    'KANNUR RURAL': ['Pariyaram MC PS', 'Payyavoor', 'Kelakam', 'Payyannur', 'Kudiyanmala', 'Alakode', 
                     'Taliparamba', 'Payangadi', 'Cherupuzha', 'Iritty', 'Peringome', 'Peravoor', 'Sreekandapuram', 
                     'Irikkur', 'Muzhakkunnu', 'Karikottakari', 'Ulikkal', 'Aralam', 'Maloor']    
}

# Spot Accident Dropdown Data
spot_accidents = ['Near bus stop', 'At pedestrian crossing', 'Market/Commercial area', 'Near office complex',
                  'Near a religious place', 'Institutional Area', 'In Residential area', 'Other',
                  'Near hospital', 'In Open area', 'Near petrol pump', 'Near or inside a village',
                  'Near a factory/industrial area', 'Narrow bridge or culverts',
                  'Near a recreation place/cinema', 'Affected by encroachments']



# Route for Home Page
@app.route('/')
def home():
    return render_template('home.html', district_data=district_data, spot_accidents=spot_accidents)

# Route for Result Page
@app.route('/predict', methods=['POST'])
def predict():
    district = request.form.get('district')
    ps_name = request.form.get('ps_name')
    spot_accident = request.form.get('spot_accident')

    # Mock Prediction Logic (replace with actual model prediction)
    #prediction = 'Hotspot' if district in ['THIRUVANANTHAPURAM CITY', 'KOLLAM CITY'] else 'Low Incident Area'
    data = {
    'District_enc': [district],
    'PS Name_enc': [ps_name],
    'Spot Accident_enc': [spot_accident]}

    input_df = pd.DataFrame(data)

    input_df['District_enc'] = input_df['District_enc'].map(district_map).fillna(input_df['District_enc'])
    input_df['Spot Accident_enc'] = input_df['Spot Accident_enc'].map(spot_accident_map).fillna(input_df['Spot Accident_enc'])
    input_df['PS Name_enc'] = input_df['PS Name_enc'].map(ps_name_map).fillna(input_df['PS Name_enc'])

    
    input_df=input_df.reindex(columns=['District_enc','PS Name_enc','Spot Accident_enc'], fill_value=0)

    predicted_cluster = model.predict(input_df)

    if predicted_cluster[0]==1:
        predicted_cluster="LOW INCIDENT AREA"
    else:
        predicted_cluster="HOT SPOT"

    




    return render_template('result.html', prediction=predicted_cluster)

if __name__ == '__main__':
    app.run(debug=True)