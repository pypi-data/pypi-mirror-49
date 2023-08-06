from enum import Enum

class SwaConfiendtiality(Enum):
    PUBLIC = "SWA Public"
    INTERNAL = "SWA Internal Only"
    CONFIDENTIAL = "SWA Confidential"

class SwaCompliance(Enum):
    PCI = "PCI"
    PII = "PII"
    SOX = "SOX"
    FAA = "FAA"
    GDPR = "GDPR"
    NA = "N/A"

class SwaEnvironment(Enum):
    DEV = "DEV"
    QA = "QA"
    PROD = "PROD"

class SwaApplicationRecovery(Enum):
    RTF = "Required To Fly"
    REQ_INFRA = "Required Infrastructure"
    RTO = "Required To Operate"
    CTB = "Critical To Business"
    BUS_SUPP = "Business Support"

class SwaTags():

    tags = {}

    def __init__(self, name: str, cost_center: str, pid: str, confidentiality: SwaConfiendtiality, #NOSONAR
                compliance: [SwaCompliance], environment: SwaEnvironment, business_service: str,
                application_recovery: SwaApplicationRecovery):
        comp_str = []

        for item in compliance:
            comp_str.append(item.value)

        self.tags.update({"SWA:Name": name})
        self.tags.update({"SWA:CostCenter": cost_center})
        self.tags.update({"SWA:PID": pid})
        self.tags.update({"SWA:Confidentiality": confidentiality.value})
        self.tags.update({"SWA:Compliance": ",".join(map(str, comp_str))})
        self.tags.update({"SWA:Environment": environment.value})
        self.tags.update({"SWA:BusinessService": business_service})
        self.tags.update({"SWA:Application Recovery Hierarchy": application_recovery.value})