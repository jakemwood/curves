from ctypes import *


class FCC_Curves():
    PROTECTED_CONTOUR = 0
    INTERFERENCE_CONTOUR = 1

    def __init__(self):
        # Import C library
        cdll.LoadLibrary("curves_subroutines.so")
        fcurves_lib = CDLL("curves_subroutines.so")

        self._tvfmfs_metric = fcurves_lib.tvfmfs_metric_
        self._tvfmfs_metric.restype = c_int
        self._tvfmfs_metric.argtypes = [POINTER(c_float),  # ERP (kW)
                                        POINTER(c_float),  # HAAT (meters)
                                        POINTER(c_long),  # channel
                                        POINTER(c_float),  # field strength (dBu)
                                        POINTER(c_float),  # distance (km)
                                        POINTER(c_long),  # switch (1 = field strength, 2 = distance)
                                        POINTER(c_long),  # curve (0 = F(50,50), 1=F(50,10))
                                        POINTER(c_byte * 2), c_long]  # error flag

    def curve(self, erp, haat, channel, dbu, ip):
        erp = c_float(erp)
        haat = c_float(haat)
        dbu = c_float(dbu)
        channel = c_long(channel)
        ip = c_long(ip)
        switch = c_long(2)
        distance = c_float(100)
        flag = (c_byte * 2)(ord(' '), ord(' '))

        self._tvfmfs_metric(byref(erp), byref(haat), byref(channel), byref(dbu), byref(distance), byref(switch),
                            byref(ip), byref(flag), 2)

        return distance.value
