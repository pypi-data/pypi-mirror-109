#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 11:15:55 2021

i@author: Lars Stenseng
@mail: lars@stenseng.net
"""

from time import time

from bitstring import Bits, pack


class Rtcm3:
    __framePreample = Bits(bin="0b11010011")
    __frameHeaderFormat = "bin:8, pad:6, uint:10, uint:12"
    __msg1029 = (
        "uint:12=1029, uint:12=refStationId, uint:16=mjd, "
        "uint:17=utc, uint:7=utfChars, uint:8=charBytes, "
        "bytes=string"
    )

    def __init__(self):
        pass

    def mjd(self, unixTimestamp):
        mjd = int(unixTimestamp / 86400.0 + 40587.0)
        return mjd

    def encodeRtcmFrame(self, messageType: int, dataDict):
        message = self.encodeRtcmMessage(messageType, dataDict)
        rtcmFrame = message
        return rtcmFrame

    def decodeRtcmFrame(self, rtcmFrame):
        pass

    def encodeRtcmMessage(self, messageType: int, dataDict):
        if messageType == 1029:
            utfStr = "Default string"
            default = {
                "refStationId": 0,
                "mjd": self.mjd(time()),
                "utc": int(time() % 86400),
                "utfChars": 0,
                "charBytes": 0,
                "string": utfStr,
            }
            data = {key: dataDict.get(key, default[key]) for key in default}
            data["utfChars"] = len(data["string"])
            data["string"] = data["string"].encode()
            data["charBytes"] = len(data["string"])
            message = pack(self.__msg1029, **data)
            return message

    def decodeRtcmMessage(self, message):
        messageType = message.peek("uint:12")
        if messageType == 1029:
            data = []
            data = message.unpack(self.__msg1029)
            # dataDict = {}
            return messageType, data  # Dict

    messageDescription = {
        1001: "L1-Only GPS RTK Observables",
        1002: "Extended L1-Only GPS RTK Observables",
        1003: "L1&L2 GPS RTK Observables",
        1004: "Extended L1&L2 GPS RTK Observables",
        1005: "Stationary RTK Reference Station ARP",
        1006: "Stationary RTK Reference Station ARP with Antenna Height",
        1007: "Antenna Descriptor",
        1008: "Antenna Descriptor & Serial Number",
        1009: "L1-Only GLONASS RTK Observables",
        1010: "Extended L1-Only GLONASS RTK Observables",
        1011: "L1&L2 GLONASS RTK Observables",
        1012: "Extended L1&L2 GLONASS RTK Observables",
        1013: "System Parameters",
        1014: "Network Auxiliary Station Data",
        1015: "GPS Ionospheric Correction Differences",
        1016: "GPS Geometric Correction Differences",
        1017: "GPS Combined Geometric and Ionospheric Correction " + "Differences",
        1018: "RESERVED for Alternative Ionospheric Correction Difference " + "Message",
        1019: "GPS Ephemerides",
        1020: "GLONASS Ephemerides",
        1021: "Helmert / Abridged Molodenski Transformation Parameters",
        1022: "Molodenski-Badekas Transformation Parameters",
        1023: "Residuals, Ellipsoidal Grid Representation",
        1024: "Residuals, Plane Grid Representation",
        1025: "Projection Parameters, Projection Types other than "
        + "Lambert Conic Conformal (2 SP) and Oblique Mercator",
        1026: "Projection Parameters, Projection Type LCC2SP "
        + "(Lambert Conic Conformal (2 SP))",
        1027: "Projection Parameters, Projection Type OM " + "(Oblique Mercator)",
        1028: "(Reserved for Global to Plate-Fixed Transformation)",
        1029: "Unicode Text String",
        1030: "GPS Network RTK Residual Message",
        1031: "GLONASS Network RTK Residual Message",
        1032: "Physical Reference Station Position Message",
        1033: "Receiver and Antenna Descriptors",
        1034: "GPS Network FKP Gradient",
        1035: "GLONASS Network FKP Gradient",
        1037: "GLONASS Ionospheric Correction Differences",
        1038: "GLONASS Geometric Correction Differences",
        1039: "GLONASS Combined Geometric and Ionospheric Correction " + "Differences",
        1042: "BDS Satellite Ephemeris Data",
        1044: "QZSS Ephemerides",
        1045: "Galileo F/NAV Satellite Ephemeris Data",
        1046: "Galileo I/NAV Satellite Ephemeris Data",
        1057: "SSR GPS Orbit Correction",
        1058: "SSR GPS Clock Correction",
        1059: "SSR GPS Code Bias",
        1060: "SSR GPS Combined Orbit and Clock Corrections",
        1061: "SSR GPS URA",
        1062: "SSR GPS High Rate Clock Correction",
        1063: "SSR GLONASS Orbit Correction",
        1064: "SSR GLONASS Clock Correction",
        1065: "SSR GLONASS Code Bias",
        1066: "SSR GLONASS Combined Orbit and Clock Corrections",
        1067: "SSR GLONASS URA",
        1068: "SSR GLONASS High Rate Clock Correction",
        1070: "Reserved MSM",
        1071: "GPS MSM1",
        1072: "GPS MSM2",
        1073: "GPS MSM3",
        1074: "GPS MSM4",
        1075: "GPS MSM5",
        1076: "GPS MSM6",
        1077: "GPS MSM7",
        1078: "Reserved MSM",
        1079: "Reserved MSM",
        1080: "Reserved MSM",
        1081: "GLONASS MSM1",
        1082: "GLONASS MSM2",
        1083: "GLONASS MSM3",
        1084: "GLONASS MSM4",
        1085: "GLONASS MSM5",
        1086: "GLONASS MSM6",
        1087: "GLONASS MSM7",
        1088: "Reserved MSM",
        1089: "Reserved MSM",
        1090: "Reserved MSM",
        1091: "Galileo MSM1",
        1092: "Galileo MSM2",
        1093: "Galileo MSM3",
        1094: "Galileo MSM4",
        1095: "Galileo MSM5",
        1096: "Galileo MSM6",
        1097: "Galileo MSM7",
        1098: "Reserved MSM",
        1099: "Reserved MSM",
        1100: "Reserved MSM",
        1101: "SBAS MSM1",
        1102: "SBAS MSM2",
        1103: "SBAS MSM3",
        1104: "SBAS MSM4",
        1105: "SBAS MSM5",
        1106: "SBAS MSM6",
        1107: "SBAS MSM7",
        1108: "Reserved MSM",
        1109: "Reserved MSM",
        1110: "Reserved MSM",
        1111: "QZSS MSM1",
        1112: "QZSS MSM2",
        1113: "QZSS MSM3",
        1114: "QZSS MSM4",
        1115: "QZSS MSM5",
        1116: "QZSS MSM6",
        1117: "QZSS MSM7",
        1118: "Reserved MSM",
        1119: "Reserved MSM",
        1120: "Reserved MSM",
        1121: "BeiDou MSM1",
        1122: "BeiDou MSM2",
        1123: "BeiDou MSM3",
        1124: "BeiDou MSM4",
        1125: "BeiDou MSM5",
        1126: "BeiDou MSM6",
        1127: "BeiDou MSM7",
        1128: "Reserved MSM",
        1129: "Reserved MSM",
        1130: "Reserved MSM",
        1230: "GLONASS L1 and L2 Code-Phase Biases"
        # 4001-4095: "Proprietary Messages"
    }
