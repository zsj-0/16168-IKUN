import sensor, image, time,ustruct,math,pyb
from pyb import Pin, Timer
from pyb import UART,LED
import json
from pyb import UART,LED
clock = time.clock()
TRA_TH= [(128, 255)]
TRA_AngTH=30
TRA_ROIS = [
		(0, 100, 160, 20, 0.7),
		(0,  50, 160, 20, 0.3),
		(0,   0, 160, 20, 0.1)
	   ]
Weight_Sum = 0
for r in TRA_ROIS: Weight_Sum += r[4]
OBS_ROI = [(30 , 10, 100, 100)]
Run	 = bytearray([0x24,0x4F,0x4D,0x56,0x31,0x26,0x23])
Left	= bytearray([0x24,0x4F,0x4D,0x56,0x32,0x26,0x23])
Right   = bytearray([0x24,0x4F,0x4D,0x56,0x33,0x26,0x23])
Stop	= bytearray([0x24,0x4F,0x4D,0x56,0x34,0x26,0x23])
def Get_MaxIndex(blobs):
	maxb_index=0
	max_pixels=0
	for i in range(len(blobs)):
		if blobs[i].pixels() > max_pixels:
			max_pixels = blobs[i].pixels()
			maxb_index = i
			return  maxb_index
def Recive_Data():
	global OVSys_State
	if uart.any():
		OVSys_State=int(uart.read())
		print(OVSys_State)
def sending_data(cx,cy,cw,ch):
	global uart;
	data = ustruct.pack("<bbhhhhb",
				   0x2C,
				   0x12,
				   int(cx),
				   int(cy),
				   int(cw),
				   int(ch),
				   0x5B)
	uart.write(data);
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
uart = UART(3,115200)
uart.init(115200, bits=8, parity=None, stop=1)
while (1):
	clock.tick()
	if (1):
			sensor.set_pixformat(sensor.GRAYSCALE)
			TRA_img = sensor.snapshot().histeq()
			TRA_img.mean(1)
			TRA_img.binary([(0,35)])
			Centroid_Sum = 0
			for r in TRA_ROIS:
				blobs = TRA_img.find_blobs(TRA_TH, roi=r[0:4], pixels_threshold=100, area_threshold=100,merge=True)
				if blobs:
					maxb_index = Get_MaxIndex(blobs)
					TRA_img.draw_rectangle(blobs[maxb_index].rect(), thickness = 2, fill = False)
					TRA_img.draw_cross(blobs[maxb_index].cx(),blobs[maxb_index].cy())
					Centroid_Sum += blobs[maxb_index].cx() * r[4]
			Center_Pos = (Centroid_Sum / Weight_Sum)
			Deflection_Angle = 0
			Deflection_Angle = -math.atan((Center_Pos-80)/60)
			Deflection_Angle =int( math.degrees(Deflection_Angle))
			cx=Deflection_Angle
			cy=0
			cw=0
			ch=0
			Angle_err=Deflection_Angle
			FH = bytearray([0x2C,0x12,cx,cy,cw,ch,0x5B])
			if abs(Deflection_Angle) > TRA_AngTH:
				if Deflection_Angle>0:
						uart.write(FH)
						print(cx,cy,cw,ch)
						print("Turn Right")
						print("Turn Angle: %f" % Deflection_Angle)
				if Deflection_Angle < 0:
						uart.write(FH)
						print(cx,cy,cw,ch)
						print("Turn ：Left")
						print("Turn Angle: %f" % Deflection_Angle)
				if abs(Deflection_Angle) <= TRA_AngTH:
						uart.write(FH)
						print(cx,cy,cw,ch)
						print("Run")
						print("Turn Angle: %f" % Deflection_Angle)