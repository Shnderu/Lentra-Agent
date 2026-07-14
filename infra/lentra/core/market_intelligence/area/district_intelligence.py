from typing import Dict, Any


DA_NANG_DISTRICTS = {

    "an_thuong": {
        "aliases": [
            "an thuong",
            "an thuong area",
            "an thuong beach"
        ],
        "score": 9.3,
        "profile": {
            "internet": 9.2,
            "safety": 8.5,
            "noise": 7.0,
            "infrastructure": 9.0,
            "expat_density": 10.0
        }
    },


    "my_an": {
        "aliases": [
            "my an",
            "mỹ an",
            "my an beach"
        ],
        "score": 9.1,
        "profile": {
            "internet": 9.0,
            "safety": 8.5,
            "noise": 7.0,
            "infrastructure": 9.0,
            "expat_density": 9.5
        }
    },


    "an_hai_bac": {
        "aliases": [
            "an hai bac",
            "an hải bắc",
            "my khe",
            "my khe beach"
        ],
        "score": 9.0,
        "profile": {
            "internet": 9.0,
            "safety": 8.5,
            "noise": 7.0,
            "infrastructure": 9.0,
            "expat_density": 9.0
        }
    },


    "hai_chau": {
        "aliases": [
            "hai chau",
            "hai châu",
            "city center",
            "central",
            "center",
            "downtown"
        ],
        "score": 8.3,
        "profile": {
            "internet": 8.5,
            "safety": 8.5,
            "noise": 6.5,
            "infrastructure": 9.5,
            "expat_density": 7.5
        }
    },


    "son_tra": {
        "aliases": [
            "son tra",
            "son trà",
            "son tra peninsula"
        ],
        "score": 8.4,
        "profile": {
            "internet": 8.0,
            "safety": 8.5,
            "noise": 8.0,
            "infrastructure": 8.0,
            "expat_density": 7.5
        }
    },


    "ngu_hanh_son": {
        "aliases": [
            "ngu hanh son",
            "ngũ hành sơn",
            "marble mountain",
            "hoa hai",
            "hoa hai ward"
        ],
        "score": 8.7,
        "profile": {
            "internet": 8.5,
            "safety": 8.5,
            "noise": 8.0,
            "infrastructure": 8.0,
            "expat_density": 8.0
        }
    },


    "thanh_khe": {
        "aliases": [
            "thanh khe",
            "thanh khê"
        ],
        "score": 7.0,
        "profile": {
            "internet": 7.5,
            "safety": 7.5,
            "noise": 6.5,
            "infrastructure": 7.5,
            "expat_density": 5.5
        }
    }

}



def detect_district(
    listing: Dict[str, Any]
) -> str:

    text = " ".join(
        [
            str(listing.get("title", "")),
            str(listing.get("description", "")),
            str(listing.get("location", ""))
        ]
    ).lower()


    # specific zones first
    detection_order = [
        "an_thuong",
        "my_an",
        "an_hai_bac",
        "hai_chau",
        "son_tra",
        "ngu_hanh_son",
        "thanh_khe"
    ]


    for district in detection_order:

        data = DA_NANG_DISTRICTS[district]

        for alias in data["aliases"]:

            if alias in text:
                return district


    return "unknown"



def get_district_intelligence(
    district: str
) -> Dict[str, Any]:

    data = DA_NANG_DISTRICTS.get(
        district
    )


    if not data:

        return {
            "district": district,
            "score": 5.0,
            "profile": {
                "internet": 5.0,
                "safety": 5.0,
                "noise": 5.0,
                "infrastructure": 5.0,
                "expat_density": 5.0
            }
        }


    return {
        "district": district,
        "score": data["score"],
        "profile": data["profile"]
    }
