# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.utils.translation import ugettext_lazy as _

LINK_TYPES = ['original', 'data', 'image', 'metadata', 'html',
              'OGC:WMS', 'OGC:WFS', 'OGC:WCS']

HIERARCHY_LEVELS = (
    ('series', _('series')),
    ('software', _('computer program or routine')),
    ('featureType', _('feature type')),
    ('model', _('copy or imitation of an existing or hypothetical object')),
    ('collectionHardware', _('collection hardware')),
    ('collectionSession', _('collection session')),
    ('nonGeographicDataset', _('non-geographic data')),
    ('propertyType', _('property type')),
    ('fieldSession', _('field session')),
    ('dataset', _('dataset')),
    ('service', _('service interfaces')),
    ('attribute', _('attribute class')),
    ('attributeType', _('characteristic of a feature')),
    ('tile', _('tile or spatial subset of geographic data')),
    ('feature', _('feature')),
    ('dimensionGroup', _('dimension group')),
)

UPDATE_FREQUENCIES = (
    ('unknown', _('frequency of maintenance for the data is not known')),
    ('continual', _('data is repeatedly and frequently updated')),
    ('notPlanned', _('there are no plans to update the data')),
    ('daily', _('data is updated each day')),
    ('annually', _('data is updated every year')),
    ('asNeeded', _('data is updated as deemed necessary')),
    ('monthly', _('data is updated each month')),
    ('fortnightly', _('data is updated every two weeks')),
    ('irregular',
        _('data is updated in intervals that are uneven in duration')),
    ('weekly', _('data is updated on a weekly basis')),
    ('biannually', _('data is updated twice each year')),
    ('quarterly', _('data is updated every three months')),
)

CONTACT_FIELDS = [
    'name',
    'organization',
    'position',
    'voice',
    'facsimile',
    'delivery_point',
    'city',
    'administrative_area',
    'postal_code',
    'country',
    'email',
    'role'
]

DEFAULT_SUPPLEMENTAL_INFORMATION = _(
    _('No information provided')
)

