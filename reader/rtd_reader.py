"""Read RTD data from Think or Swim"""
import pythoncom
from rtd import RTDClient

tos = RTDClient('TOS.RTD')
tos.connect()
