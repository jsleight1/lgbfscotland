import pandas as pd


def example_lgbf_metadata():
    return pd.DataFrame(
        {
            "Indicators_Information_Code": ["C&L02", "SW01"],
            "Indicators_Information_Title": [
                "Cost per Library Visit",
                "Home care costs per hour for people aged 65 or over",
            ],
            "Indicators_Information_ServiceArea": [
                "Culture & Leisure Services",
                "Adult Social Care Services",
            ],
            "Indicators_Information_Numerator_Title": [
                "Libraries - net expenditure (£000)",
                "Total Homecare Expenditure  (£000)",
            ],
            "Indicators_Information_Denominator_Title": [
                "Number of Library Visits",
                "Care Hours per Year,",
            ],
            "Indicators_Information_Unit": "Pounds",
            "Indicators_Information_Category": "Financial",
        }
    )


def example_lgbf_data():
    return pd.DataFrame(
        {
            "Indicators_Information_Code": [
                "C&L02",
                "C&L02",
                "C&L02",
                "C&L02",
                "SW01",
                "SW01",
                "SW01",
                "SW01",
            ],
            "LA_Information_LocalAuthority": [
                "Aberdeen City",
                "Aberdeen City",
                "Falkirk",
                "Falkirk",
                "Aberdeen City",
                "Aberdeen City",
                "Falkirk",
                "Falkirk",
            ],
            "LA_Data_LGBF_Year": [
                "2010-11",
                "2011-12",
                "2010-11",
                "2011-12",
                "2010-11",
                "2011-12",
                "2010-11",
                "2011-12",
            ],
            "LA_Data_LA_IndicatorReal": [
                5.211,
                3.5006,
                5.3123,
                6.1508,
                29.1235,
                28.0328,
                30.7446,
                33.6309,
            ],
            "LA_Data_LA_Numerator_real": [
                8243.444,
                5491.772,
                4572.615,
                4509.631,
                19564.248,
                19702.353,
                21858.517,
                21622.702,
            ],
            "LA_Data_LA_Den_Real": [
                1582483,
                1570220,
                860025,
                733914,
                671922.2,
                702913.1,
                711079.7,
                642815.7,
            ],
            "Scotland_Data_Scotland_Indicator_Real": [
                4.9359,
                4.6202,
                4.9359,
                4.6202,
                29.1524,
                28.0187,
                29.1524,
                28.0187,
            ],
            "Scotland_Data_Scotland_Num_Real": [
                156854.1,
                148097.9,
                156854.1,
                148097.9,
                629716.6,
                616961.4,
                629716.6,
                616961.4,
            ],
            "Scotland_Data_Scotland_Den_Real": [
                31800305,
                32074635,
                31800305,
                32074635,
                21602216,
                22016337,
                21602216,
                22016337,
            ],
            "FG_Data_FG_Avg_Indicator_Real": [
                5.523975,
                5.041812,
                5.523975,
                5.041812,
                30.60895,
                32.047125,
                27.290575,
                26.096563,
            ],
            "FG_Data_FG_Avg_Num_Real": [
                8956.513,
                8341.825,
                8956.513,
                8341.825,
                15864.469,
                16624.835,
                21924.016,
                21610.404,
            ],
            "FG_Data_FG_Avg_Den_Real": [
                1804141.5,
                1805378.4,
                1804141.5,
                1805378.4,
                548521.2,
                550521.9,
                817185.5,
                823029.2,
            ],
        }
    )