COUNTRIES = (
    ('AFG', 'Afghanistan'),
    ('ALA', 'Aland Islands'),
    ('ALB', 'Albania'),
    ('DZA', 'Algeria'),
    ('ASM', 'American Samoa'),
    ('AND', 'Andorra'),
    ('AGO', 'Angola'),
    ('AIA', 'Anguilla'),
    ('ATG', 'Antigua and Barbuda'),
    ('ARG', 'Argentina'),
    ('ARM', 'Armenia'),
    ('ABW', 'Aruba'),
    ('AUS', 'Australia'),
    ('AUT', 'Austria'),
    ('AZE', 'Azerbaijan'),
    ('BHS', 'Bahamas'),
    ('BHR', 'Bahrain'),
    ('BGD', 'Bangladesh'),
    ('BRB', 'Barbados'),
    ('BLR', 'Belarus'),
    ('BEL', 'Belgium'),
    ('BLZ', 'Belize'),
    ('BEN', 'Benin'),
    ('BMU', 'Bermuda'),
    ('BTN', 'Bhutan'),
    ('BOL', 'Bolivia'),
    ('BIH', 'Bosnia and Herzegovina'),
    ('BWA', 'Botswana'),
    ('BRA', 'Brazil'),
    ('VGB', 'British Virgin Islands'),
    ('BRN', 'Brunei Darussalam'),
    ('BGR', 'Bulgaria'),
    ('BFA', 'Burkina Faso'),
    ('BDI', 'Burundi'),
    ('KHM', 'Cambodia'),
    ('CMR', 'Cameroon'),
    ('CAN', 'Canada'),
    ('CPV', 'Cape Verde'),
    ('CYM', 'Cayman Islands'),
    ('CAF', 'Central African Republic'),
    ('TCD', 'Chad'),
    ('CIL', 'Channel Islands'),
    ('CHL', 'Chile'),
    ('CHN', 'China'),
    ('HKG', 'China - Hong Kong'),
    ('MAC', 'China - Macao'),
    ('COL', 'Colombia'),
    ('COM', 'Comoros'),
    ('COG', 'Congo'),
    ('COK', 'Cook Islands'),
    ('CRI', 'Costa Rica'),
    ('CIV', 'Cote d\'Ivoire'),
    ('HRV', 'Croatia'),
    ('CUB', 'Cuba'),
    ('CYP', 'Cyprus'),
    ('CZE', 'Czech Republic'),
    ('PRK', 'Democratic People\'s Republic of Korea'),
    ('COD', 'Democratic Republic of the Congo'),
    ('DNK', 'Denmark'),
    ('DJI', 'Djibouti'),
    ('DMA', 'Dominica'),
    ('DOM', 'Dominican Republic'),
    ('ECU', 'Ecuador'),
    ('EGY', 'Egypt'),
    ('SLV', 'El Salvador'),
    ('GNQ', 'Equatorial Guinea'),
    ('ERI', 'Eritrea'),
    ('EST', 'Estonia'),
    ('ETH', 'Ethiopia'),
    ('FRO', 'Faeroe Islands'),
    ('FLK', 'Falkland Islands (Malvinas)'),
    ('FJI', 'Fiji'),
    ('FIN', 'Finland'),
    ('FRA', 'France'),
    ('GUF', 'French Guiana'),
    ('PYF', 'French Polynesia'),
    ('GAB', 'Gabon'),
    ('GMB', 'Gambia'),
    ('GEO', 'Georgia'),
    ('DEU', 'Germany'),
    ('GHA', 'Ghana'),
    ('GIB', 'Gibraltar'),
    ('GRC', 'Greece'),
    ('GRL', 'Greenland'),
    ('GRD', 'Grenada'),
    ('GLP', 'Guadeloupe'),
    ('GUM', 'Guam'),
    ('GTM', 'Guatemala'),
    ('GGY', 'Guernsey'),
    ('GIN', 'Guinea'),
    ('GNB', 'Guinea-Bissau'),
    ('GUY', 'Guyana'),
    ('HTI', 'Haiti'),
    ('VAT', 'Holy See (Vatican City)'),
    ('HND', 'Honduras'),
    ('HUN', 'Hungary'),
    ('ISL', 'Iceland'),
    ('IND', 'India'),
    ('IDN', 'Indonesia'),
    ('IRN', 'Iran'),
    ('IRQ', 'Iraq'),
    ('IRL', 'Ireland'),
    ('IMN', 'Isle of Man'),
    ('ISR', 'Israel'),
    ('ITA', 'Italy'),
    ('JAM', 'Jamaica'),
    ('JPN', 'Japan'),
    ('JEY', 'Jersey'),
    ('JOR', 'Jordan'),
    ('KAZ', 'Kazakhstan'),
    ('KEN', 'Kenya'),
    ('KIR', 'Kiribati'),
    ('KWT', 'Kuwait'),
    ('KGZ', 'Kyrgyzstan'),
    ('LAO', 'Lao People\'s Democratic Republic'),
    ('LVA', 'Latvia'),
    ('LBN', 'Lebanon'),
    ('LSO', 'Lesotho'),
    ('LBR', 'Liberia'),
    ('LBY', 'Libyan Arab Jamahiriya'),
    ('LIE', 'Liechtenstein'),
    ('LTU', 'Lithuania'),
    ('LUX', 'Luxembourg'),
    ('MKD', 'Macedonia'),
    ('MDG', 'Madagascar'),
    ('MWI', 'Malawi'),
    ('MYS', 'Malaysia'),
    ('MDV', 'Maldives'),
    ('MLI', 'Mali'),
    ('MLT', 'Malta'),
    ('MHL', 'Marshall Islands'),
    ('MTQ', 'Martinique'),
    ('MRT', 'Mauritania'),
    ('MUS', 'Mauritius'),
    ('MYT', 'Mayotte'),
    ('MEX', 'Mexico'),
    ('FSM', 'Micronesia, Federated States of'),
    ('MCO', 'Monaco'),
    ('MNG', 'Mongolia'),
    ('MNE', 'Montenegro'),
    ('MSR', 'Montserrat'),
    ('MAR', 'Morocco'),
    ('MOZ', 'Mozambique'),
    ('MMR', 'Myanmar'),
    ('NAM', 'Namibia'),
    ('NRU', 'Nauru'),
    ('NPL', 'Nepal'),
    ('NLD', 'Netherlands'),
    ('ANT', 'Netherlands Antilles'),
    ('NCL', 'New Caledonia'),
    ('NZL', 'New Zealand'),
    ('NIC', 'Nicaragua'),
    ('NER', 'Niger'),
    ('NGA', 'Nigeria'),
    ('NIU', 'Niue'),
    ('NFK', 'Norfolk Island'),
    ('MNP', 'Northern Mariana Islands'),
    ('NOR', 'Norway'),
    ('PSE', 'Occupied Palestinian Territory'),
    ('OMN', 'Oman'),
    ('PAK', 'Pakistan'),
    ('PLW', 'Palau'),
    ('PAN', 'Panama'),
    ('PNG', 'Papua New Guinea'),
    ('PRY', 'Paraguay'),
    ('PER', 'Peru'),
    ('PHL', 'Philippines'),
    ('PCN', 'Pitcairn'),
    ('POL', 'Poland'),
    ('PRT', 'Portugal'),
    ('PRI', 'Puerto Rico'),
    ('QAT', 'Qatar'),
    ('KOR', 'Republic of Korea'),
    ('MDA', 'Republic of Moldova'),
    ('REU', 'Reunion'),
    ('ROU', 'Romania'),
    ('RUS', 'Russian Federation'),
    ('RWA', 'Rwanda'),
    ('BLM', 'Saint-Barthelemy'),
    ('SHN', 'Saint Helena'),
    ('KNA', 'Saint Kitts and Nevis'),
    ('LCA', 'Saint Lucia'),
    ('MAF', 'Saint-Martin (French part)'),
    ('SPM', 'Saint Pierre and Miquelon'),
    ('VCT', 'Saint Vincent and the Grenadines'),
    ('WSM', 'Samoa'),
    ('SMR', 'San Marino'),
    ('STP', 'Sao Tome and Principe'),
    ('SAU', 'Saudi Arabia'),
    ('SEN', 'Senegal'),
    ('SRB', 'Serbia'),
    ('SYC', 'Seychelles'),
    ('SLE', 'Sierra Leone'),
    ('SGP', 'Singapore'),
    ('SVK', 'Slovakia'),
    ('SVN', 'Slovenia'),
    ('SLB', 'Solomon Islands'),
    ('SOM', 'Somalia'),
    ('ZAF', 'South Africa'),
    ('SSD', 'South Sudan'),
    ('ESP', 'Spain'),
    ('LKA', 'Sri Lanka'),
    ('SDN', 'Sudan'),
    ('SUR', 'Suriname'),
    ('SJM', 'Svalbard and Jan Mayen Islands'),
    ('SWZ', 'Swaziland'),
    ('SWE', 'Sweden'),
    ('CHE', 'Switzerland'),
    ('SYR', 'Syrian Arab Republic'),
    ('TJK', 'Tajikistan'),
    ('THA', 'Thailand'),
    ('TLS', 'Timor-Leste'),
    ('TGO', 'Togo'),
    ('TKL', 'Tokelau'),
    ('TON', 'Tonga'),
    ('TTO', 'Trinidad and Tobago'),
    ('TUN', 'Tunisia'),
    ('TUR', 'Turkey'),
    ('TKM', 'Turkmenistan'),
    ('TCA', 'Turks and Caicos Islands'),
    ('TUV', 'Tuvalu'),
    ('UGA', 'Uganda'),
    ('UKR', 'Ukraine'),
    ('ARE', 'United Arab Emirates'),
    ('GBR', 'United Kingdom'),
    ('TZA', 'United Republic of Tanzania'),
    ('USA', 'United States of America'),
    ('VIR', 'United States Virgin Islands'),
    ('URY', 'Uruguay'),
    ('UZB', 'Uzbekistan'),
    ('VUT', 'Vanuatu'),
    ('VEN', 'Venezuela (Bolivarian Republic of)'),
    ('VNM', 'Viet Nam'),
    ('WLF', 'Wallis and Futuna Islands'),
    ('ESH', 'Western Sahara'),
    ('YEM', 'Yemen'),
    ('ZMB', 'Zambia'),
    ('ZWE', 'Zimbabwe'),
)

