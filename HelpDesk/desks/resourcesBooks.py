from Config.settings import API_KEY_BACKLOG, API_USER_BACKLOG, URL_BACKLOG
from requests import get
__author__ = 'Manuel Escriche'

domain = URL_BACKLOG
auth = API_USER_BACKLOG, API_KEY_BACKLOG


def find_enablersbook():
    # TODO: Need to get dinamically the information of the enablersbook, currently it is a static workaround just to
    #       stay working the tool
    # url = '{}'.format(domain) + '/api/enablersbook'
    # answer = get(url, auth=auth)

    # if not answer.ok:
    #     raise Exception

    result = {
  "book": {
    "2D-3D Capture": {
      "backlog_keyword": "2D-3DCapture",
      "chapter": "WebUI",
      "component": "10241",
      "owner": "J-P Viuhkola"
    },
    "2D-UI": {
      "backlog_keyword": "2D-UI",
      "chapter": "WebUI",
      "component": "10234",
      "owner": "Cvetan Stefanovski"
    },
    "Aeon": {
      "backlog_keyword": "Aeon",
      "chapter": "Data",
      "component": "10332",
      "owner": "Jose Manuel Cantera"
    },
    "Augmented Reality": {
      "backlog_keyword": "AugmentedReality",
      "chapter": "WebUI",
      "component": "10242",
      "owner": "Torsten Spieldenner"
    },
    "AuthZForce": {
      "backlog_keyword": "AuthorizationPDP",
      "chapter": "Security",
      "component": "10229",
      "owner": "Cyril Dangerville"
    },
    "Bosun": {
      "backlog_keyword": "PolicyMgr",
      "chapter": "Cloud",
      "component": "10207",
      "owner": "Fernando Lopez"
    },
    "Business Ecosystem": {
      "backlog_keyword": "BusinessAPIEcosystem",
      "chapter": "Apps",
      "component": "11505",
      "owner": "Francisco de la Vega"
    },
    "CEP": {
      "backlog_keyword": "CEP - IBM",
      "chapter": "Data",
      "component": "10209",
      "owner": "Uri Shani"
    },
    "CKAN": {
      "backlog_keyword": "CKAN",
      "chapter": "Data",
      "component": "10212",
      "owner": "Francisco de la Vega"
    },
    "Cepheus": {
      "backlog_keyword": "DataEdge-Cepheus",
      "chapter": "IoT",
      "component": "10222",
      "owner": "Martial Granger"
    },
    "Cloud Portal": {
      "backlog_keyword": "CloudPortal",
      "chapter": "Cloud",
      "component": "10202",
      "owner": "Alvaro Alonso"
    },
    "Cloud Render": {
      "backlog_keyword": "CloudRendering",
      "chapter": "WebUI",
      "component": "10238",
      "owner": "Cvetan Stefanovski"
    },
    "Cosmos": {
      "backlog_keyword": "BigData-Analysis",
      "chapter": "Data",
      "component": "10210",
      "owner": "Francisco Romero"
    },
    "Cyber Security": {
      "backlog_keyword": "CyberSecurity",
      "chapter": "Security",
      "component": "10231",
      "owner": "Bettan Olivier"
    },
    "Cygnus": {
      "backlog_keyword": "Cygnus",
      "chapter": "Data",
      "component": "11721",
      "owner": "Joaquín Salvachúa "
    },
    "Docker": {
      "backlog_keyword": "Docker",
      "chapter": "Cloud",
      "component": "11204",
      "owner": "Kenneth Nagin"
    },
    "EPCGE": {
      "backlog_keyword": "EPCGE",
      "chapter": "IoT",
      "component": "10224",
      "owner": "Gilles Privat"
    },
    "FastRTPS": {
      "backlog_keyword": "FastRTPS",
      "chapter": "I2ND",
      "component": "11838",
      "owner": "Jaime Martin Losa"
    },
    "Fives": {
      "backlog_keyword": "Fives",
      "chapter": "WebUI",
      "component": "10512",
      "owner": "Torsten Spieldenner"
    },
    "FogFlow": {
      "backlog_keyword": "FogFlow",
      "chapter": "Data",
      "component": "12002",
      "owner": "Bin Cheng"
    },
    "GIS Provider": {
      "backlog_keyword": "GISDataProvider",
      "chapter": "WebUI",
      "component": "10239",
      "owner": "Cyber Lightning"
    },
    "IDAS": {
      "backlog_keyword": "IDAS",
      "chapter": "IoT",
      "component": "10218",
      "owner": "Jose Gato Luis"
    },
    "IaaS RM": {
      "backlog_keyword": "ResMgmt",
      "chapter": "Cloud",
      "component": "10201",
      "owner": "Ezra Silvera"
    },
    "IoT Broker": {
      "backlog_keyword": "BackendIoTBroker",
      "chapter": "IoT",
      "component": "10219",
      "owner": "Stefan Gessler"
    },
    "IoT Discovery": {
      "backlog_keyword": "IoTDiscovery",
      "chapter": "IoT",
      "component": "10221",
      "owner": "Stefan Gessler"
    },
    "KeyRock": {
      "backlog_keyword": "IDM-KeyRock",
      "chapter": "Security",
      "component": "10228",
      "owner": "Alvaro Alonso"
    },
    "Kiara": {
      "backlog_keyword": "Kiara",
      "chapter": "I2ND",
      "component": "10214",
      "owner": "Jaime Martin Losa"
    },
    "Knowage": {
      "backlog_keyword": "DataVisualization",
      "chapter": "Apps",
      "component": "11905",
      "owner": "Davide Zerbetto"
    },
    "Kurento": {
      "backlog_keyword": "Stream-oriented",
      "chapter": "Data",
      "component": "10211",
      "owner": "NaevaTeC Development Team"
    },
    "Marketplace": {
      "backlog_keyword": "Marketplace",
      "chapter": "Apps",
      "component": "10103",
      "owner": "Aitor Magán"
    },
    "Monitoring": {
      "backlog_keyword": "Monitoring",
      "chapter": "Cloud",
      "component": "10206",
      "owner": "Fernando Lopez"
    },
    "Murano": {
      "backlog_keyword": "Murano",
      "chapter": "Cloud",
      "component": "10506",
      "owner": "Fernando Lopez"
    },
    "Netfloc": {
      "backlog_keyword": "Netfloc",
      "chapter": "I2ND",
      "component": "10254",
      "owner": "Thomas Michael Bohnert"
    },
    "OFNIC": {
      "backlog_keyword": "OFNIC",
      "chapter": "I2ND",
      "component": "10213",
      "owner": "Federico Cimorelli"
    },
    "Object Storage": {
      "backlog_keyword": "ObjectStorage",
      "chapter": "Cloud",
      "component": "10203",
      "owner": "Yosef Moatti"
    },
    "OpenMTC": {
      "backlog_keyword": "OpenMTC",
      "chapter": "IoT",
      "component": "12003",
      "owner": "Ronald Steinke"
    },
    "Ops-Dashboard": {
      "backlog_keyword": "Dash",
      "chapter": "Ops",
      "component": "10311",
      "owner": "Miguel Jiménez"
    },
    "Ops-Deploy": {
      "backlog_keyword": "Deploy",
      "chapter": "Ops",
      "component": "10310",
      "owner": "Daniele Santoro"
    },
    "Ops-Health": {
      "backlog_keyword": "Health",
      "chapter": "Ops",
      "component": "10312",
      "owner": "Fernando Lopez"
    },
    "Ops-Toolkit": {
      "backlog_keyword": "Toolkit",
      "chapter": "Ops",
      "component": "10313",
      "owner": "Ozdemir, Omer"
    },
    "Orion": {
      "backlog_keyword": "OrionContextBroker",
      "chapter": "Data",
      "component": "10208",
      "owner": "Jose Manuel Cantera"
    },
    "POI Provider": {
      "backlog_keyword": "POIDataProvider",
      "chapter": "WebUI",
      "component": "10240",
      "owner": "Ari Okkonen"
    },
    "Pegasus": {
      "backlog_keyword": "PaaSManager",
      "chapter": "Cloud",
      "component": "10205",
      "owner": "Henar Muñoz"
    },
    "Perseo": {
      "backlog_keyword": "Perseo",
      "chapter": "Data",
      "component": "11909",
      "owner": "Rafael Fernández"
    },
    "Privacy": {
      "backlog_keyword": "Privacy",
      "chapter": "Security",
      "component": "10233",
      "owner": "Stephan Neuhaus"
    },
    "Quantum Leap": {
      "backlog_keyword": "Quantum-Leap",
      "chapter": "Core",
      "component": "11558",
      "owner": "MARTEL"
    },
    "Real Virtual Interaction": {
      "backlog_keyword": "RealVirtualInteraction",
      "chapter": "WebUI",
      "component": "10243",
      "owner": "J-P Viuhkola"
    },
    "Repository": {
      "backlog_keyword": "Repository",
      "chapter": "Apps",
      "component": "10102",
      "owner": "Francisco de la Vega"
    },
    "Revenue": {
      "backlog_keyword": "RSS",
      "chapter": "Apps",
      "component": "10104",
      "owner": "Francisco de la Vega"
    },
    "Robotics": {
      "backlog_keyword": "Robotics",
      "chapter": "I2ND",
      "component": "10403",
      "owner": "Jaime Martin Losa"
    },
    "STH-Comet": {
      "backlog_keyword": "STH-Comet",
      "chapter": "Data",
      "component": "11908",
      "owner": "Joaquín Salvachúa "
    },
    "Sagitta": {
      "backlog_keyword": "SwDeployConfig",
      "chapter": "Cloud",
      "component": "10204",
      "owner": "Henar Muñoz"
    },
    "SpagoBI": {
      "backlog_keyword": "DataViz-SpagoBI",
      "chapter": "Apps",
      "component": "10106",
      "owner": "Davide Zerbetto"
    },
    "Synch - Tundra": {
      "backlog_keyword": "Synchronization",
      "chapter": "WebUI",
      "component": "10237",
      "owner": "Jonne Väisänen"
    },
    "Trust": {
      "backlog_keyword": "TrustworthyFactory",
      "chapter": "Security",
      "component": "10232",
      "owner": "Sebastien Keller"
    },
    "UI Designer": {
      "backlog_keyword": "InterfaceDesigner",
      "chapter": "WebUI",
      "component": "10245",
      "owner": "Cvetan Stefanovski"
    },
    "WStore": {
      "backlog_keyword": "Store",
      "chapter": "Apps",
      "component": "10105",
      "owner": "Francisco de la Vega"
    },
    "Web Tundra 3D": {
      "backlog_keyword": "WebTundra3D",
      "chapter": "WebUI",
      "component": "10236",
      "owner": "Cvetan Stefanovski"
    },
    "Web Tundra Avatar": {
      "backlog_keyword": "VirtualCharacters",
      "chapter": "WebUI",
      "component": "10244",
      "owner": "Jonne Väisänen"
    },
    "Wilma": {
      "backlog_keyword": "PEP-Proxy",
      "chapter": "Security",
      "component": "10402",
      "owner": "Alvaro Alonso"
    },
    "Wirecloud": {
      "backlog_keyword": "ApplicationMashup",
      "chapter": "Apps",
      "component": "10101",
      "owner": "Miguel Jiménez"
    },
    "XML3D": {
      "backlog_keyword": "XML3D",
      "chapter": "WebUI",
      "component": "10235",
      "owner": "Torsten Spieldenner"
    }
  }
}

    return result['book']


