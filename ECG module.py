import os
import csv
import array
import base64
import xmltodict
import numpy as np

class ECGXMLReader:
    def __init__(self, path, augmentLeads=False):
        try:
            with open(path, 'rb') as xml:
                self.ECG = xmltodict.parse(xml.read().decode('utf-8'))
            self.path = path
            self.PatientDemographics = self.ECG['RestingECG']['PatientDemographics']
            self.TestDemographics = self.ECG['RestingECG']['TestDemographics']
            self.RestingECGMeasurements = self.ECG['RestingECG']['RestingECGMeasurements']
            self.Waveforms = self.ECG['RestingECG']['Waveform']
            self.LeadVoltages = self.makeLeadVoltages()
        except Exception as e:
            print(str(e))

    def makeLeadVoltages(self):
        num_leads = 0
        leads = {}
        for lead in self.Waveforms[1]['LeadData']:
            num_leads += 1
            lead_data = lead['WaveFormData']
            lead_b64 = base64.b64decode(lead_data)
            lead_vals = np.array(array.array('h', lead_b64))
            leads[ lead['LeadID']] =lead_vals
        return leads

    def getLeadVoltages(self, LeadID):
        return self.LeadVoltages[LeadID]

    def getAllVolages(self):
        return self.LeadVoltages

res = ECGXMLReader('./MUSE_20201218_172156_13000.xml')
print(res.getAllVolages())
