# Generated by Django 2.0.3 on 2018-08-16 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0008_auto_20180815_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingmethodcountry',
            name='country_code',
            field=models.CharField(blank=True, choices=[('', 'Rest of World'), ('BY', 'Беларусь'), ('BB', 'Барбадос'), ('TR', 'Турция'), ('NR', 'Науру'), ('ET', 'Эфиопия'), ('JO', 'Иордания'), ('ER', 'Эритрея'), ('TG', 'Того'), ('AM', 'Армения'), ('NU', 'Ниуэ'), ('HU', 'Венгрия'), ('RS', 'Сербия'), ('MR', 'Мавритания'), ('IL', 'Израиль'), ('KH', 'Камбоджа'), ('BG', 'Болгария'), ('SY', 'Сирия'), ('DM', 'Доминика'), ('PE', 'Перу'), ('CL', 'Чили'), ('TO', 'Тонга'), ('LB', 'Ливан'), ('TD', 'Чад'), ('AU', 'Австралия'), ('ES', 'Испания'), ('FJ', 'Фиджи'), ('AL', 'Албания'), ('MM', 'Мьянмы'), ('GL', 'Гренландия'), ('SR', 'Суринам'), ('ME', 'Черногория'), ('CW', 'Кюрасао'), ('CZ', 'Чехия'), ('ZW', 'Зимбабве'), ('MZ', 'Мозамбик'), ('RU', 'Россия'), ('GH', 'Гана'), ('SV', 'Сальвадор'), ('BZ', 'Белиз'), ('FI', 'Финляндия'), ('BI', 'Бурунди'), ('JE', 'Джерси'), ('BW', 'Ботсвана'), ('BE', 'Бельгия'), ('GY', 'Гайана'), ('LU', 'Люксембург'), ('AT', 'Австрия'), ('RW', 'Руанда'), ('IR', 'Иран'), ('GU', 'Гуам'), ('NA', 'Намибия'), ('GI', 'Гибралтар'), ('SG', 'Сингапур'), ('YT', 'Майотта'), ('MO', 'Макао'), ('LR', 'Либерии'), ('GN', 'Гвинея'), ('PA', 'Панама'), ('DK', 'Дания'), ('HK', 'Гонконг'), ('LT', 'Литва'), ('IE', 'Ирландия'), ('AQ', 'Антарктида'), ('GE', 'Грузия'), ('LA', 'Лаос'), ('BT', 'Бутан'), ('TJ', 'Таджикистан'), ('BH', 'Бахрейн'), ('TN', 'Тунис'), ('MG', 'Мадагаскар'), ('MU', 'Маврикий'), ('PW', 'Палау'), ('MA', 'Марокко'), ('KG', 'Киргизия'), ('GT', 'Гватемала'), ('PY', 'Парагвай'), ('JP', 'Япония'), ('GG', 'Гернси'), ('EC', 'Эквадор'), ('HT', 'Гаити'), ('TW', 'Тайвань'), ('IT', 'Италия'), ('AI', 'Ангилья'), ('ID', 'Индонезия'), ('DZ', 'Алжир'), ('AD', 'Андорра'), ('MD', 'Молдавия'), ('NE', 'Нигер'), ('MC', 'Монако'), ('TH', 'Таиланд'), ('GM', 'Гамбия'), ('UG', 'Уганда'), ('DE', 'Германия'), ('VE', 'Венесуэла'), ('EE', 'Эстония'), ('PL', 'Польша'), ('SO', 'Сомали'), ('PN', 'Питкэрн'), ('SD', 'Судан'), ('HR', 'Хорватия'), ('LS', 'Лесото'), ('CO', 'Колумбия'), ('GP', 'Гваделупа'), ('IS', 'Исландия'), ('SE', 'Швеция'), ('SZ', 'Свазиленд'), ('BN', 'Бруней'), ('CU', 'Куба'), ('CN', 'Китай'), ('NP', 'Непал'), ('UA', 'Украина'), ('MV', 'Мальдивы'), ('FR', 'Франция'), ('MK', 'Македония'), ('MQ', 'Мартиника'), ('MN', 'Монголия'), ('KE', 'Кения'), ('AZ', 'Азербайджан'), ('AF', 'Афганистан'), ('AW', 'Аруба'), ('CG', 'Конго'), ('KW', 'Кувейт'), ('CA', 'Канада'), ('KI', 'Кирибати'), ('NI', 'Никарагуа'), ('ML', 'Мали'), ('MS', 'Монтсеррат'), ('AO', 'Ангола'), ('HN', 'Гондурас'), ('IQ', 'Ирак'), ('PK', 'Пакистан'), ('TV', 'Тувалу'), ('MT', 'Мальта'), ('BJ', 'Бенин'), ('CM', 'Камерун'), ('IN', 'Индия'), ('WS', 'Самоа'), ('LY', 'Ливия'), ('LV', 'Латвия'), ('TK', 'Токелау'), ('GR', 'Греция'), ('CY', 'Кипр'), ('AR', 'Аргентина'), ('MX', 'Мексика'), ('TZ', 'Танзания'), ('UZ', 'Узбекистан'), ('PH', 'Филиппины'), ('SN', 'Сенегал'), ('JM', 'Ямайка'), ('DJ', 'Джибути'), ('UY', 'Уругвай'), ('MY', 'Малайзия'), ('QA', 'Катар'), ('PT', 'Португалия'), ('EG', 'Египет'), ('NO', 'Норвегия'), ('CH', 'Швейцария'), ('SI', 'Словения'), ('BO', 'Боливия'), ('RO', 'Румыния'), ('SK', 'Словакия'), ('GA', 'Габон'), ('VN', 'Вьетнам'), ('YE', 'Йемен'), ('NL', 'Нидерланды'), ('GD', 'Гренада'), ('ZM', 'Замбия'), ('RE', 'Реюньон'), ('VU', 'Вануату'), ('LI', 'Лихтенштейн'), ('BR', 'Бразилия'), ('MW', 'Малави'), ('KZ', 'Казахстан'), ('BD', 'Бангладеш'), ('TM', 'Туркменистан'), ('NG', 'Нигерия'), ('OM', 'Оман'), ('PF', 'Французская Полинезия'), ('KM', 'Коморские острова'), ('SC', 'Сейшельские острова'), ('CK', 'Острова Кука'), ('SB', 'Соломоновы Острова'), ('KR', 'Южная Корея'), ('SA', 'Саудовская Аравия'), ('NZ', 'Новая Зеландия'), ('AX', 'Аландские острова'), ('CF', 'Центральноафриканская Республика'), ('BV', 'Остров Буве'), ('BS', 'Багамские острова'), ('GQ', 'Экваториальная Гвинея'), ('BM', 'Бермудские острова'), ('ZA', 'Южная Африка'), ('AS', 'Американское Самоа'), ('FO', 'Фарерские острова'), ('IM', 'Остров Мэн'), ('GB', 'Соединенное Королевство'), ('SS', 'Южный Судан'), ('VA', 'Святой Престол'), ('CX', 'Остров Рождества'), ('NC', 'Новой Каледонии'), ('GF', 'Французская Гвиана'), ('EH', 'Западная Сахара'), ('KP', 'Северная Корея'), ('NF', 'Остров Норфолк'), ('MH', 'Маршалловы острова'), ('DO', 'Доминиканская Республика'), ('KY', 'Каймановы острова'), ('TF', 'Французские южные территории'), ('WF', 'Уоллис и Футуна'), ('TT', 'Тринидад и Тобаго'), ('AG', 'Антигуа и Барбуда'), ('MP', 'Северные Марианские острова'), ('BA', 'Босния и Герцеговина'), ('US', 'Соединенные Штаты Америки'), ('AE', 'Объединенные Арабские Эмираты'), ('UM', 'Внешние малые острова США'), ('TC', 'Острова Теркс и Кайкос'), ('HM', 'Остров Херд и Острова Макдоналд'), ('IO', 'Британская территория в Индийском океане'), ('GS', 'Южная Георгия и Южные Сандвичевы острова'), ('VG', 'Виргинские Острова (Британские)'), ('VI', 'Виргинские Острова (США)'), ('SX', 'Святого Мартина (Остров, нидерландская часть)'), ('MF', 'Святого Мартина (Остров, французская часть)'), ('SJ', 'Шпицберген и Ян-Майен'), ('FK', 'Фолклендские острова [Мальвинские]'), ('CD', 'Конго (Демократическая Республика)'), ('FM', 'Микронезия (Федеративные Штаты)'), ('CC', 'Кокосовые (Килинг) острова'), ('SH', 'Святой Елены, Вознесения и Тристан-да-Кунья (Острова)'), ('SM', 'Сан - Марино'), ('PS', 'Палестина, Государство'), ('BQ', 'Бонайре, Синт-Эстатиус и Саба'), ('CV', 'Кабо-Верде'), ('LC', 'Сент-Люсия'), ('LK', 'Шри-Ланка'), ('GW', 'Гвинея-Бисау'), ('BL', 'Сен-Бартельми'), ('BF', 'Буркина-Фасо'), ('PR', 'Пуэрто-Рико'), ('SL', 'Сьерра-Леоне'), ('TL', 'Тимор-Лесте'), ('CR', 'Коста-Рика'), ('PG', 'Папуа-Новая Гвинея'), ('ST', 'Сан-Томе и Принсипи'), ('VC', 'Сент-Винсент и Гренадины'), ('PM', 'Сен-Пьер и Микелон'), ('KN', 'Сент-Китс и Невис'), ('CI', "Кот-д'Ивуар"), ('EU', 'European Union')], default='', max_length=2),
        ),
    ]