def find_nodesbook():
    # TODO: Need to get dinamically the information of the nodesbook, currently it is a static workaround just to
    #       stay working the tool
    # url = '{}'.format(domain) + '/api/nodesbook'
    # answer = get(url, auth=auth)

    # if not answer.ok:
    #     raise Exception

    result = {
  "book": {
    "Berlin": {
      "support": "BerlinSupportTeam"
    },
    "Brittany": {
      "support": "support-brittany"
    },
    "Budapest": {
      "support": "WIGNER"
    },
    "Crete": {
      "support": "CreteNHD"
    },
    "Genoa": {
      "support": "tntlab"
    },
    "Gent": {
      "support": "IMINDS"
    },
    "Hannover": {
      "support": "netzlink"
    },
    "Karlskrona": {
      "support": "BTH"
    },
    "Lannion": {
      "support": "lannionsupport"
    },
    "Messina": {
      "support": "MessinaNHD"
    },
    "Mexico": {
      "support": "internetdelfuturo"
    },
    "Netherland": {
      "support": ""
    },
    "PiraeusN": {
      "support": "neuropublic"
    },
    "PiraeusU": {
      "support": "UPRC"
    },
    "Poznan": {
      "support": "PSNC"
    },
    "Prague": {
      "support": "prgsupportteam"
    },
    "SaoPaolo": {
      "support": "pad_lsi"
    },
    "SophiaAntipolis": {
      "support": "Com4Innov"
    },
    "Spain": {
      "support": "spain.node"
    },
    "SpainTenerife": {
      "support": "fw_support_st"
    },
    "Stockholm": {
      "support": "stockholm"
    },
    "Trento": {
      "support": "TrentoNodeTeam"
    },
    "Vicenza": {
      "support": "mauropecetti"
    },
    "Volos": {
      "support": "UTH"
    },
    "Waterford": {
      "support": "Tynan"
    },
    "Wroclaw": {
      "support": "radamkiewicz"
    },
    "Zurich": {
      "support": "ZHAW Node Helpdesk"
    },
    "ZurichS": {
      "support": "zurichs"
    }
  }
}
    return result['book']


def find_chaptersbook():
    # TODO: Need to get dinamically the information of the chaptersbook, currently it is a static workaround just to
    #       stay working the tool
    # url = '{}'.format(domain) + '/api/chaptersbook'
    # answer = get(url, auth=auth)

    # if not answer.ok:
    #     raise Exception

    result = {
  "book": {
    "Apps": {
      "coordination_key": "10255",
      "leader": "Alessandro Portosa"
    },
    "Cloud": {
      "coordination_key": "10261",
      "leader": "Kenneth Nagin"
    },
    "Data": {
      "coordination_key": "10262",
      "leader": "Jose Manuel Cantera"
    },
    "I2ND": {
      "coordination_key": "10263",
      "leader": "Jaime Martin Losa"
    },
    "IoT": {
      "coordination_key": "10264",
      "leader": "Martial Granger"
    },
    "Ops": {
      "coordination_key": "10268",
      "leader": "Federico Michele Facca"
    },
    "Security": {
      "coordination_key": "10265",
      "leader": "Pascal Bisson"
    },
    "WebUI": {
      "coordination_key": "10266",
      "leader": "Philipp Slusallek"
    }
  }
}
    return result['book']