# Taken from http://www.w3.org/WAI/ER/IG/ert/iso639.htm
ALL_LANGUAGES = (
    ('abk', 'Abkhazian'),
    ('aar', 'Afar'),
    ('afr', 'Afrikaans'),
    ('amh', 'Amharic'),
    ('ara', 'Arabic'),
    ('asm', 'Assamese'),
    ('aym', 'Aymara'),
    ('aze', 'Azerbaijani'),
    ('bak', 'Bashkir'),
    ('ben', 'Bengali'),
    ('bih', 'Bihari'),
    ('bis', 'Bislama'),
    ('bre', 'Breton'),
    ('bul', 'Bulgarian'),
    ('bel', 'Byelorussian'),
    ('cat', 'Catalan'),
    ('chi', 'Chinese'),
    ('cos', 'Corsican'),
    ('dan', 'Danish'),
    ('dzo', 'Dzongkha'),
    ('eng', 'English'),
    ('fra', 'French'),
    ('epo', 'Esperanto'),
    ('est', 'Estonian'),
    ('fao', 'Faroese'),
    ('fij', 'Fijian'),
    ('fin', 'Finnish'),
    ('fry', 'Frisian'),
    ('glg', 'Gallegan'),
    ('ger', 'German'),
    ('gre', 'Greek'),
    ('kal', 'Greenlandic'),
    ('grn', 'Guarani'),
    ('guj', 'Gujarati'),
    ('hau', 'Hausa'),
    ('heb', 'Hebrew'),
    ('hin', 'Hindi'),
    ('hun', 'Hungarian'),
    ('ind', 'Indonesian'),
    ('ina', 'Interlingua (International Auxiliary language Association)'),
    ('iku', 'Inuktitut'),
    ('ipk', 'Inupiak'),
    ('ita', 'Italian'),
    ('jpn', 'Japanese'),
    ('kan', 'Kannada'),
    ('kas', 'Kashmiri'),
    ('kaz', 'Kazakh'),
    ('khm', 'Khmer'),
    ('kin', 'Kinyarwanda'),
    ('kir', 'Kirghiz'),
    ('kor', 'Korean'),
    ('kur', 'Kurdish'),
    ('oci', 'Langue d \'Oc (post 1500)'),
    ('lao', 'Lao'),
    ('lat', 'Latin'),
    ('lav', 'Latvian'),
    ('lin', 'Lingala'),
    ('lit', 'Lithuanian'),
    ('mlg', 'Malagasy'),
    ('mlt', 'Maltese'),
    ('mar', 'Marathi'),
    ('mol', 'Moldavian'),
    ('mon', 'Mongolian'),
    ('nau', 'Nauru'),
    ('nep', 'Nepali'),
    ('nor', 'Norwegian'),
    ('ori', 'Oriya'),
    ('orm', 'Oromo'),
    ('pan', 'Panjabi'),
    ('pol', 'Polish'),
    ('por', 'Portuguese'),
    ('pus', 'Pushto'),
    ('que', 'Quechua'),
    ('roh', 'Rhaeto-Romance'),
    ('run', 'Rundi'),
    ('rus', 'Russian'),
    ('smo', 'Samoan'),
    ('sag', 'Sango'),
    ('san', 'Sanskrit'),
    ('scr', 'Serbo-Croatian'),
    ('sna', 'Shona'),
    ('snd', 'Sindhi'),
    ('sin', 'Singhalese'),
    ('ssw', 'Siswant'),
    ('slv', 'Slovenian'),
    ('som', 'Somali'),
    ('sot', 'Sotho'),
    ('spa', 'Spanish'),
    ('sun', 'Sudanese'),
    ('swa', 'Swahili'),
    ('tgl', 'Tagalog'),
    ('tgk', 'Tajik'),
    ('tam', 'Tamil'),
    ('tat', 'Tatar'),
    ('tel', 'Telugu'),
    ('tha', 'Thai'),
    ('tir', 'Tigrinya'),
    ('tog', 'Tonga (Nyasa)'),
    ('tso', 'Tsonga'),
    ('tsn', 'Tswana'),
    ('tur', 'Turkish'),
    ('tuk', 'Turkmen'),
    ('twi', 'Twi'),
    ('uig', 'Uighur'),
    ('ukr', 'Ukrainian'),
    ('urd', 'Urdu'),
    ('uzb', 'Uzbek'),
    ('vie', 'Vietnamese'),
    ('vol', 'Volapük'),
    ('wol', 'Wolof'),
    ('xho', 'Xhosa'),
    ('yid', 'Yiddish'),
    ('yor', 'Yoruba'),
    ('zha', 'Zhuang'),
    ('zul', 'Zulu'),
)

