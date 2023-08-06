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

    tags = []

    def __init__(self, name: str, cost_center: str, pid: str, confidentiality: SwaConfiendtiality, #NOSONAR
                compliance: [SwaCompliance], environment: SwaEnvironment, business_service: str,
                application_recovery: SwaApplicationRecovery):
        comp_str = []

        for item in compliance:
            comp_str.append(item.value)

        self.tags.append({"SWA:Name": name})
        self.tags.append({"SWA:CostCenter": cost_center})
        self.tags.append({"SWA:PID": pid})
        self.tags.append({"SWA:Confidentiality": confidentiality.value})
        self.tags.append({"SWA:Compliance": ",".join(map(str, comp_str))})
        self.tags.append({"SWA:Environment": environment.value})
        self.tags.append({"SWA:BusinessService": business_service})
        self.tags.append({"SWA:Application Recovery Hierarchy": application_recovery.value})

tags = SwaTags(name = "MyApp", cost_center = "123", pid = "456", confidentiality = SwaConfiendtiality.PUBLIC, #NOSONAR
                compliance= [SwaCompliance.PII], environment = SwaEnvironment.DEV, business_service = "foobar",
                application_recovery = SwaApplicationRecovery.RTF)

print(tags.tags)