import pynvml, time
from pynvml import *

# Disable stdout printing
import os
import sys
f = open(os.devnull, 'w')
sys.stdout = f

import argparse
CLI=argparse.ArgumentParser()
CLI.add_argument("--gpu_ids", nargs="*", type=int, default=[])
args = CLI.parse_args()

TEMP_MIN_VALUE = 50.0 # fan is around 30%
TEMP_MAX_VALUE = 80.0 # fan is at 100% onwards
TEMP_RANGE = TEMP_MAX_VALUE - TEMP_MIN_VALUE
def fanspeed_from_t(t):
  if t <= TEMP_MIN_VALUE: return 0.0
  if t >= TEMP_MAX_VALUE: return 1.0
  return (t - TEMP_MIN_VALUE) / TEMP_RANGE

try:
  _nvmlGetFunctionPointer = pynvml._nvmlGetFunctionPointer
  _nvmlCheckReturn = pynvml._nvmlCheckReturn
except AttributeError as err:
  _nvmlGetFunctionPointer = pynvml.nvml._nvmlGetFunctionPointer
  _nvmlCheckReturn = pynvml.nvml._nvmlCheckReturn


nvmlInit()

def alex_nvmlDeviceGetMinMaxFanSpeed(handle):
  c_minSpeed = c_uint()
  c_maxSpeed = c_uint()
  fn = _nvmlGetFunctionPointer("nvmlDeviceGetMinMaxFanSpeed")
  ret = fn(handle, byref(c_minSpeed), byref(c_maxSpeed))
  _nvmlCheckReturn(ret)
  return c_minSpeed.value, c_maxSpeed.value

class Device:
  def __init__(self, index):
    self.index = index
    self.handle = nvmlDeviceGetHandleByIndex(index)
    self.name = nvmlDeviceGetName(self.handle)
    self.fan_count = nvmlDeviceGetNumFans(self.handle)
    self.fan_min, self.fan_max = alex_nvmlDeviceGetMinMaxFanSpeed(self.handle)
    self._fan_range = self.fan_max - self.fan_min

  def temp(self):
    return nvmlDeviceGetTemperature(self.handle, NVML_TEMPERATURE_GPU)

  def fan_percentages(self):
    return [nvmlDeviceGetFanSpeed_v2(self.handle, i) for i in range(self.fan_count)]

  def set_fan_speed(self, percentage):
    """ WARNING: This function changes the fan control policy to manual. It means that YOU have to monitor the temperature and adjust the fan speed accordingly. If you set the fan speed too low you can burn your GPU! Use nvmlDeviceSetDefaultFanSpeed_v2 to restore default control policy.
    """
    for i in range(self.fan_count):
      nvmlDeviceSetFanSpeed_v2(self.handle, i, percentage)

  def query(self):
    return f"{self.index}:{self.name} {self.temp()}@{self.fan_percentages()}"

  def control(self):
    t = self.temp()
    fans = self.fan_percentages()
    current = round(sum(fans) / len(fans))
    shouldbe = round(fanspeed_from_t(t) * self._fan_range + self.fan_min)
    if(shouldbe != current):
      print(f"{self.index}:{self.name} t={t} {current} >> {shouldbe}")
      # change fan speed
      self.set_fan_speed(shouldbe)

  def __str__(self):
    return f"{self.index}:{self.name} fans={self.fan_count} {self.fan_min}-{self.fan_max}"
  __repr__ = __str__

print(f"Driver Version: {nvmlSystemGetDriverVersion()}")
device_count = nvmlDeviceGetCount()
print('CLI args', args.gpu_ids)

if args.gpu_ids:
  devices = [Device(i) for i in range(device_count) if i in args.gpu_ids]
else:
  devices = [Device(i) for i in range(device_count)]

for device in devices:
  print(device)
print()

def main():
  try:
    while True:
      for device in devices:
        # print(device.query())
        device.control()
      time.sleep(1)
  finally:
    # reset to auto fan control
    for device in devices:
      for i in range(device.fan_count):
        nvmlDeviceSetDefaultFanSpeed_v2(device.handle, i)
    nvmlShutdown()

if __name__ == "__main__":
  main()