CHARSETS = (('', 'None/Unknown'),
            ('UTF-8', 'UTF-8/Unicode'),
            ('ISO-8859-1', 'Latin1/ISO-8859-1'),
            ('ISO-8859-2', 'Latin2/ISO-8859-2'),
            ('ISO-8859-3', 'Latin3/ISO-8859-3'),
            ('ISO-8859-4', 'Latin4/ISO-8859-4'),
            ('ISO-8859-5', 'Latin5/ISO-8859-5'),
            ('ISO-8859-6', 'Latin6/ISO-8859-6'),
            ('ISO-8859-7', 'Latin7/ISO-8859-7'),
            ('ISO-8859-8', 'Latin8/ISO-8859-8'),
            ('ISO-8859-9', 'Latin9/ISO-8859-9'),
            ('ISO-8859-10', 'Latin10/ISO-8859-10'),
            ('ISO-8859-13', 'Latin13/ISO-8859-13'),
            ('ISO-8859-14', 'Latin14/ISO-8859-14'),
            ('ISO8859-15', 'Latin15/ISO-8859-15'),
            ('Big5', 'BIG5'),
            ('EUC-JP', 'EUC-JP'),
            ('EUC-KR', 'EUC-KR'),
            ('GBK', 'GBK'),
            ('GB18030', 'GB18030'),
            ('Shift_JIS', 'Shift_JIS'),
            ('KOI8-R', 'KOI8-R'),
            ('KOI8-U', 'KOI8-U'),
            ('cp874', 'Windows CP874'),
            ('windows-1250', 'Windows CP1250'),
            ('windows-1251', 'Windows CP1251'),
            ('windows-1252', 'Windows CP1252'),
            ('windows-1253', 'Windows CP1253'),
            ('windows-1254', 'Windows CP1254'),
            ('windows-1255', 'Windows CP1255'),
            ('windows-1256', 'Windows CP1256'),
            ('windows-1257', 'Windows CP1257'),
            ('windows-1258', 'Windows CP1258'))
