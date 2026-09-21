#!python3
import os
import wave
import array


DAC_bit = 12    # 8, 12, or 16

Tim_len = 10    # second


def wave2c(path, name):
    try:
        wav = wave.open(path, 'rb')

        nchannels, sampwidth, framerate, nframes = wav.getparams()[:4]

        wavbin = wav.readframes(nframes)

        wav.close()

    except Exception as e:
        print(f'{path} open fail')

    else:
        print(f'{path}\n\t声道数：{nchannels}, 量化位数：{sampwidth * 8}, 采样频率：{framerate}, 采样点数：{nframes}')

        if sampwidth == 1:
            wavArr = array.array('B', wavbin)

            if DAC_bit == 12:
                wavArr = array.array('H', [x << 4 for x in wavArr])
            elif DAC_bit == 16:
                wavArr = array.array('H', [x << 8 for x in wavArr])

        elif sampwidth == 2:
            wavArr = array.array('H', wavbin)

            if DAC_bit == 8:
                wavArr = array.array('B', [x >> 8 for x in wavArr])
            elif DAC_bit == 12:
                wavArr = array.array('H', [x >> 4 for x in wavArr])

        else:
            print(f'\tSample Width > 16-bit, Not Support!')
            return

        wavArr = wavArr[:framerate * Tim_len * nchannels]

        if nchannels == 1:
            if DAC_bit == 8:
                txt = f'const unsigned char wave_{name}[{len(wavArr)}] = {{\n'
                
            else:
                txt = f'const unsigned short wave_{name}[{len(wavArr)}] = {{\n'
            
            wavArr = [f'0x{x:02X},' if DAC_bit == 8 else f'0x{x:04X},' for x in wavArr]
            lines = [' '.join(wavArr[i:i+16]) for i in range(0, len(wavArr), 16)]
            txt += '\n'.join(lines) + '\n};\n'
            
        elif nchannels == 2:
            if DAC_bit == 8:
                txtL = f'const unsigned char waveL_{name}[{len(wavArr)//2}] = {{\n'
                txtR = f'const unsigned char waveR_{name}[{len(wavArr)//2}] = {{\n'

            else:
                txtL = f'const unsigned short waveL_{name}[{len(wavArr)//2}] = {{\n'
                txtR = f'const unsigned short waveR_{name}[{len(wavArr)//2}] = {{\n'

            wavArrL, wavArrR = wavArr[0::2], wavArr[1::2]

            wavArrL = [f'0x{x:02X},' if DAC_bit == 8 else f'0x{x:04X},' for x in wavArrL]
            lines = [' '.join(wavArrL[i:i+16]) for i in range(0, len(wavArrL), 16)]
            txtL += '\n'.join(lines) + '\n};\n'

            wavArrR = [f'0x{x:02X},' if DAC_bit == 8 else f'0x{x:04X},' for x in wavArrR]
            lines = [' '.join(wavArrR[i:i+16]) for i in range(0, len(wavArrR), 16)]
            txtR += '\n'.join(lines) + '\n};\n'

            txt = f'{txtL}\n\n{txtR}'

        else:
            print(f'\tChannel Count > 2, Not Support!')
            return

        try:
            open(f'{path}.c', 'w', encoding='utf-8').write(txt)

        except Exception as e:
            pass


for name in os.listdir('.'):
    if name.lower().endswith('.wav'):
        wave2c(os.path.join(os.getcwd(), name), os.path.splitext(name)[0])
