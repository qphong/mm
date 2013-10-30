

filenamed=open('gps_data.txt','r');
filenamed.readline();
for lineR in filenamed:
    lineRS=lineR.split();
    numbers=[float(jj) for jj in lineRS[2:4]];
#
    TNc_x=UTM.LLtoUTM(23, numbers[1], numbers[0], zone = None)[1];
    TNc_y=UTM.LLtoUTM(23, numbers[1], numbers[0], zone = None)[2];


def mdf(vect):
	
	vect[0] = -9999
	vect.append(12)
